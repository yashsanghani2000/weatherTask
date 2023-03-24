from django.conf import settings
from django.urls import path
from .views import *
from django.conf.urls.static import static

urlpatterns = [
    path('register-user/', RegiserUser.as_view()),
    path('user-emai-verify-otp/', UserEmaiVerifyOTP.as_view()),
    path('login-user/', LoginView.as_view()),
    path('get-weather/', GetWeather.as_view()),
]