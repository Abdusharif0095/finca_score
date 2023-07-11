import os

from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import jwt, datetime
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from .decorators import *
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.
def homeView(request):
    return HttpResponse('<h1>Welcome, to Finca Score</h1>')


def pass_has_number(password):
    for s in password:
        if s.isdigit():
            return True
    return False


def pass_has_upper_case(password):
    for s in password:
        if 65 <= ord(s) <= 90:
            return True
    return False


def pass_has_specific_symbol(password):
    symbols = "~!@#$%^&*()_+{}\":;'[]"
    for s in password:
        if s in symbols:
            return True
    return False


# @csrf_exempt
@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(APIView):
    def initialize_request(self, request, *args, **kwargs):
        setattr(request, 'csrf_processing_done', True)
        return super().initialize_request(request, *args, **kwargs)

    def post(self, request):
        # print(request.data)
        email = request.data['email']
        try:
            validate_email(email)
        except ValidationError:
            data = {
                "email": {
                    "message": "Поле не правильно заполнено!"
                }
            }
            return JsonResponse(data, status=400)

        password = request.data["password"]
        data = {
            "password": {
                "message": "Поле должно состоять как минимум из 8 символов и содержать прописные, строчные буквы, числа и символы"
            }
        }
        try:
            validate_password(password=str(password))
        except ValidationError:
            return JsonResponse(data, status=400)

        if not (pass_has_number(password) and pass_has_upper_case(password)):
            return JsonResponse(data, status=400)

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# @method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    def initialize_request(self, request, *args, **kwargs):
        setattr(request, 'csrf_processing_done', True)
        return super().initialize_request(request, *args, **kwargs)

    def post(self, request):
        # print(request.data)
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed('Пользователь не найден!')

        if not user.check_password(password):
            raise AuthenticationFailed('Не правильный пароль!')

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=20),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "message": "Success!",
            "user_id": user.id,
            "jwt": token
        }
        login(request, user)

        return response


class UserView(APIView):
    def initialize_request(self, request, *args, **kwargs):
        setattr(request, 'csrf_processing_done', True)
        return super().initialize_request(request, *args, **kwargs)

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Не авторизован!')

        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Не авторизован!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def initialize_request(self, request, *args, **kwargs):
        setattr(request, 'csrf_processing_done', True)
        return super().initialize_request(request, *args, **kwargs)

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "Success!"
        }
        return response


class GetClient(APIView):
    def initialize_request(self, request, *args, **kwargs):
        setattr(request, 'csrf_processing_done', True)
        return super().initialize_request(request, *args, **kwargs)

    @allowed_users(allowed_roles=['manager'])
    def get(self, request):
        return HttpResponse("<h1>Success<h1>")
