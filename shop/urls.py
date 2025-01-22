from django.urls import path
from . import views
from .views import (SignInView,
                    SignUpView,
                    ProfileView,
                    ChangePasswordView)

app_name = 'shop'

urlpatterns = [
    path("sign-in/", SignInView.as_view(), name="login"),
    path("sign-up/", SignUpView.as_view(), name="register"),
    path('sign-out/', views.signOut),
    path("profile/", ProfileView.as_view(), name="profile"),
    path('profile/password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile/avatar/', views.avatar, name='avatar'),
]
