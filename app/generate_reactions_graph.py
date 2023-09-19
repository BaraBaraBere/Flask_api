import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from app import usage_database
import time


def generate_reactions_graph():
    # Получение данных о пользователях и их постах
    users_data = usage_database.get_users_name()
    reactions_data = usage_database.get_users_reactions()
    # Если данных нет в таблице - возвращение None
    if not users_data or not reactions_data:
        return None

    # Создание уникального имени файла
    file_name = f"plot_{time.thread_time_ns()}.png"
    # Создание пути к файлу через папку app
    file_path = f"app/" + file_name
    # Создание списков с данными
    users = np.array(users_data)
    reactions = np.array(reactions_data)

    # Отображение в виде столбцов
    plt.bar(users, reactions)

    # Форматирование оформления
    plt.title("Popularity of user posts")
    plt.xlabel("Users", size=9)
    plt.ylabel("Reactions")
    plt.yticks(ticks=np.arange(max(reactions) + 1))
    plt.xticks(rotation=12, size=8)

    # Сохранение картинки
    plt.savefig(file_path)
    # Возвращение имени файла
    return file_name
