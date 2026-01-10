from __future__ import annotations

import json
import traceback
from base64 import b64encode
from typing import TYPE_CHECKING, ClassVar, Self

from flask import current_app, request
from flask_jwt_extended import get_current_user

from backend.api.resources import camel_to_snake, formata_string
from backend.common.exceptions._fatal import FatalError
from backend.extensions import celery, db
from backend.models import Bots, LicenseUser, User

if TYPE_CHECKING:
    from flask_keepass import KeepassManager
    from pykeepass import Attachment

    from typings import Dict


class FormBot:
    """Classe base para formulários de bots.

    Gerencia o registro dinâmico de subclasses e fornece métodos utilitários
    para carregar formulários, manipular tarefas e converter dados.
    """

    _subclass: ClassVar[dict[str, type[Self]]] = {}

    @classmethod
    def load_form(cls) -> Self:
        """Carregue e retorne uma instância do formulário solicitado.

        Args:
            cls (type[Self]): Classe do formulário.

        Returns:
            Self: Instância do formulário carregado.

        """
        # Obtém os dados do request e identifica o formulário a ser carregado
        request_data: Dict = json.loads(request.get_data())
        form_name: str = camel_to_snake(
            request_data["configuracao_form"],
        )
        kwargs: dict = {
            k.lower(): v
            for k, v in list(request_data.items())
            if k != "configuracao_form" and k != "seeduploadedfiles"
        }
        return cls._subclass[form_name.replace("_", "")](**kwargs)

    def handle_task(self, pid_exec: str) -> None:
        """Envie tarefas para execução assíncrona via Celery e notifique o usuário.

        Args:
            pid_exec (str): Identificador do processo de execução.

        """
        try:
            # Converte os dados do formulário para dicionário

            kwargs = self.to_dict()
            # Busca o bot no banco de dados
            bot = db.session.query(Bots).filter(Bots.Id == self.bot_id).first()
            user: User = get_current_user()

            kwargs.update({
                "id_execucao": pid_exec,
                "bot_id": bot.Id,
                "user_id": user.Id,
                "sistema": bot.sistema.lower(),
                "categoria": bot.categoria.lower(),
            })

            keyword_args = list(kwargs.items())

            for k, v in keyword_args:
                if k in ["xlsx", "anexos", "kdbx", "certificado"]:
                    if isinstance(v, list):
                        kwargs.update({
                            k: [formata_string(i) for i in v],
                        })
                        continue

                    kwargs.update({k: formata_string(v)})

            # Envia tarefa principal
            cookies = request.cookies.to_dict(flat=True)
            cookies = json.dumps(request.cookies.to_dict()).encode()

            kwargs.update(
                {"cookies": b64encode(cookies).decode()},
            )

            celery.send_task(
                f"{kwargs['categoria']}_{kwargs['sistema']}",
                kwargs={"config": kwargs},
            )

            # Notifica o usuário sobre o início da execução
            celery.send_task(
                "notifica_usuario",
                kwargs={
                    "id_execucao": pid_exec,
                    "bot_id": bot.Id,
                    "user_id": user.Id,
                    "xlsx": kwargs.get("xlsx"),
                    "tipo_notificacao": "start",
                },
            )
        except Exception as e:
            # Loga a exceção para depuração
            exc = "\n".join(traceback.format_exception(e))
            raise FatalError(e, msg=exc) from e

    def to_dict(self) -> Dict:
        """Converta os atributos do formulário em um dicionário serializável.

        Returns:
            Dict: Dicionário com os dados do formulário.

        """
        data = {
            "credenciais": {},
        }

        # Filtra atributos públicos e não métodos
        keys = list(
            filter(
                lambda key: not key.startswith("_") and not callable(getattr(self, key, None)),
                dir(self),
            ),
        )
        keepass: KeepassManager = current_app.extensions["keepass"]
        for key in keys:
            value = getattr(self, key)
            if key == "credencial":
                # Busca credencial do usuário logado
                user: User = get_current_user()
                # Acessa 'credenciais' antes de fechar a sessão
                # para evitar DetachedInstanceError
                lic = (
                    db.session
                    .query(LicenseUser)
                    .select_from(User)
                    .join(LicenseUser.usuarios)
                    .filter(User.Id == user.Id)
                    .first()
                )
                credencial = list(
                    filter(
                        lambda x: x.Id == int(value),
                        lic.credenciais,
                    ),
                )[-1]

                entry = keepass.find_entries(
                    first=True,
                    title=credencial.nome_credencial,
                    notes=credencial.rastreio,
                )

                if credencial.login_metodo == "pw":
                    data.update({
                        "credenciais": {
                            "username": entry.username,
                            "password": entry.password,
                            "otp": entry.otp,
                        },
                    })
                    continue

                data_cred = {
                    "username": entry.username,
                    "password": entry.password,
                    "nome_certificado": "",
                    "certificado": "",
                    "otp": entry.otp,
                }

                if entry.attachments:
                    attachment: Attachment = entry.attachments[0]
                    data_cred.update({
                        "nome_certificado": attachment.filename,
                        "certificado": b64encode(
                            attachment.data,
                        ).decode(),
                    })

                data.update({
                    "credenciais": data_cred,
                })

                continue

            if key == "sid_filesocket":
                # Renomeia o campo para compatibilidade com o MinIO
                data.update({"folder_objeto_minio": value})
                continue

            data.update({key: value})

        return data

    def __init_subclass__(cls: type[Self]) -> None:
        """Registre automaticamente subclasses para carregamento dinâmico.

        Args:
            cls (type[Self]): Subclasse a ser registrada.

        """
        cls._subclass[camel_to_snake(cls.__name__.lower())] = cls
