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
