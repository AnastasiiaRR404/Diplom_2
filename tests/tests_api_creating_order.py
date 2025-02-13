import requests
from generator import UserGenerator
from data import HOST
import allure


class TestCreateOrder:

    def get_valid_ingredients(self):
        response = requests.get(f"{HOST}/ingredients")
        assert response.status_code == 200, f"Failed to fetch ingredients: {response.text}"
        return [ingredient["_id"] for ingredient in response.json().get("data", [])]


    def get_access_token(self):
        user = UserGenerator.generate_user()
        response = requests.post(f"{HOST}/auth/register", json=user)
        assert response.status_code == 200, f"Registration failed: {response.text}"
        return response.json().get("accessToken")

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_with_auth(self):
        access_token = self.get_access_token()
        ingredients = self.get_valid_ingredients()

        response = requests.post(
            f"{HOST}/orders",
            headers={"Authorization": access_token},
            json={"ingredients": ingredients[:2]}
        )

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        ingredients = self.get_valid_ingredients()

        response = requests.post(
            f"{HOST}/orders",
            json={"ingredients": ingredients[:2]}
        )

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        access_token = self.get_access_token()

        response = requests.post(
            f"{HOST}/orders",
            headers={"Authorization": access_token},
            json={"ingredients": []}
        )

        assert response.status_code == 400,f"Unexpected status: {response.text}"
        assert response.json().get("message") == "Ingredient ids must be provided"
    @allure.title("Создание заказа с невалидным ингредиентом")
    def test_create_order_with_invalid_ingredient(self):
        access_token = self.get_access_token()
        invalid_ingredient_id = "invalid_id"

        response = requests.post(
            f"{HOST}/orders",
            headers={"Authorization": access_token},
            json={"ingredients": [invalid_ingredient_id]}
        )
        assert response.status_code == 500, f"Unexpected status: {response.text}"
        assert response.json().get("message") == "Internal Server Error", "Expected error message not received"
