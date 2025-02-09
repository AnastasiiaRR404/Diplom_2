import pytest
import requests
from data import HOST
from generator import UserGenerator
import allure


@pytest.fixture
def unique_user():
    return UserGenerator.generate_user()


@pytest.fixture
def existing_user():
    user = UserGenerator.generate_user()
    requests.post(f"{HOST}/auth/register", json=user)  # Регистрируем пользователя заранее
    return user

class TestCreateUser:
    @allure.title("Регистрация пользователя")
    def test_create_unique_user(self, unique_user):
        response = requests.post(f"{HOST}/auth/register", json=unique_user)
        assert response.status_code == 200

    @allure.title("Регистрация существующего пользователя")
    def test_create_existing_user(self, existing_user):
        response = requests.post(f"{HOST}/auth/register", json=existing_user)
        assert response.status_code == 403


    @allure.title("Регистрация пользователя с пропущенным полем")
    def test_create_user_missing_field(self):
        incomplete_user = {
            "email": UserGenerator.generate_email(),
            "password": UserGenerator.generate_password()
            # Поле "name" отсутствует
        }
        response = requests.post(f"{HOST}/auth/register", json=incomplete_user)
        assert response.status_code == 403

