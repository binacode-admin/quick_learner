from django.urls import path
from .views import SignupAPIView, GetUserProfileAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('profile/', GetUserProfileAPIView.as_view(), name='get_user_profile'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
