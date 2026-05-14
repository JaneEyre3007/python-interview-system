from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserAIConfig

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserAIConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAIConfig
        fields = ['id', 'provider', 'api_key', 'api_url', 'model_name', 'is_active']
        extra_kwargs = {
            'api_key': {'write_only': True}
        }
