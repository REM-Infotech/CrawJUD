from flask_socketio import Namespace


class CredenciaisRobosNS(Namespace):
    def __init__(self) -> None:
        self._namespace = "/admin/credenciais"
        super().__init__(self._namespace)

    def on_disconnect(self) -> None:

        return ""

    def on_connect(self) -> None:

        return ""
