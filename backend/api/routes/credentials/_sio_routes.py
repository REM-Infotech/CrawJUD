from flask_socketio import Namespace


class CredenciaisRobosNS(Namespace):
    def __init__(self) -> None:
        super().__init__("/admin/credenciais")

    def on_connect(self) -> None:

        print("ok")  # noqa: T201
