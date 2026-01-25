import pytest

# #import db_connector
#
# @pytest.fixture(scope='session')
# def db_connection():
#     # ---SETUP---
#     # #Этот код выполнится один раз в начале всего запуска
#     print('\nУстанвока соединения с БД...')
#     connection = db_connector.connect('test_db_host')
#
#     yield connection
#
#     #---TEARDOWN---
#     #Этот код выполнится один раз в конце всего запуска
#     print('\nЗакрываем соединения с БД...')
#     connection.close()

# Для примера создадим простой класс пользователя
class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def is_admin(self):
        return self.role == "admin"

@pytest.fixture
def admin_user():
    """Фикстура, создающая объект пользователя с правами админа."""
    print("\n[conftest] Создание admin_user")
    return User(name="Admin", role="admin")