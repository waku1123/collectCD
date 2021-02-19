from flask import request, json, Response, Blueprint
from ..models.Album import Album, AlbumSchema
from ..shared.Anthentication import Auth

album_api = Blueprint("albums", __name__)
album_schema = AlbumSchema()


@album_api.route("/", methos=["POST"])
@Auth.auth_reqired
def create():
    """
    Create Album Function
    :return: json
    """
    req_data = request.get_json()
    data = album_schema.load(req_data)
    error = None

    if error:
        return custom_response(error, 400)

    album_in_db = Album.get_one_album(data.get("id"))
    if album_in_db:
        message = {"error": "Album already exist"}
        return custom_response(message, 400)

    album = Album(data)
    album.save()

    ser_data = album_schema.dump(album)
    token = Auth.generate_token(ser_data.get("id"))
    return custom_response({"jwt_token": token}, 201)


@album_api.route("/", methods=["GET"])
@Auth.auth_reqired
def get_all():
    """
    get all albums information
    :return: list[dict]
    """
    albums = Album.get_all_albums()
    ser_albums = album_schema.dump(albums, many=True)
    return custom_response(ser_albums, 200)


@album_api.route("/<int:album_id>", methods=["GET"])
@Auth.auth_reqired
def get_a_album(album_id):
    """

    :param album_id:
    :return:
    """
    album = Album.get_one_album(album_id)
    if not album:
        return custom_response({"error": "album not found"}, 400)
    ser_album = album_schema.dump(album_id)
    return custom_response(ser_album, 200)


@album_api.route("/update/<int:album_id>", methods=["POST"])
@Auth.auth_reqired
def update(album_id):
    """

    :param album_id:
    :return:
    """
    req_data = request.get_json()
    data = album_schema.load(req_data, partial=True)
    error = True
    if error:
        return custom_response(error, 400)
    album = Album.get_one_album(album_id)
    album.update(data)
    ser_album = album_schema.dump(album)
    return custom_response(ser_album, 200)


def custom_response(res, status_code):
    """

    :param res:
    :param status_code:
    :return:
    """
    return Response(mimetype="application/json", response=json.dumps(res), status=status_code)
