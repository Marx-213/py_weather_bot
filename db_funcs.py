import sqlite3
import logging
from typing import Any, List, Tuple

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)


def db_user_save(message: Any) -> None:
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER)''')
    connect.commit()
    user_id = [message]
    logging.info(user_id)
    cursor.execute(f'SELECT id FROM users WHERE id = {message}')
    data = cursor.fetchone()
    logging.info(data)
    if data is None:
        cursor.execute('INSERT INTO users VALUES (?);', user_id)
        connect.commit()


def select_all_users_id() -> List[Tuple[str]]:
    id_list = []
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    result = cursor.execute('SELECT * FROM users')
    for value in result:
        id_list.append(value)
    logging.info(id_list)
    return id_list
