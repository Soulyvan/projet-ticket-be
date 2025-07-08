from django.contrib.auth import login, logout, authenticate
from rest_framework import generics, status
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer


# Enregistrement
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Connexion
class LoginAPIView(APIView):
    permission_classes = [AllowAny]  # Permet l'accès à tous les utilisateurs

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        print(f"Email: {email}, Password: {password}")

        user = authenticate(username=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'organisateur': user.organisateur,
                }
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# Vue de déconnexion
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]  # L'utilisateur doit être authentifié pour se déconnecter

    def post(self, request):
        # Récupérer le token de l'utilisateur actuel
        try:
            token = Token.objects.get(user=request.user)
            token.delete()  # Supprimer le token pour déconnecter l'utilisateur
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserAPIView(APIView):
    permission_classes = [IsAuthenticated]  # L'utilisateur doit être authentifié
    print("On vient quand meme")
    def delete(self, request):
        token = get_authorization_header(request).decode('utf-8')
        print(f"Token reçu : {token}")  # Pour vérifier si le token est transmis

        user = request.user  # Récupérer l'utilisateur authentifié

        try:
            # Supprimer l'utilisateur
            user.delete()
            return Response({"detail": "User deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
