from django.urls import path

from . import views
from .views import SignInView, SignUpView

urlpatterns = [
    path("sign-up/", SignInView.as_view(), name="register"),
    path("sign-up/", SignUpView.as_view(), name="register"),
    path('sign-out', views.signOut),

]
