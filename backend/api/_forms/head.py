from __future__ import annotations

import json
import traceback
from typing import TYPE_CHECKING, ClassVar, Self

from flask import request
from flask_jwt_extended import get_current_user

from backend.api.extensions import celery
from backend.api.models import Bots, LicenseUser, User, db
from backend.api.resources import camel_to_snake

if TYPE_CHECKING:
    from backend.api.types_app import Dict


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
        form_name: str = request_data["configuracao_form"]
        kwargs: dict = {
            k: v
            for k, v in list(request_data.items())
            if k != "configuracao_form"
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
            kwargs["pid"] = pid_exec
            # Busca o bot no banco de dados
            bot = db.session.query(Bots).filter(Bots.Id == self.bot_id).first()
            user: User = get_current_user()
            kwargs["sistema"] = bot.sistema.lower()
            kwargs["categoria"] = bot.categoria.lower()

            # Envia tarefa principal
            celery.send_task("crawjud", kwargs={"config": kwargs})

            # Notifica o usuário sobre o início da execução
            celery.send_task(
                "notifica_usuario",
                kwargs={
                    "pid": pid_exec,
                    "bot_id": bot.Id,
                    "user_id": user.Id,
                    "xlsx": kwargs.get("planilha_xlsx"),
                    "tipo_notificacao": "start",
                },
            )
        except Exception as e:
            # Loga a exceção para depuração
            _exc = "\n".join(traceback.format_exception(e))

    def to_dict(self) -> Dict:
        """Converta os atributos do formulário em um dicionário serializável.

        Returns:
            Dict: Dicionário com os dados do formulário.

        """
        data = {}

        # Filtra atributos públicos e não métodos
        keys = list(
            filter(
                lambda key: not key.startswith("_")
                and not callable(getattr(self, key, None)),
                dir(self),
            ),
        )

        for key in keys:
            value = getattr(self, key)
            if key == "credencial":
                # Busca credencial do usuário logado
                user: User = get_current_user()
                # Acessa 'credenciais' antes de fechar a sessão para evitar DetachedInstanceError
                lic = (
                    db.session.query(LicenseUser)
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
                data.update({
                    "credenciais": {
                        "username": credencial.login,
                        "password": credencial.password,
                    },
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
