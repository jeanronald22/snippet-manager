from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

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


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({'access': access_token}, status=status.HTTP_200_OK)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite='strict',
                            max_age=7 * 24 * 60 * 60,  # 7jours
                            path="/"
                            )
        return response


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response({'detail': 'No refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh_token = RefreshToken(refresh_token)
            access_token = str(refresh_token.access_token)
            return Response({'access': access_token}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'detail': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response({'detail': 'Logout'}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token', path='/'
                               )
        return response
