import requests


def get_user_full_name(user_id):
    """
    Получает данные пользователя с внешнего API
    и возвращает его полное имя.
    """
    # Внешняя зависимость, которую мы хотим "обмануть"
    response = requests.get(f"https://reqres.in/api/users/{user_id}")

    # Эта строчка вызовет ошибку, если API вернет 404, 500 и т.д.
    response.raise_for_status()

    user_data = response.json()["data"]

    # Логика, которую мы на самом деле хотим протестировать
    first_name = user_data["first_name"]
    last_name = user_data["last_name"]

    return f"{first_name} {last_name}"