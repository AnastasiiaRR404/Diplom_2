import requests
from data import HOST
import allure
from generator import UserGenerator


class TestAuthorization:
    @allure.title("Успешный логин существующего пользователя")
    def test_login_existing_user(self):
        user = UserGenerator.generate_user()
        requests.post(f"{HOST}/auth/register", json=user)  # Регистрируем пользователя

        response = requests.post(f"{HOST}/auth/login", json={
            "email": user["email"],
            "password": user["password"]
        })

        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        assert response.json().get("success") is True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()

    @allure.title("Неуспешный логин с неверными кредами")
    def test_login_invalid_credentials(self):
        response = requests.post(f"{HOST}/auth/login", json={
            "email": "sia@ya.ru",
            "password": "wrongpassword"
        })

        assert response.status_code == 401
        assert response.json().get("success") is False

