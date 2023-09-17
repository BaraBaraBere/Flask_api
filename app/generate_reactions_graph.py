import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from app import usage_database
import time


def generate_reactions_graph():
    users_data = usage_database.get_users_name()
    reactions_data = usage_database.get_users_reactions()
    if not users_data or not reactions_data:
        return None

    file_name = f'plot_{time.thread_time_ns()}.png'
    file_path = f'app/'+file_name
    users = np.array(users_data)
    reactions = np.array(reactions_data)

    plt.bar(users, reactions)

    plt.title("Popularity of user posts")
    plt.xlabel("Users")
    plt.ylabel("Reactions")
    plt.yticks(ticks=np.arange(max(reactions) + 1))

    plt.savefig(file_path)
    return file_name
