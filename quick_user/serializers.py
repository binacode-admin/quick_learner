from rest_framework import serializers
from .models import QuickUser, QuickUserProfile


class QuickUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickUserProfile
        fields = ['profile_picture', 'first_name', 'last_name', 'last_login_date', 'date_created', 'date_updated']


class QuickUserSerializer(serializers.ModelSerializer):
    profile = QuickUserProfileSerializer()

    class Meta:
        model = QuickUser
        fields = ['id', 'email', 'user_category', 'is_active', 'profile']


class SignupSerializer(serializers.ModelSerializer):
    profile = QuickUserProfileSerializer()

    class Meta:
        model = QuickUser
        fields = ['email', 'user_category', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')

        user = QuickUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # QuickUserProfile.objects.create(user=user, **profile_data)
        return user