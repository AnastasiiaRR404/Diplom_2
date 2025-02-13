import requests
import pytest
from generator import UserGenerator
from data import HOST
import allure

class TestGetUserOrders:
    @allure.title("Получение заказов авторизованным пользователем")
    def test_get_user_orders_authorized(self):
        user = UserGenerator.generate_user()
        register_response = requests.post(f"{HOST}/auth/register", json=user)
        access_token = register_response.json().get("accessToken")

        response = requests.get(
            f"{HOST}/orders",
            headers={"Authorization": access_token}
        )

        orders = response.json()["orders"]
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        assert response.json().get("success") is True
        assert "orders" in response.json()
        assert len(orders) == 0  #проверка что заказа нет

    @allure.title("Получение заказов неавторизованным пользователем")
    def test_get_user_orders_unauthorized(self):
        response = requests.get(f"{HOST}/orders")

        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json().get("message") == "You should be authorised"