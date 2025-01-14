from utils.http_metods import Http_methods
"""Методы для тестирования API гугл карт"""

base_url = "https://rahulshettyacademy.com/"  # базовый урл
key = "?key=qaclick123" #парамтер для всех
#post_resurs = "/maps/api/place/add/json"  # рескрс метода пост

class Google_meps_api():

    """Метод для создания новой локации"""
    @staticmethod
    def create_new_place():
        jsom_for_create_new_place = {
            "location": {
                "lat": -38.383494,
                "lng": 33.427362
            },
            "accuracy": 50,
            "name": "Frontline house",
            "phone_number": "(+91) 983 893 3937",
            "address": "29, side layout, cohen 09",
            "types": [
                "shoe park",
                "shop"
            ],
            "website": "http://google.com",
            "language": "French-IN"
        }

        post_resource = "/maps/api/place/add/json"
        post_url = base_url + post_resource + key
        result_post = Http_methods.post(post_url, jsom_for_create_new_place)
        return result_post

    """Метод для проверки новой локации"""

    @staticmethod
    def get_new_place(place_id):

        get_resource = "/maps/api/place/get/json" # ресур метода гут
        get_url = base_url + get_resource + key + "&place_id=" + place_id
        result_get = Http_methods.get(get_url)
        return result_get

    """Метод для редактирования новой локации"""

    @staticmethod
    def put_new_place(place_id):
        put_resource = "/maps/api/place/update/json"  # ресур метода put
        put_url = base_url + put_resource + key
        json_for_update_new_location = {
            "place_id": place_id,
            "address": "100 Lenina street, RU",
            "key": "qaclick123"
        }
        result_put = Http_methods.put(put_url, json_for_update_new_location)
        return result_put

    """Метод для удаления новой локации"""

    @staticmethod
    def delete_new_place(place_id):
        delete_resource = "/maps/api/place/delete/json"  # ресур метода delete
        delete_url = base_url + delete_resource + key
        json_for_delete_new_location = {
            "place_id": place_id
        }
        result_delete = Http_methods.delete(delete_url, json_for_delete_new_location)
        return result_delete