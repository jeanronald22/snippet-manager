from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['list', 'destroy']:
            return [IsAdminUser()]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_object(self):
        if self.action in ['update', 'partial_update']:
            # L'utilisateur ne peut modifier que son propre profil
            return self.request.user

        obj = super().get_object()

        if self.action == 'retrieve':
            # Seul admin ou la personne elle-même peut voir le profil
            if self.request.user != obj and not self.request.user.is_staff:
                raise PermissionDenied("Vous ne pouvez voir que votre propre profil.")

        return obj

