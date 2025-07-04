from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LoginView, LogoutView, RefreshTokenView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename="user")
urlpatterns = [path('login/', LoginView.as_view(), name='login'),
               path('refresh/', RefreshTokenView.as_view(), name='token_refresh'),
               path('logout/', LogoutView.as_view(), name='logout'), path('', include(router.urls))]
