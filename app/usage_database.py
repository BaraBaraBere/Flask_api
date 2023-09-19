import mysql.connector
from app import config


# Получение кол-ва реакций на посты у каждого пользователя из БД
def get_users_reactions():
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )

        # Создаем курсор
        cursor = conn.cursor()

        # Выполняем SQL-запрос для извлечения кол-ва реакций на посты из таблицы users
        query = "SELECT total_reactions FROM users"
        cursor.execute(query)

        # Получаем результаты в список
        data = [row[0] for row in cursor.fetchall()]

        # Закрываем соединение
        cursor.close()
        conn.close()
        # Возвращение списка кол-ва реакций
        return data
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


# Получение имен всех пользователей из БД
def get_users_name():
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )

        # Создаем объект cursor для выполнения SQL-запросов
        cursor = conn.cursor()

        # Выполняем SQL-запрос для извлечения имени и фамилии из таблицы users, объединения их
        query = "SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM users"
        cursor.execute(query)

        # Получаем объединенные имя и фамилию в список
        data = [row[0] for row in cursor.fetchall()]

        # Закрываем соединение
        cursor.close()
        conn.close()
        # Возвращаем список
        return data
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


# Получение списка пользователей с информацией отсортированных по кол-ву реакций по типу сортировки
def get_sorted_users(type_of_sort):
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
        # SQL-запрос для сохранения пользователей из таблицы users выборкой по определенной сортировке
        update_query = f"SELECT * FROM users ORDER BY total_reactions {type_of_sort}"
        cursor.execute(update_query)
        # Сохранение пользователей в формате словаря
        data = cursor.fetchall()

        # Закрываем соединение
        cursor.close()
        conn.close()
        # Возвращение данных о пользователях
        return data
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


# Получение сортированного списка постов пользователя из БД по user_id и типу сортировки
def get_sorted_user_posts_by_user_id(user_id, type_of_sort):
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
        # SQL-запрос для поиска постов из таблицы wall по author_id с выборкой в определенной сортировкой
        update_query = f"SELECT id, author_id, text FROM wall WHERE author_id = %s ORDER BY reactions_to_post {type_of_sort}"
        cursor.execute(update_query, (user_id,))
        # Сохранение постов в формате словоря
        data = cursor.fetchall()
        # Добавление к каждому посту информации о реакциях
        for row in data:
            row["reactions"] = get_reactions_by_post_id(row["id"])

        # Закрываем соединение
        cursor.close()
        conn.close()
        # Возвращение списка с информацией о постах
        return data
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


# Получение author_id из БД по post_id
def get_author_id_by_post_id(post_id):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )
        # Создание курсора
        cursor = conn.cursor()
        # SQL-запрос для поиска author_id из таблицы wall по post_id
        update_query = "SELECT author_id FROM wall WHERE id = %s"
        cursor.execute(update_query, (post_id,))
        # Сохранение данных в список
        author_id = [row[0] for row in cursor.fetchall()]

        # Закрываем соединение
        cursor.close()
        conn.close()
        # Возвращение author_id из списка(Единственный элемент в массиве)
        return author_id[0]
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


# Добавление статистики реакций в БД по author_id и post_id
def add_reacted_stat_to_author_and_post(author_id, post_id):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )
        # Создание курсора
        cursor = conn.cursor()
        # Увеличение кол-ва реакций в таблицу users по author_id
        # Увеличения кол-ва реакций в таблицу wall по post_id
        update_user_statistics = (
            "UPDATE users SET total_reactions = total_reactions + 1 WHERE id = %s"
        )
        update_post_statistics = (
            "UPDATE wall SET reactions_to_post = reactions_to_post + 1 WHERE id = %s"
        )
        cursor.execute(update_user_statistics, (author_id,))
        cursor.execute(update_post_statistics, (post_id,))
        # Сохранение изменений
        conn.commit()

        # Закрываем соединение
        cursor.close()
        conn.close()
        # Возвращение True, если все выполнено без ошибок
        return True
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


# Проверка на существование поста БД по post_id
def check_post_exists(post_id):
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
        # SQL-запрос для поиска поста из таблицы wall по post_id
        selection_query = "SELECT * FROM wall WHERE id = %s"
        cursor.execute(selection_query, (post_id,))
        # Сохранение данных о поста
        data = cursor.fetchone()
        # Закрываем соединение
        cursor.close()
        conn.close()
        # Возвращение True, если в data что-то есть, иначе False
        return True if data else False
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


