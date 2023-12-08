from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Cart, Item
from ..products.models import Product, ProductCategory
from ..users.models import User


class CartsEndpointsAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.admin_user = User.objects.create_superuser(email="admin@email.com", password="pass")
        self.admin_token = RefreshToken.for_user(self.admin_user)

        self.user = User.objects.create(first_name="Mark", last_name="Johns", email="mark@email.com", password="mark1")
        self.token = RefreshToken.for_user(self.user)

        self.product_category = ProductCategory.objects.create(name="Asdjhfds")
        self.product = Product.objects.create(name="jsdhgjd", price=230.5, category=self.product_category)

        self.cart = Cart.objects.create(user=self.user)

    def test_add_to_cart_action(self):
        data = {"quantity": 2}

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.post(f'/products/{self.product.pk}/add_to_cart/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "success")

    def test_list_carts(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')
        response = self.client.get("/carts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_cart(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.get(f"/carts/{self.cart.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)

    def test_make_payment_action(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        data = {"user": self.user, "street": "Street", "city": "Tokyo", "zip_code": 34250, "phone": "065 23 45 123"}
        response = self.client.post(f"/carts/{self.cart.pk}/make_payment/", data)
        self.assertTrue(response.data)

    def test_delete_cart(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.delete(f"/carts/{self.cart.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
