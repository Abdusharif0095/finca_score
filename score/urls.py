from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, homeView, GetClient


urlpatterns = [
    # path('', homeView, name='home'),
    path('user', UserView.as_view(), name='user'),
    path('get_client', GetClient.as_view(), name='get_client'),
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),
]
