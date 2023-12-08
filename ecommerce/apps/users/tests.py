from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import AddressSerializer, UserSerializer


class UsersEndpointsAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.admin_user = User.objects.create_superuser(email="admin@email.com", password="testpass")
        self.admin_token = RefreshToken.for_user(self.admin_user)

        self.user = User.objects.create(first_name="Mark", last_name="Johns", email="mark@email.com", password="mark1")
        self.token = RefreshToken.for_user(self.user)

        self.other_user = User.objects.create(email="other@email.com", password="ksjdjd")
        self.other_user_token = RefreshToken.for_user(self.other_user)

    def test_list_users(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token.access_token}')
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_users_without_auth(self):
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_without_auth(self):
        response = self.client.get(f"/users/{self.user.pk}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.get(f"/users/{self.user.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "mark@email.com")

    def test_register_user(self):
        data = {"first_name": "Mr", "last_name": "Dr", "email": "mr@email.com", "password": "sdxpf"}
        response = self.client.post("/users/register_user/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], data["email"])

    def test_patch_user(self):
        new_data = {"first_name": "Rdr"}

        response = self.client.patch(f"/users/{self.user.pk}/", new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.other_user_token.access_token}')
        response = self.client.patch(f"/users/{self.user.pk}/", new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.patch(f'/users/{self.user.pk}/', new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], new_data["first_name"])

    def test_delete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.other_user_token.access_token}')
        response = self.client.delete(f'/users/{self.user.pk}/')
        self.assertEqual(response.status_code, 403)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.delete(f'/users/{self.user.pk}/')
        self.assertEqual(response.status_code, 204)


class SerializersAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="user@email.com", password="skdjdj")

        self.new_user_data = {"email": "user@email.com", "password": "dsjds"}
        data = {"user": self.user, "street": "Street", "city": "Tokyo", "zip_code": "79000", "phone": "064 34 56 789"}
        self.address_data = data

    def test_create_user_with_existing_email(self):
        serializer = UserSerializer(data=self.new_user_data)
        self.assertFalse(serializer.is_valid())

    def test_address_serializer(self):
        serializer = AddressSerializer(data=self.address_data)
        self.assertTrue(serializer.is_valid())
