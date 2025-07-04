import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
class TestTagAPI:
    def setup_method(self):
        self.client = APIClient()
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(username=self.username, password=self.password)

        response = self.client.post("/api/auth/token/", {
            "username": self.username,
            "password": self.password
        })
        self.access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create_tag(self):
        data = {"name": "Important", "description": "Mes trucs", "color": "#ff0000"}
        response = self.client.post("/api/tags/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Important"

    def test_user_can_only_see_own_tags(self):
        # Créer un tag pour un autre utilisateur
        other_user = User.objects.create_user(username="otheruser", password="otherpass")
        other_client = APIClient()
        token = other_client.post("/api/auth/token/", {
            "username": "otheruser",
            "password": "otherpass"
        }).data["access"]
        other_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        other_client.post("/api/tags/", {
            "name": "Privé", "description": "Ne pas voir", "color": "#000000"
        })

        # Créer un tag pour l'utilisateur courant
        self.client.post("/api/tags/", {
            "name": "Visible", "description": "Mon tag", "color": "#00ff00"
        })

        response = self.client.get("/api/tags/")
        names = [tag["name"] for tag in response.data]
        assert "Visible" in names
        assert "Privé" not in names

    def test_edit_or_delete_others_tag(self):
        # Créer un tag pour un autre utilisateur
        other_user = User.objects.create_user(username="otheruser", password="otherpass")
        other_client = APIClient()
        token = other_client.post("/api/auth/token/", {
            "username": "otheruser",
            "password": "otherpass"
        }).data["access"]
        other_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = other_client.post("/api/tags/", {
            "name": "Secret", "description": "Ne pas toucher", "color": "#123456"
        })
        tag_id = response.data["id"]

        # Essayer de modifier
        update_response = self.client.patch(f"/api/tags/{tag_id}/", {"name": "Hack"})
        assert update_response.status_code == status.HTTP_404_NOT_FOUND

        # Essayer de supprimer
        delete_response = self.client.delete(f"/api/tags/{tag_id}/")
        assert delete_response.status_code == status.HTTP_404_NOT_FOUND
