from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from shop.models import Profile


class SignInView(APIView):
    def post(self, request):
        serialized_data = list(request.POST.keys())[0]
        user_data = json.loads(serialized_data)
        username = user_data.get("username")
        password = user_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
