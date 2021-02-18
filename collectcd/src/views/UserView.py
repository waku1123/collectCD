from flask import request, json, Response, Blueprint, g
from ..models.User import User, UserSchema
from ..shared.Anthentication import Auth

user_api = Blueprint("users", __name__)
user_schema = UserSchema()


@user_api.route("/", methods=["POST"])
def create():
    """
    Create User Function
    :return:
    """
    req_data = request.get_json()
    data = user_schema.load(req_data)
    error = None

    if error:
        return custom_response(error, 400)

    user_in_db = User.get_user_by_email(data.get("email"))
    if user_in_db:
        message = {"error": "User already exist."}
        return custom_response(message, 400)

    user = User(data)
    user.save()

    ser_data = user_schema.dump(user)
    token = Auth.generate_token(ser_data.get("id"))
    return custom_response({"jwt_token": token}, 201)


@user_api.route("/login", methods=["POST"])
def login():
    """
    user login
    :return: json {token : generated token}
    """
    req_data = request.get_json()
    data = user_schema.load(req_data, partial=True)
    error = None

    if error:
        return custom_response(error, 400)

    if not data.get("email") or not data.get("password"):
        return custom_response({"error": "you need email and password to sign in"}, 400)

    user = User.get_user_by_email(data.get("email"))

    if not user:
        return custom_response({"error": "invalid credentials"}, 400)

    if not user.check_hash(data.get("password")):
        return custom_response({"error": "invalid credentials"}, 400)
    # ser_data = user_schema.dump(user).data
    ser_data = user_schema.dump(user)
    token = Auth.generate_token(ser_data.get("id"))
    return custom_response({"jwt_token": token}, 200)


@user_api.route("/", methods=["GET"])
@Auth.auth_reqired
def get_all():
    """
    get all users information
    :return: list[dict]
    """
    users = User.get_all_users()
    ser_users = user_schema.dump(users, many=True)
    return custom_response(ser_users, 200)


@user_api.route("/<int:user_id>", methods=["GET"])
@Auth.auth_reqired
def get_a_user(user_id):
    """
    get a single user information
    :param user_id:
    :return:
    """
    user = User.get_one_user(user_id)
    if not user:
        return custom_response({"error": "user not found"}, 400)
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)


@user_api.route("/me", methods=["PUT"])
@Auth.auth_reqired
def update():
    """
    Update me
    :return:
    """
    req_data = request.get_json()
    data = user_schema.load(req_data, partial=True)
    error = None
    if error:
        return custom_response(error, 400)

    user = User.get_one_user(g.user.get("id"))
    user.update(data)
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)


@user_api.route("/me", methods=["DELETE"])
@Auth.auth_reqired
def delete():
    """
    delete a user
    :return:
    """
    user = User.get_one_user(g.user.get("id"))
    user.delete()
    return custom_response({"message": "delete"}, 204)


@user_api.route("/me", methods=["GET"])
@Auth.auth_reqired
def get_me():
    """
    get my user information
    :return:
    """
    user = User.get_one_user(g.user.get("id"))
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)


def custom_response(res, status_code):
    """
    Custom Response Function
    :param res:
    :param status_code:
    :return:
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code,
    )
