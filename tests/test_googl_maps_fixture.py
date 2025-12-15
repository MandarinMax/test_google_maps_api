from utils.api import GoogleMepsApi

def test_get_place(googl_create_place):
    #print(f"\n[Test] Выполняем PUT для place_id = {googl_create_place.place_id}")
    response = GoogleMepsApi.put_new_place(googl_create_place)
    print(f"[Test] PUT завершен. Status code: {response.status_code}")
    assert response.status_code == 200
