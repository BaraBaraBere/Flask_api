import mysql.connector
from app import config


def get_sorted_user_posts_by_user_id(user_id, type_of_sort):
    try:
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )

        cursor = conn.cursor(dictionary=True)

        update_query = f"SELECT id, author_id, text FROM wall WHERE author_id = %s ORDER BY reactions_to_post {type_of_sort}"
        cursor.execute(update_query, (user_id,))

        data = cursor.fetchall()

        for row in data:
            row["reactions"] = get_reactions_by_post_id(row["id"])

        cursor.close()
        conn.close()
        return data
    except mysql.connector.Error:
        return None


def get_author_id_by_post_id(post_id):
    try:
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )

        cursor = conn.cursor()

        update_query = "SELECT author_id FROM wall WHERE id = %s"
        cursor.execute(update_query, (post_id,))
        author_id = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return author_id[0]
    except mysql.connector.Error:
        return None


def add_reacted_stat_to_author_and_post(author_id, post_id):
    try:
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )

        cursor = conn.cursor()

        update_user_statistics = (
            "UPDATE users SET total_reactions = total_reactions + 1 WHERE id = %s"
        )
        update_post_statistics = (
            "UPDATE wall SET reactions_to_post = reactions_to_post + 1 WHERE id = %s"
        )

        cursor.execute(update_user_statistics, (author_id,))
        cursor.execute(update_post_statistics, (post_id,))
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error:
        return None


def check_post_exists(post_id):
    try:
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )

        cursor = conn.cursor(dictionary=True)

        selection_query = "SELECT * FROM wall WHERE id = %s"
        cursor.execute(selection_query, (post_id,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return True if data else False
    except mysql.connector.Error:
        return None


def add_reaction_to_post_by_post_id(post_id, reaction):
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
        insert_query = "INSERT INTO reactions (post_id, reaction) VALUES (%s, %s)"

        # Добавление в базу данных
        cursor.execute(insert_query, (post_id, reaction))
        conn.commit()
        # Закрытие базы данных
        cursor.close()
        conn.close()

        user_id = get_author_id_by_post_id(post_id)

        return add_reacted_stat_to_author_and_post(user_id, post_id)
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


def get_post_by_post_id(post_id):
    try:
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )

        cursor = conn.cursor(dictionary=True)

        selection_query = "SELECT id, author_id, text FROM wall WHERE id = %s"
        cursor.execute(selection_query, (post_id,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data
    except mysql.connector.Error:
        return None


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
        select_data = "SELECT id, author_id, text FROM wall WHERE author_id = %s AND text = %s ORDER BY id DESC LIMIT 1"
        cursor.execute(select_data, (author_id, text))
        data = cursor.fetchone()
        # Закрытие базы данных
        cursor.close()
        conn.close()
        return data
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


def add_post(author_id, text, reactions_to_post=0):
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
        insert_query = (
            "INSERT INTO wall (author_id, text, reactions_to_post) VALUES (%s, %s, %s)"
        )

        # Добавление в базу данных
        cursor.execute(insert_query, (author_id, text, reactions_to_post))
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
