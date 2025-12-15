import pytest
from utils.api import GoogleMepsApi
from config.config import BASE_URL, API_KEY

@pytest.fixture()
def googl_create_place():
    """
    Fixture:
    1. Создаёт новую локацию
    2. Возвращает place_id
    3. После теста удаляет локацию (teardown)
    """
    print('\n[Fixture] Создаем новую локацию ...')
    create_response = GoogleMepsApi.create_new_place()
    assert create_response.status_code == 200
    place_id = create_response.json()['place_id']
    print(f'[Fixture] Локация создана: place_ad={place_id}')

    yield place_id

    print(f"[Fixture] Удаляем локацию: place_id = {place_id}")
    GoogleMepsApi.delete_new_place(place_id)
    print(f"[Fixture] Локация {place_id} удалена")