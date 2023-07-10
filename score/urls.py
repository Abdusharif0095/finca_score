from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, homeView, GetClient


urlpatterns = [
    path('', homeView, name='home'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('user', UserView.as_view(), name='user'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('get_client', GetClient.as_view(), name='get_client'),
]
