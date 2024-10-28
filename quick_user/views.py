from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from .serializers import SignupSerializer, QuickUserSerializer
from .models import QuickUser


class SignupAPIView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            subject = "Welcome to QLearner!"
            message = f"Hello {user.profile.first_name},\n\nWelcome to QLearner! We're excited to have you on board."
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            user_serializer = QuickUserSerializer(user)

            response_data = {
                "message": "User Account Created",
                "user": user_serializer.data,
                "status": True
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)