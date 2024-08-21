from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.middleware.csrf import get_token

from .models import CustomUser
from .serializers import (UserSerializer,
                          UserProfileSerializer,
                          UserProfileCreateSerializer,
                          UserListSerializer,
                          GroupSerializer,
                          UserEmailSerializer,

                          )


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
        else:
            return Response('Datos incorrectos', status=status.HTTP_401_UNAUTHORIZED)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            session_key = request.session.session_key
            csrf_token = get_token(request)

            response = Response({'message': 'Login exitoso'}, status=status.HTTP_200_OK)
            response['sessionid'] = session_key
            response['X-CSRFToken'] = csrf_token
            return response

        return Response('Datos incorrectos', status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):

    def post(self, request):
        logout(request)
        response = Response({'message': 'Vuelve pronto'}, status=status.HTTP_200_OK)
        return response


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserProfileCreateSerializer
        return UserListSerializer


class UserDestroyUpdateAPIView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = 'uuid'
    serializer_class = UserProfileCreateSerializer
    permission_classes = [IsAuthenticated]


class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class SendEmailView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = UserEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.get(email=email)
            random_password = get_random_string(length=8)
            user.set_password(random_password)
            user.save()
            send_mail(
                'Recuperacion de contraseña',
                f'Tu contraseña temporal es: {random_password} usuario: {user.username}',
                'from@example.com',  # Cambia esto a tu dirección de correo
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Correo enviado correctamente.'}, status=status.HTTP_200_OK)
        return Response({'message': 'El correo no existe.'}, status=status.HTTP_401_UNAUTHORIZED)