import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCategoryAPI:
    def setup_method(self):
        self.client = APIClient()
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(username=self.username, password=self.password)

        response = self.client.post("/api/auth/token/", {
            "username": self.username, "password": self.password
        }
                                    )
        self.access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create_category(self):
        data = {"name": "Utilitaire", "description": "Catégorie pour les outils"}
        response = self.client.post("/api/categories/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Utilitaire"

    def test_user_can_only_see_own_categories(self):
        # Créer une catégorie pour un autre utilisateur
        other_user = User.objects.create_user(username="otheruser", password="otherpass")
        other_client = APIClient()
        token = other_client.post("/api/auth/token/", {
            "username": "otheruser", "password": "otherpass"
        }
                                  ).data["access"]
        other_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        other_client.post("/api/categories/", {
            "name": "Secret", "description": "Ne pas afficher"
        }
                          )

        # Créer une catégorie pour le user courant
        self.client.post("/api/categories/", {
            "name": "Visible", "description": "Cat perso"
        }
                         )

        response = self.client.get("/api/categories/")
        names = [c["name"] for c in response.data]
        assert "Visible" in names
        assert "Secret" not in names

    def test_forbidden_access_returns_404(self):
        # Créer une catégorie pour un autre utilisateur
        other_user = User.objects.create_user(username="otheruser", password="otherpass")
        other_client = APIClient()
        token = other_client.post("/api/auth/token/", {
            "username": "otheruser", "password": "otherpass"
        }
                                  ).data["access"]
        other_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        create_response = other_client.post("/api/categories/", {
            "name": "Privée", "description": "Top secret"
        }
                                            )
        category_id = create_response.data["id"]

        # Essayer de la récupérer avec le mauvais utilisateur
        response = self.client.get(f"/api/categories/{category_id}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Essayer de la modifier
        patch_response = self.client.patch(f"/api/categories/{category_id}/", {
            "name": "Hackée"
        }
                                           )
        assert patch_response.status_code == status.HTTP_404_NOT_FOUND

        # Essayer de la supprimer
        delete_response = self.client.delete(f"/api/categories/{category_id}/")
        assert delete_response.status_code == status.HTTP_404_NOT_FOUND
