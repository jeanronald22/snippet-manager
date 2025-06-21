import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Category, Language, Tag


@pytest.mark.django_db
class TestSnippetAPI:
    def setup_method(self):
        self.client = APIClient()

        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        # Créer des catégories, tags et langage pour cet utilisateur
        self.category = Category.objects.create(user=self.user, name='Cat1', description='desc')
        self.tag = Tag.objects.create(user=self.user, name='Tag1', description='desc', color='#fff')
        self.language = Language.objects.create(user=self.user, name='Python')

        # Authentification
        response = self.client.post('/api/auth/token/', {
            'username': self.username, 'password': self.password,
        }
                                    )
        assert response.status_code == 200
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_snippet(self):
        data = {
            "name": "My snippet", "description": "Desc snippet", "code": "print('hello')",
            "instruction": "Use this code carefully", "categories": [self.category.id], "tags": [self.tag.id],
            "language": self.language.id,
        }
        response = self.client.post('/api/snippets/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == "My snippet"

    def test_user_can_only_see_own_snippets(self):
        # Créer snippet pour un autre user
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        other_category = Category.objects.create(user=other_user, name='CatOther', description='desc')
        other_tag = Tag.objects.create(user=other_user, name='TagOther', description='desc', color='#000')
        other_language = Language.objects.create(user=other_user, name='Java')
        other_client = APIClient()
        response = other_client.post('/api/auth/token/', {
            'username': 'otheruser', 'password': 'otherpass'
        }
                                     )
        other_token = response.data['access']
        other_client.credentials(HTTP_AUTHORIZATION=f'Bearer {other_token}')
        other_client.post('/api/snippets/', {
            "name": "Other snippet", "description": "Other desc", "code": "System.out.println('hello');",
            "instruction": "Use carefully", "categories": [other_category.id], "tags": [other_tag.id],
            "language": other_language.id,
        }
                          )

        # Le user courant crée un snippet
        self.client.post('/api/snippets/', {
            "name": "My snippet", "description": "Desc snippet", "code": "print('hello')",
            "instruction": "Use this code carefully", "categories": [self.category.id], "tags": [self.tag.id],
            "language": self.language.id,
        }
                         )

        # Récupérer la liste des snippets
        response = self.client.get('/api/snippets/')
        names = [s['name'] for s in response.data]
        assert "My snippet" in names
        assert "Other snippet" not in names

    def test_forbidden_access_returns_404(self):
        # Créer snippet pour un autre user
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        other_category = Category.objects.create(user=other_user, name='CatOther', description='desc')
        other_tag = Tag.objects.create(user=other_user, name='TagOther', description='desc', color='#000')
        other_language = Language.objects.create(user=other_user, name='Java')
        other_client = APIClient()
        response = other_client.post('/api/auth/token/', {
            'username': 'otheruser', 'password': 'otherpass'
        }
                                     )
        other_token = response.data['access']
        other_client.credentials(HTTP_AUTHORIZATION=f'Bearer {other_token}')
        create_response = other_client.post('/api/snippets/', {
            "name": "Other snippet", "description": "Other desc", "code": "System.out.println('hello');",
            "instruction": "Use carefully", "categories": [other_category.id], "tags": [other_tag.id],
            "language": other_language.id,
        }
                                            )
        snippet_id = create_response.data['id']

        # Essayer d’accéder, modifier, supprimer avec mauvais user
        response = self.client.get(f'/api/snippets/{snippet_id}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

        patch_response = self.client.patch(f'/api/snippets/{snippet_id}/', {'name': 'Hack'})
        assert patch_response.status_code == status.HTTP_404_NOT_FOUND

        delete_response = self.client.delete(f'/api/snippets/{snippet_id}/')
        assert delete_response.status_code == status.HTTP_404_NOT_FOUND
