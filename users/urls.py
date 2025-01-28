from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (SignInView,
                    SignUpView,
                    ProfileView,
                    UpdateAvatarView,
                    UpdatePasswordView)

app_name = 'users'

urlpatterns = [
    path('sign-in/', SignInView.as_view(), name='sign_in'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/avatar/', UpdateAvatarView.as_view(), name='update_avatar'),
    path('profile/password/', UpdatePasswordView.as_view(), name='update_password'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
