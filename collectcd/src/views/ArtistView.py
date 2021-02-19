from flask import request, json, Response, Blueprint, g
from ..models.Artist import Artist, ArtistSchema
from ..shared.Anthentication import Auth

artist_api = Blueprint("artists", __name__)
artist_schema = ArtistSchema()


@artist_api.route("/", methods=["POST"])
@Auth.auth_reqired
def create():
    """
    Create Artist Function
    :return: json
    """
    req_data = request.get_json()
    data = artist_schema.load(req_data)
    error = None

    if error:
        return custom_response(error, 400)

    artist_in_db = Artist.get_one_artist(data.get("id"))
    if artist_in_db:
        message = {"error": "User already exist, please supply another email address"}
        return custom_response(message, 400)

    artist = Artist(data)
    artist.save()

    ser_data = artist_schema.dump(artist)
    token = Auth.generate_token(ser_data.get("id"))
    return custom_response({"jwt_token": token}, 201)


@artist_api.route("/", methods=["GET"])
@Auth.auth_reqired
def get_all():
    """
    get all artists information
    :return: list[dict]
    """
    artists = Artist.get_all_artists()
    ser_artists = artist_schema.dump(artists, many=True)
    return custom_response(ser_artists, 200)


@artist_api.route("/<int:artist_id>", methods=["GET"])
@Auth.auth_reqired
def get_a_artist(artist_id):
    """
    get a single artist information
    :param artist_id:
    :return:
    """
    artist = Artist.get_one_artist(artist_id)
    if not artist:
        return custom_response({"error": "artist not found"}, 400)
    ser_artist = artist_schema.dump(artist)
    return custom_response(ser_artist, 200)


@artist_api.route("/update/<int:artist_id>", methods=["POST"])
@Auth.auth_reqired
def update(artist_id):
    """
    update single artist information
    :param artist_id:
    :return: json
    """
    req_data = request.get_json()
    data = artist_schema.load(req_data, partial=True)
    error = None
    if error:
        return custom_response(error, 400)
    artist = Artist.get_one_artist(artist_id)
    artist.update(data)
    ser_artist = artist_schema.dump(artist)
    return custom_response(ser_artist, 200)


def custom_response(res, status_code):
    """
    Custom Response Function
    :param res:
    :param status_code:
    :return:
    """
    return Response(
        mimetype="application/json", response=json.dumps(res), status=status_code
    )
