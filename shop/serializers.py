from django.contrib.auth.models import User
from rest_framework import serializers

from shop.models import Avatar, Profile, Category


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer()

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]


class ChangePasswordSerializer(serializers.ModelSerializer):
    currentPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('currentPassword', 'newPassword')

    def validate_currentPassword(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Текущий пароль неверен.")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['newPassword'])
        instance.save()
        return instance



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'image_src', 'image_alt']


