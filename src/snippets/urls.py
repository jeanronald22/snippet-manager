from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, LanguageViewSet, SnippetViewSet, TagViewSet)

router = DefaultRouter()

router.register(r'languages', LanguageViewSet, basename='language')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'snippets', SnippetViewSet, basename='snippet')

urlpatterns = [path('', include(router.urls)), ]
