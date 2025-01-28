from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework import status, permissions
from rest_framework.authtoken.admin import User

from users.models import Profile, Avatar
from users.serializers import AvatarSerializer, ProfileSerializer


class SignInView(APIView):
    def post(self, request):
        try:
            # Получаем данные из тела запроса
            user_data = request.data
            username = user_data.get("username")
            password = user_data.get("password")

            # Проверяем наличие данных
            if not username or not password:
                return Response({"error": "Необходимо указать username и password."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Аутентификация пользователя
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({"message": "Успешный вход"}, status=status.HTTP_200_OK)

            return Response({"error": "Неверные данные для входа"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Ошибка: {e}")  # Логируем ошибку
            return Response({"error": "Ошибка сервера"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    def post(self, request):

        serialized_data = list(request.data.keys())[0]
        user_data = json.loads(serialized_data)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")

        try:
            user = User.objects.create_user(username=username, password=password)
            profile = Profile.objects.create(user=user, first_name=name)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def signOut(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get("currentPassword")
        new_password = request.data.get("newPassword")

        if not user.check_password(current_password):
            return Response({"error": "Текущий пароль указан неверно."}, status=status.HTTP_400_BAD_REQUEST)

        if current_password == new_password:
            return Response({"error": "Новый пароль не может совпадать с текущим."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Пароль успешно обновлен."}, status=status.HTTP_200_OK)


class UpdateAvatarView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]  # Для обработки загрузки файлов

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        avatar_file = request.FILES.get('avatar')  # Получаем загруженный файл
        alt_text = request.data.get('alt', '')  # Получаем описание, если есть

        if not avatar_file:
            return Response({"error": "Файл аватара не был предоставлен."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем новый аватар
        avatar = Avatar.objects.create(src=avatar_file, alt=alt_text)
        profile.avatar = avatar
        profile.save()

        # Используем AvatarSerializer для возврата данных о новом аватаре
        avatar_serializer = AvatarSerializer(avatar)
        return Response(avatar_serializer.data, status=status.HTTP_200_OK)
