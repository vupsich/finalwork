from rest_framework import serializers
from .models import User

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
