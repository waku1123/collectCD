from flask import Flask
from .config import app_config
from .models import db, bcrypt
from .views.UserView import user_api as user_blueprint
from .views.ArtistView import artist_api as artist_blueprint


def create_app(env_name: str) -> Flask:
    """
    Create app
    :param env_name:
    :return:
    """

    app: Flask = Flask(__name__)
    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)
    db.init_app(app)

    app.register_blueprint(user_blueprint, url_prefix="/api/v1/users/")
    app.register_blueprint(artist_blueprint, url_prefix="/api/v1/artists/")

    @app.route("/", methods=["GET"])
    def index():
        """
        example endpoint
        :return:
        """
        return "Congratulations! Your first endpoint is workin"

    return app
