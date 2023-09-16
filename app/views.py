from app import app
from flask import request, jsonify, Response
import json
from http import HTTPStatus
from app import usage_database
from validate_email import validate_email


@app.route("/")
def index():
    return "<h1>Hello World</h1>"


@app.post("/users/create")
def user_create():
    try:
        # Распаковка json
        data = request.get_json()
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]

        # Если email неправильный вызов ошибки
        if not validate_email(email):
            return Response(
                json.dumps({"message": "incorrect email"}),
                HTTPStatus.BAD_REQUEST,
                mimetype="aplication/json",
            )

        # Добавление пользователя в базу данных
        data_user = usage_database.add_user(
            first_name,
            last_name,
            email,
        )
        # Если произошла ошибка с базой данных и вернулось None - оповещение об ошибке
        if not data_user:
            return Response(
                json.dumps({"message": "Fail to connect database"}),
                HTTPStatus.INTERNAL_SERVER_ERROR,
                mimetype="aplication/json",
            )
        # Обработка случая если польователь уже зарегистрировн
        elif (
            "message" in data_user.keys()
            and data_user["message"] == "The user has already been created"
        ):
            return Response(
                json.dumps(data_user),
                HTTPStatus.CONFLICT,
                mimetype="aplication/json",
            )

        # Если пользователь новый ответ в виде json
        responce = Response(
            json.dumps(data_user),
            HTTPStatus.CREATED,
            mimetype="aplication/json",
        )
        return responce
    except KeyError:
        return jsonify({"message": "Icorrect data"}), 400
    except Exception as err:
        return str(err), 404


@app.get("/users/<int:user_id>")
def get_user(user_id):
    try:
        data_user = usage_database.get_user_by_id(user_id)
        if not data_user:
            return Response(
                json.dumps({"message": "User is not found"}),
                HTTPStatus.NOT_FOUND,
                mimetype="aplication/json",
            )
        data_posts = usage_database.get_posts_id_by_user_id(user_id)
        data_user["posts"] = data_posts

        request = Response(
            json.dumps(data_user),
            HTTPStatus.OK,
            mimetype="aplication/json",
        )
        return request

    except Exception as err:
        return str(err), 404


@app.post("/posts/create")
def create_post():
    try:
        data_post = request.get_json()
        autor_id = data_post["author_id"]
        text = data_post["text"]

        data_created_post = usage_database.add_post(autor_id, text)
        # Если произошла ошибка с базой данных и вернулось None - оповещение об ошибке
        if not data_created_post:
            return Response(
                json.dumps({"message": "Fail to connect database"}),
                HTTPStatus.INTERNAL_SERVER_ERROR,
                mimetype="aplication/json",
            )
        responce = Response(
            json.dumps(data_created_post),
            HTTPStatus.CREATED,
            mimetype="aplication/json",
        )
        return responce

    except KeyError:
        return Response(
            json.dumps({"message": "Icorrect data"}),
            HTTPStatus.BAD_REQUEST,
            mimetype="aplication/json",
        )
    except Exception as err:
        return str(err), 404


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    try:
        data = usage_database.get_post_by_post_id(post_id)
        if not data:
            return Response(
                json.dumps({"message": "User is not found"}),
                HTTPStatus.NOT_FOUND,
                mimetype="aplication/json",
            )
        data["reactions"] = usage_database.get_reactions_by_post_id(data["id"])
        request = Response(
            json.dumps(data),
            HTTPStatus.OK,
            mimetype="aplication/json",
        )
        return request

    except KeyError:
        return Response(
            json.dumps({"message": "Icorrect data"}),
            HTTPStatus.BAD_REQUEST,
            mimetype="aplication/json",
        )
    except Exception as err:
        return str(err), 404