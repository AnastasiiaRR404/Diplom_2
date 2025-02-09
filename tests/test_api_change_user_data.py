import requests
from data import HOST
import allure

from generator import UserGenerator


class TestUserInfo:
    @allure.title("Успешное получение юзером информации о себе, если он авторизован")
    def test_get_user_info(self):
        user = UserGenerator.generate_user()
        register_response = requests.post(f"{HOST}/auth/register", json=user)
        access_token = register_response.json().get("accessToken")

        response = requests.get(f"{HOST}/auth/user", headers={"Authorization": access_token})

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Успешное изменение юзером информации о себе, если он авторизован")
    def test_update_user_info_with_auth(self):
        user = UserGenerator.generate_user()
        register_response = requests.post(f"{HOST}/auth/register", json=user)
        access_token = register_response.json().get("accessToken")

        updated_data = {"name": "NewName"}
        response = requests.patch(f"{HOST}/auth/user", headers={"Authorization": access_token}, json=updated_data)

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Успешное изменение юзером информации о себе, если он неавторизован")
    def test_update_user_info_without_auth(self):
        updated_data = {"name": "HackerName"}
        response = requests.patch(f"{HOST}/auth/user", json=updated_data)

        assert response.status_code == 401
        assert response.json().get("success") is False