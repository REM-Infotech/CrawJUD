"""Inicialize a aplicação Flask principal da API CrawJUD.

Este módulo configura a aplicação, carrega variáveis de ambiente,
define o contexto de criptografia e fornece a função de criação da app.
"""

from dotenv import load_dotenv
from dynaconf import FlaskDynaconf
from flask import Flask
from passlib.context import CryptContext
from werkzeug.middleware.proxy_fix import ProxyFix

from backend.config import settings

# Instancia a aplicação Flask
app: Flask = Flask(__name__)
# Carrega variáveis de ambiente do .env
load_dotenv()

# Define o contexto de criptografia para senhas
crypt_context: CryptContext = CryptContext.from_string("""
[passlib]
schemes = argon2, bcrypt
default = argon2
deprecated = bcrypt
""")


def create_app() -> Flask:
    """Crie e configure a aplicação Flask.

    Returns:
        Flask: Instância configurada da aplicação Flask.

    """
    # Configura a aplicação com Dynaconf
    FlaskDynaconf(
        app=app,
        instance_relative_config=True,
        extensions_list="EXTENSIONS",  # pyright: ignore[reportArgumentType]
        dynaconf_instance=settings,
    )

    # Adiciona middleware para corrigir headers de proxy reverso
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_prefix=1,
    )
    return app
