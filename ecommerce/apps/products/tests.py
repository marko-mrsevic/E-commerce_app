from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..users.models import User
from .models import Product, ProductCategory


class ProductsEndpointsAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.admin_user = User.objects.create_superuser(email="admin@email.com", password="password")
        self.admin_token = RefreshToken.for_user(self.admin_user)

        self.user = User.objects.create(first_name="Mark", last_name="Johns", email="mark@email.com", password="mark1")
        self.token = RefreshToken.for_user(self.user)

        self.product_category = ProductCategory.objects.create(name="Asdjhfds")
        self.another_product_category = ProductCategory.objects.create(name="dffvdd")
        self.product = Product.objects.create(name="jsdhgjd", price=230.5, category=self.product_category)

    def test_list_products(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_product(self):
        response = self.client.get(f'/products/{self.product.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_patch_product(self):
        new_data = {"price": 400}

        response = self.client.patch(f"/products/{self.product.pk}/", new_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.patch(f"/products/{self.product.pk}/", new_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')
        response = self.client.patch(f'/products/{self.product.pk}/', new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["price"], f'{new_data["price"]:.2f}')

    def test_create_products(self):
        data = {"name": "sdjfds", "price": 340.2, "category": f'{self.another_product_category.name}'}

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')
        response = self.client.post("/products/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_to_cart_action(self):
        data = {"quantity": 1}

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.post(f'/products/{self.product.pk}/add_to_cart/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], "success")

    def test_delete_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.delete(f'/products/{self.product.pk}/')
        self.assertEqual(response.status_code, 403)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')
        response = self.client.delete(f'/products/{self.product.pk}/')
        self.assertEqual(response.status_code, 204)
