from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class UserViewSetTests(APITestCase):

    def setUp(self):
        # Création des utilisateurs
        self.admin = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        self.user1 = User.objects.create_user(username='user1', password='pass123', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='pass123', email='user2@example.com')

        self.register_url = "/api/user/"
        self.token_url = "/api/token/"

    def authenticate(self, username, password):
        response = self.client.post(self.token_url, {
            "username": username, "password": password
        }
                                    )
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # def test_register_user(self):
    #     data = {
    #         "username": "newuser", "email": "newuser@example.com", "password": "pass1234",
    #         "password_confirm": "pass1234"
    #     }
    #     response = self.client.post(self.register_url, data)
    #     print(response.status_code)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_list_users(self):
        self.authenticate("user1", "pass123")
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_users(self):
        self.authenticate("admin", "adminpass")
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_user_can_update_own_profile(self):
    #     self.authenticate("user1", "pass123")
    #     url = f"{self.register_url}{self.user1.id}/"
    #     data = {"email": "updated@example.com"}
    #     response = self.client.patch(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data["email"], "updated@example.com")

    # def test_user_cannot_update_other_profile(self):
    #     self.authenticate("user1", "pass123")
    #     url = f"{self.register_url}{self.user2.id}/"
    #     data = {"email": "hacker@example.com"}
    #     response = self.client.patch(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_users(self):
        self.authenticate("admin", "adminpass")
        url = f"{self.register_url}{self.user1.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_user_cannot_delete_other_users(self):
    #     self.authenticate("user1", "pass123")
    #     url = f"{self.register_url}{self.user2.id}/"
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
