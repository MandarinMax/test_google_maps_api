import json
import allure
from requests import Response
from utils.chaking import Cheking
from utils.api import GoogleMepsApi


"""Создание изменения и удаления новой локации"""
@allure.epic("Test create place")
class Test_create_pleace():

    @allure.description("Test create, update, delete new place")
    def test_create_new_pleace(self):

        print("Метод POST")
        result_post: Response = GoogleMepsApi.create_new_place()
        check_post = result_post.json()
        place_id = check_post.get("place_id")
        Cheking.check_status_code(result_post, 200)
        # token = json.loads(result_post.text) получить все поля из ответа
        # print(list(token))
        Cheking.check_json_token(result_post, ['status', 'place_id', 'scope', 'reference', 'id'])
        Cheking.check_json_value(result_post, 'status', 'OK')


        print("Метод GET POST")
        result_get: Response = GoogleMepsApi.get_new_place(place_id)
        Cheking.check_status_code(result_get, 200)
        # token = json.loads(result_get.text)
        # print(list(token)) #['location', 'accuracy', 'name', 'phone_number', 'address', 'types', 'website', 'language']
        Cheking.check_json_token(result_get, ['location', 'accuracy', 'name', 'phone_number', 'address', 'types', 'website', 'language'])
        Cheking.check_json_value(result_get, 'address', '29, side layout, cohen 09')


        print("Метод PUT")
        result_put: Response = GoogleMepsApi.put_new_place(place_id)
        Cheking.check_status_code(result_put, 200)
        Cheking.check_json_token(result_put, ["msg"])
        Cheking.check_json_value(result_put, 'msg', 'Address successfully updated')


        print("Метод GET PUT")
        result_get: Response = GoogleMepsApi.get_new_place(place_id)
        Cheking.check_status_code(result_get, 200)
        Cheking.check_json_token(result_get,
                                 ['location', 'accuracy', 'name', 'phone_number', 'address', 'types', 'website',
                                  'language'])
        Cheking.check_json_value(result_get, 'address', '100 Lenina street, RU')


        print("Метод DELETE")
        result_delete: Response = GoogleMepsApi.delete_new_place(place_id)
        Cheking.check_status_code(result_delete, 200)
        Cheking.check_json_token(result_delete, ["status"])
        Cheking.check_json_value(result_delete, 'status', 'OK')


        print("Метод GET DELETE")
        result_get: Response = GoogleMepsApi.get_new_place(place_id)
        Cheking.check_status_code(result_get, 404)
        Cheking.check_json_token(result_get,['msg'])
        Cheking.check_json_value(result_get, 'msg', "Get operation failed, looks like place_id  doesn't exists")
        Cheking.check_json_search_word_in_value(result_get, 'msg', "failed")

        print("Тестирование создания, изменения и удаления новой локации прошло успешно")