"""Методы для проверки ответов наших запросов"""
import json
from tabnanny import check

from requests import Response


class Cheking():


    """Метод ля проверки статус кода запроса"""
    @staticmethod
    def check_status_code(response: Response, status_code):
        assert status_code == response.status_code
        if response.status_code == status_code:
            print("Успешно! Статус код = " + str(response.status_code))
        else:
            print("Провал! Статус код = " + str(response.status_code))


    """Метод для проверки наличия обязательных полей в ответе запроса"""
    @staticmethod
    def check_json_token(response: Response, expected_value):
        token = json.loads(response.text)
        assert  list(token) == expected_value
        print("Все поля присутствуют")

    """Метод для проверки значений обязательных полей в ответе запроса"""
    @staticmethod
    def check_json_value(response: Response, field_name,expected_value):
        check = response.json()
        check_info = check.get(field_name)
        assert check_info == expected_value
        print(f"Значение поля {field_name} верно")

    """Метод для проверки присутствия нужной подстроки в ответе"""

    @staticmethod
    def check_json_search_word_in_value(response: Response, field_name, search_word):
        check = response.json()
        check_info = check.get(field_name)
        if search_word in check_info:
            print(f"Значение поля {field_name} слово {search_word} присутствует")
        else:
            print(f"Значение поля {field_name} слово {search_word} отсутствует")