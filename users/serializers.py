from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','email','password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        print("oka")
        validated_data['password'] = make_password(validated_data['password'])
        return super(RegisterSerializer, self).create(validated_data)

class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(
        max_length=128, write_only=True, style={"input_type": "password"}
    )

    class Meta:
        fields = ['email', 'password']

class GetWeatherSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=128,)

    class Meta:
        fields = ['city',]