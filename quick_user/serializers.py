import re
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import QuickUser, QuickUserProfile


class QuickUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickUserProfile
        fields = ['id', 'profile_picture', 'first_name', 'last_name', 'last_login_date', 'date_created', 'date_updated']

class QuickUserSerializer(serializers.ModelSerializer):
    profile = QuickUserProfileSerializer()

    class Meta:
        model = QuickUser
        fields = ['id', 'email', 'category', 'is_active', 'profile']


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = QuickUser
        fields = ['email', 'category', 'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        password = data.get("password")
        password_confirm = data.get("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})

        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise serializers.ValidationError("Password must contain at least one special character.")

        validate_password(password)

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')

        user = QuickUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user