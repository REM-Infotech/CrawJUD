from quart import Blueprint

from backend.base import BlueprintNamespace

bots = Blueprint("bots", __name__, url_prefix="/bot")
auth = Blueprint("auth", __name__, url_prefix="/auth")
admin = Blueprint("admin", __name__, url_prefix="/admin")
upload = Blueprint("upload", __name__, url_prefix="/upload")

botNS = BlueprintNamespace("/bot")  # noqa: N816
adminNS = BlueprintNamespace("/admin")  # noqa: N816
fileNS = BlueprintNamespace("/files")  # noqa: N816
