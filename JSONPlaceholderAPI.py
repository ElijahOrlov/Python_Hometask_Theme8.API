"""
Задание 1. Получение данных из публичного API
1. Выберите публичный API. Например, JSONPlaceholder.
2. Напишите скрипт, который:
 отправляет GET-запрос к /posts,
 извлекает и выводит заголовки и тела первых 5 постов.
"""
# https://jsonplaceholder.typicode.com/

import requests
from starlette import status


def get_posts(count: int = 1) -> None:
    """
    Вывод заданного количества списка постов с заголовком
    (https://jsonplaceholder.typicode.com/)
    :param count: количество постов для вывода
    """
    url = f'https://jsonplaceholder.typicode.com/posts'
    try:
        response = requests.get(url)
        response.raise_for_status()
        posts = response.json()

        if len(posts) < count:
            count = len(posts)
        for index, post in enumerate(posts[:count]):
            num = index + 1
            print(f"№{num}\nTitle: {post['title']}\nBody: {post['body']}", end=f"{'\n' * 2 if num < count else ''}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Ошибка запроса: {err}")


get_posts(5)
