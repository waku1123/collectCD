import jwt
import os
import datetime
from flask import json, Response, request, g
from ..models.User import User
from functools import wraps


class Auth:
    """
    認証用クラス
    """

    @staticmethod
    def generate_token(user_id):
        """
        user_idをもとにHS256で生成したtokenを返す
        :param user_id:
        :return:
        """
        try:
            payload = {
                "exp": datetime.datetime.now() + datetime.timedelta(days=1),
                "iat": datetime.datetime.now(),
                "sub": user_id,
            }
            return jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), "HS256")
        except Exception as e:
            return Response(
                mimetype="application/json",
                response=json.dumps({"error": "error in generating user token"}),
                status=400,
            )

    @staticmethod
    def decode_token(token):
        """
        Decode Token Method
        :param token:
        :return:
        """
        re = {"data": {}, "error": {}}
        try:
            payload = jwt.decode(jwt=token, key=os.getenv("JWT_SECRET_KEY"), algorithms="HS256")
            re["data"] = {"user_id": payload["sub"]}
            return re
        except jwt.ExpiredSignatureError as e1:
            re["error"] = {"message": "token expired, please login again"}
            return re
        except jwt.InvalidTokenError:
            re["error"] = {"message": "Invalid token, try again with a new token"}
            return re

    @staticmethod
    def auth_reqired(func):
        """
        Auth decorator
        :param func:
        :return:
        """

        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if "api-token" not in request.headers:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(
                        {"error": "Authentication token is not available. please login to get one"}
                    ),
                    status=400,
                )
            token = request.headers.get("api-token")
            data = Auth.decode_token(token=token)
            if data["error"]:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data["error"]),
                    status=400,
                )

            user_id = data["data"]["user_id"]
            check_user = User.get_one_user(user_id)
            if not check_user:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({"error": "user does not exist, invalid token"}),
                    status=400,
                )
            g.user = {"id": user_id}
            return func(*args, **kwargs)

        return decorated_auth
