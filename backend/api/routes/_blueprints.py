from quart import Blueprint

bots = Blueprint("bots", __name__, url_prefix="/bot")
auth = Blueprint("auth", __name__, url_prefix="/auth")
admin = Blueprint("admin", __name__, url_prefix="/admin")
upload = Blueprint("upload", __name__, url_prefix="/upload")
