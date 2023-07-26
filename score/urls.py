from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, GetClient, ScorePredict


urlpatterns = [
    path('auth/user', UserView.as_view(), name='user'),
    path('auth/get_client', GetClient.as_view(), name='get_client'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('score/predict', ScorePredict.as_view(), name='predict')
]
