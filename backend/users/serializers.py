from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    gender = serializers.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'birth_date', 'city', 'language', 'password', 'confirm_password']

    def validate_gender(self, value):
        gender_map = {"Мужской": "male", "Женский": "female"}
        if value not in gender_map:
            raise serializers.ValidationError("Допустимые значения: Мужской, Женский.")
        return gender_map[value]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        gender = validated_data.pop('gender')
        user = User.objects.create_user(**validated_data, gender=gender)
        return user


User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(request=self.context.get("request"), email=email, password=password)

        if not user:
            raise serializers.ValidationError("Неверный email или пароль")

        # ключ должен быть "email", а не "username"
        data = super().validate({
            "email": user.email,
            "password": password,
        })

        return {
            "access_token": data["access"],
            "token_type": "bearer"
        }