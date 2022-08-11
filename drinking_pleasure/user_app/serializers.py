from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MazleUser

MazleUser = get_user_model()

class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    passwd = serializers.CharField(required=True)

    def create(self, validated_data):
        user = MazleUser.objects.create(
            email=validated_data['email'],
        )
        user.set_password(validated_data['passwd'])

        user.save()
        return user

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    passwd = serializers.CharField(required=True)
    
    class Meta:
        model = MazleUser
        fields = ['email','passwd', 'profile', 'nickname', 'birth']