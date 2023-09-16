import mysql.connector

# Подключение к пользователю
conn = mysql.connector.connect(host="localhost", user="root", password="A12345678a")

# Создание курсора
cursor = conn.cursor()

# Создание базы данных
cursor.execute("CREATE DATABASE IF NOT EXISTS flask_project_database")

# Выбор базы данных
cursor.execute("USE flask_project_database")

# Создание таблицы для данных о пользователях
create_table_user = """
CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    total_reactions INT
)
"""

# Создание таблицы для данных о постах пользователей
create_table_wall = """
        CREATE TABLE IF NOT EXISTS wall(
            id INT AUTO_INCREMENT PRIMARY KEY,
            author_id INT,
            text TEXT
        )
        """

# Создание таблицы для данных о реакциях на посты
create_table_of_reactions = """
    CREATE TABLE IF NOT EXISTS reactions(
        id INT AUTO_INCREMENT PRIMARY KEY,
        post_id INT,
        reaction TEXT
        )
"""

# Создание таблиц
cursor.execute(create_table_wall)
cursor.execute(create_table_user)
cursor.execute(create_table_of_reactions)

cursor.close()
conn.close()
