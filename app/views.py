from app import app
from flask import request, jsonify, Response, send_file
import json
from http import HTTPStatus
from app import usage_database
from validate_email import validate_email
from app import generate_reactions_graph


@app.route("/")
def index():
    return "<h1>Hello World</h1>"


# Создание пользователя
@app.post("/users/create")
def user_create():
    try:
        # Распаковка json
        data = request.get_json()
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]

        # Если email неправильный возвращение ошибки
        if not validate_email(email):
            return Response(
                json.dumps({"message": "Incorrect email"}),
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

        # Если пользователь новый - ответ в формате json
        responce = Response(
            json.dumps(data_user),
            HTTPStatus.CREATED,
            mimetype="aplication/json",
        )
        return responce
    # Обработка ошибки если в json нет нужных ключей
    except KeyError:
        return jsonify({"message": "Icorrect data"}), 400
    # Обработка общей ошибки
    except Exception as err:
        return str(err), 404


# Получение информации о пользователе по user_id
@app.get("/users/<int:user_id>")
def get_user(user_id):
    try:
        # Получение данных о пользователе по user_id
        data_user = usage_database.get_user_by_id(user_id)
        # Если пользователь не найден и вывело None - ответ об отсутствии пользователя
        if not data_user:
            return Response(
                json.dumps({"message": "User is not found"}),
                HTTPStatus.NOT_FOUND,
                mimetype="aplication/json",
            )
        # Получение posts_id созданных пользователем
        data_posts = usage_database.get_posts_id_by_user_id(user_id)
        data_user["posts"] = data_posts

        # Ответ в формате json
        request = Response(
            json.dumps(data_user),
            HTTPStatus.OK,
            mimetype="aplication/json",
        )
        return request

    # Обработка общей ошибки
    except Exception as err:
        return str(err), 404


# Создание поста
@app.post("/posts/create")
def create_post():
    try:
        # Распановка json
        data_post = request.get_json()
        autor_id = data_post["author_id"]
        text = data_post["text"]
        # Создание поста по id_author и добавление туда текста
        data_created_post = usage_database.add_post(autor_id, text)
        # Если произошла ошибка с базой данных и вернулось None - оповещение об ошибке
        if not data_created_post:
            return Response(
                json.dumps({"message": "Fail to connect database"}),
                HTTPStatus.INTERNAL_SERVER_ERROR,
                mimetype="aplication/json",
            )
        # Ответ в формате json
        responce = Response(
            json.dumps(data_created_post),
            HTTPStatus.CREATED,
            mimetype="aplication/json",
        )
        return responce
    # Обработка ошибки если в json нет нужных ключей
    except KeyError:
        return Response(
            json.dumps({"message": "Icorrect data"}),
            HTTPStatus.BAD_REQUEST,
            mimetype="aplication/json",
        )
    # Обработка общей ошибки
    except Exception as err:
        return str(err), 404


# Получение поста по post_id
@app.get("/posts/<int:post_id>")
def get_post(post_id):
    try:
        # Получение информации из БД о посте по post_id
        data = usage_database.get_post_by_post_id(post_id)
        # Если при поиске было возвращено None - ответ об отсутствии поста
        if not data:
            return Response(
                json.dumps({"message": "Post is not found"}),
                HTTPStatus.NOT_FOUND,
                mimetype="aplication/json",
            )
        # Добавление реакций в виде списка в data о посте
        data["reactions"] = usage_database.get_reactions_by_post_id(data["id"])
        # Ответ в формате json
        responce = Response(
            json.dumps(data),
            HTTPStatus.OK,
            mimetype="aplication/json",
        )
        return responce
    # Обработка общей ошибки
    except Exception as err:
        return str(err), 404


# Добавление реакции к посту по post_id
@app.post("/posts/<int:post_id>/reaction")
def add_reaction(post_id):
    try:
        # Распаковка json
        data = request.get_json()
        reaction = data["reaction"]
        # Проверка на существование поста
        if usage_database.check_post_exists(post_id):
            # Если успешно выполнилось -  ответ в фомате json
            if usage_database.add_reaction_to_post_by_post_id(post_id, reaction):
                return Response(
                    json.dumps({"message": "Successfull"}),
                    HTTPStatus.CREATED,
                    mimetype="aplication/json",
                )
            # Если вернулось None - ответ об ошибке
            else:
                return Response(
                    json.dumps({"message": "Fail to connect database"}),
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    mimetype="aplication/json",
                )
        # Ответ об отсутствии поста в БД
        return Response(
            json.dumps({"message": "No such post exists"}),
            HTTPStatus.NOT_FOUND,
            mimetype="aplication/json",
        )
    # Обработка ошибки если в json нет нужных ключей
    except KeyError:
        return Response(
            json.dumps({"message": "Icorrect data"}),
            HTTPStatus.BAD_REQUEST,
            mimetype="aplication/json",
        )
    # Обработка общей ошибки
    except Exception as err:
        return str(err), 404


# Получение отсортированных постов пользователя по user_id
@app.get("/users/<int:user_id>/posts")
def get_sorted_user_posts(user_id):
    try:
        # Распаковка json
        data = request.get_json()
        type_of_sort = data["sort"]
        # Получение отсортированных постов пользователя по user_id и типу сортировки
        posts_data = usage_database.get_sorted_user_posts_by_user_id(
            user_id, type_of_sort.upper()
        )
        # Если вернулось None - значит посты пользователя не найдены - ответ
        if not posts_data:
            return Response(
                json.dumps({"message": "Posts is not found"}),
                HTTPStatus.NOT_FOUND,
                mimetype="aplication/json",
            )
        # Ответ в формате json
        responce = Response(
            json.dumps({"posts": [posts_data]}),
            HTTPStatus.OK,
            mimetype="aplication/json",
        )
        return responce
    # Обработка ошибки если в json нет нужных ключей
    except KeyError:
        return Response(
            json.dumps({"message": "Icorrect data"}),
            HTTPStatus.BAD_REQUEST,
            mimetype="aplication/json",
        )
    # Обработка общей ошибки
    except Exception as err:
        return str(err), 404


# Получение данных о популярности постах пользователях в формате списка или графа
@app.get("/users/leaderboard")
def get_leaderboard():
    try:
        # Распаковка json
        data = request.get_json()
        type = data["type"]
        # Вывод в формате списка
        if type == "list":
            # Получение данных о типе сортировки
            sort = data["sort"]
            # Получение данных о пользователе отсортированных по реакциям
            users_data = usage_database.get_sorted_users(sort.upper())
            # Если не было найдено пользователей и вернулось None
            if not users_data:
                return Response(
                    json.dumps({"message": "Users is not found"}),
                    HTTPStatus.NOT_FOUND,
                    mimetype="aplication/json",
                )
            # Ответ в формате json
            responce = Response(
                json.dumps({"users": [users_data]}),
                HTTPStatus.OK,
                mimetype="aplication/json",
            )
            return responce
        # Вывод в формате графа
        elif type == "graph":
            # Получение имени файла с графом с визуализацией пользователей и их кол-ва реакций на посты
            file_name = generate_reactions_graph.generate_reactions_graph()
            # Если пользователи были найдены - ответ в формате png
            if file_name:
                return send_file(file_name, mimetype="image/png")
            # Если пользователи или посты были не найдены - ответ в формате json
            else:
                return Response(
                    json.dumps({"message": "Users or posts are not found"}),
                    HTTPStatus.NOT_FOUND,
                    mimetype="aplication/json",
                )
        # Если в type нет нужного формата вывода данных - создание ошибки KeyError для дальнейшей обработки
        raise KeyError
    # Обработка ошибки если в json нет нужных ключей или данные не соответствуют требуемым
    except KeyError:
        return Response(
            json.dumps({"message": "Icorrect data"}),
            HTTPStatus.BAD_REQUEST,
            mimetype="aplication/json",
        )
    # Обработка общей ошибки
    except Exception as err:
        return str(err), 404