# Добавление реакции на пост в БД по post_id и реакции
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

        # SQL-запрос для добавление post_if и реакции в таблицу reactions
        insert_query = "INSERT INTO reactions (post_id, reaction) VALUES (%s, %s)"
        cursor.execute(insert_query, (post_id, reaction))
        # Сохранение изменений
        conn.commit()
        # Закрываем соединение
        cursor.close()
        conn.close()
        # Получение author_id по post_id для обновления статистики автора
        user_id = get_author_id_by_post_id(post_id)
        # Вызов функции по добавлению статистики по user_id(author_id) и post_id, для обновления статистики автора поста
        # Вернется True, если статистика обновлена удачно, в противном случае False
        return add_reacted_stat_to_author_and_post(user_id, post_id)
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


# Получение поста из БД по post_id
def get_post_by_post_id(post_id):
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
        # SQL-запрос для поиска поста из таблицы wall по post_id
        selection_query = "SELECT id, author_id, text FROM wall WHERE id = %s"
        cursor.execute(selection_query, (post_id,))
        # Сохранение поста в формате словаря
        data = cursor.fetchone()

        # Закрываем соединение
        cursor.close()
        conn.close()
        # Возвращение словаря с постом
        return data
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


# Получение реакций из БД по post_id
def get_reactions_by_post_id(post_id):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )
        # Создание курсора
        cursor = conn.cursor()

        # SQL-запрос для поиска реакций по post_id из таблицы reactions
        select_query = "SELECT reaction FROM reactions WHERE post_id = %s"
        cursor.execute(select_query, (post_id,))
        # Сохранение реакций на пост в формате списка
        id_reactions = [row[0] for row in cursor.fetchall()]

        # Закрываем соединение
        cursor.close()
        conn.close()
        # Возвращение списка реакций
        return id_reactions
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


# Получение поста из БД по author_id и тексту
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
        # SQl запрос для получения информации поста по author_id и тексту, отсортировано по убыванию id и лимит вывода
        # 1 пост. То есть при наличии одинаковых постов выведет последний добавленный
        select_data = "SELECT id, author_id, text FROM wall WHERE author_id = %s AND text = %s ORDER BY id DESC LIMIT 1"
        cursor.execute(select_data, (author_id, text))
        # Сохранение данных о посте в словарь
        data = cursor.fetchone()

        # Закрытие базы данных
        cursor.close()
        conn.close()
        # Возвращение словаря
        return data
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


# Добавление поста в БД
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

        # SQL запрос для добавления поста в таблицу с постами
        insert_query = (
            "INSERT INTO wall (author_id, text, reactions_to_post) VALUES (%s, %s, %s)"
        )
        cursor.execute(insert_query, (author_id, text, reactions_to_post))
        # Сохранение
        conn.commit()

        # Получение словаря с информацией о посте
        data = get_post_by_info(author_id, text)
        # Получение реакций у поста по post_id
        reactions = get_reactions_by_post_id(data["id"])

        # Добавление данных о реакциях в словарь поста
        data["reactions"] = reactions if reactions else []

        # Закрываем соединение
        cursor.close()
        conn.close()
        # Возвращение словаря
        return data
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


# Получение пользователя из БД по user_id
def get_user_by_id(user_id):
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
        # SQL-запрос для поиска пользователя по id и извлечению его полной информации
        selection_query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(selection_query, (user_id,))
        # Сохранение данных в виде словаря
        data = cursor.fetchone()

        # Закрытие соединения
        cursor.close()
        conn.close()
        # Возврящение данных о пользователе в виде словаря
        return data
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


# Получение id постов пользователей из БД по user_id
def get_posts_id_by_user_id(user_id):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database,
        )
        # Создание курсора
        cursor = conn.cursor()
        # SQL-запрос для поиска пользователя по author_id и извлечения его id его постов
        select_query = "SELECT id FROM wall WHERE author_id = %s"
        cursor.execute(select_query, (user_id,))
        # Сохранение данных в список
        id_posts = [row[0] for row in cursor.fetchall()]

        # Закрытие соединения
        cursor.close()
        conn.close()
        # Возвращение списка id постов
        return id_posts

    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


# Получение информации из БД по полной информации о пользователе(Имя, Фамилия, почта)
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
        # Сохранение найденных данных в виде словаря
        data = cursor.fetchone()

        # Закрытие базы данных
        cursor.close()
        conn.close()
        # Возвращение собранных данных
        return data
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None


# Добавление в БД пользователя по имени, фамилии и почте
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

        # Закрытие соединения
        cursor.close()
        conn.close()
        return data
    # Обработка случая если возникла какая-то ошибка
    except mysql.connector.Error:
        return None
