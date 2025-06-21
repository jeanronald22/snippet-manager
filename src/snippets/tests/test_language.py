import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestLanguageAPI:
    def setup_method(self):
        self.client = APIClient()

        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        # Auth via /token/
        response = self.client.post("/api/auth/token/", {
            "username": self.username, "password": self.password
        })
        assert response.status_code == 200
        self.access_token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create(self):
        data = {"name": "Python"}
        response = self.client.post("/api/languages/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == "Python"
        assert 'id' in response.data

    def test_list(self):
        response = self.client.get("/api/languages/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []  # Aucun langage encore

    def test_list_one(self):
        response = self.client.get("/api/languages/1/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update(self):
        # Création
        data = {"name": "Python"}
        create_response = self.client.post("/api/languages/", data)
        language_id = create_response.data['id']

        # Mise à jour complète
        updated_data = {"name": "Python 3"}
        update_response = self.client.put(f"/api/languages/{language_id}/", updated_data)

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.data["name"] == "Python 3"

    def test_partial_update(self):
        # Création
        data = {"name": "Python"}
        create_response = self.client.post("/api/languages/", data)
        language_id = create_response.data['id']

        # Mise à jour partielle
        patch_data = {"name": "Py"}
        patch_response = self.client.patch(f"/api/languages/{language_id}/", patch_data)

        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data["name"] == "Py"

    def test_delete(self):
        # Création
        data = {"name": "Python"}
        create_response = self.client.post("/api/languages/", data)
        language_id = create_response.data['id']

        # Suppression
        delete_response = self.client.delete(f"/api/languages/{language_id}/")

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # Vérifier que l'objet n'existe plus
        get_response = self.client.get(f"/api/languages/{language_id}/")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
