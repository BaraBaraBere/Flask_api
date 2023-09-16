import mysql.connector
from app import config


def get_reactions_by_post_id(post_id):
    try:
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )
        cursor = conn.cursor()

        # SQL-запрос для поиска пользователя по имени и извлечения его id
        select_query = "SELECT reaction FROM reactions WHERE post_id = %s"
        cursor.execute(select_query, (post_id,))
        id_reactions = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return id_reactions
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None



def get_post_by_info(author_id, text):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )
        # Создание курсора
        cursor = conn.cursor(dictionary=True)
        # Поиск пользователя в системе
        select_data = "SELECT * FROM wall WHERE author_id = %s AND text = %s ORDER BY id DESC LIMIT 1"
        cursor.execute(select_data, (author_id, text))
        data = cursor.fetchone()
        # Закрытие базы данных
        cursor.close()
        conn.close()
        return data
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None



def add_post(author_id, text):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )
        # Создание курсора
        cursor = conn.cursor(dictionary=True)

        # Добавление шаблона для данных
        insert_query = "INSERT INTO wall (author_id, text) VALUES (%s, %s)"

        # Добавление в базу данных
        cursor.execute(insert_query, (author_id, text))
        conn.commit()

        # Сбор данных о пользователе в словарь
        data = get_post_by_info(author_id, text)
        # Данные о реакциях на пост
        reactions = get_reactions_by_post_id(data["id"])
        # Закрытие базы данных

        # Добавление данных о постах пользователя
        data["reactions"] = reactions if reactions else []
        cursor.close()
        conn.close()
        return data
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


def get_user_by_id(user_id):
    try:
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )

        cursor = conn.cursor(dictionary=True)

        selection_query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(selection_query, (user_id,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data
    except mysql.connector.Error:
        return None



def get_posts_id_by_user_id(user_id):
    try:
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )
        cursor = conn.cursor()
        # SQL-запрос для поиска пользователя по имени и извлечения его id
        select_query = "SELECT id FROM wall WHERE author_id = %s"
        cursor.execute(select_query, (user_id,))
        id_posts = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return id_posts

    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


def get_user_by_info(first_name, last_name, email):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )
        # Создание курсора
        cursor = conn.cursor(dictionary=True)
        # Поиск пользователя в системе
        select_data = "SELECT * FROM users WHERE first_name = %s AND last_name = %s AND email = %s"
        cursor.execute(select_data, (first_name, last_name, email))
        data = cursor.fetchone()
        # Закрытие базы данных
        cursor.close()
        conn.close()

        return data
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


def add_user(first_name, last_name, email, total_reactions=0):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )
        # Создание курсора
        cursor = conn.cursor(dictionary=True)
        # Обработка случая если пользователь уже существует
        data = get_user_by_info(first_name, last_name, email)

        if data:
            return {"message": "The user has already been created"}
        # Добавление шаблона для данных
        insert_query = "INSERT IGNORE INTO users (first_name, last_name, email, total_reactions) VALUES (%s, %s, %s, %s)"
        # Добавление в базу данных
        cursor.execute(insert_query, (first_name, last_name, email, total_reactions))
        conn.commit()
        # Сбор данных о пользователе в словарь
        data = get_user_by_info(first_name, last_name, email)
        # Данные о постах пользователя
        posts = get_posts_id_by_user_id(data["id"])

        # Добавление данных о постах пользователя
        data["posts"] = posts if posts else []
        cursor.close()
        conn.close()
        return data
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


