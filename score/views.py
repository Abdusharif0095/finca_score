import os
import pandas as pd
from pycaret.classification import *
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework.views import APIView
from .serializers import UserSerializer, ScoreModelSerializer
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
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from finca.settings import BASE_DIR


# model for predictions
classifier = load_model(f"{BASE_DIR}/score/finca_score")


# Create your views here.
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


class LoginView(APIView):
    def initialize_request(self, request, *args, **kwargs):
        setattr(request, 'csrf_processing_done', True)
        return super().initialize_request(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            example={
                "username": "username",
                "password": "password"
            },
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
                    'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
                },
            ),
            400: "Bad request - validation error",
        },
    )
    def post(self, request):
        # print(request.data)
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed('User is not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Wrong password!')

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


class RegisterView(APIView):
    def initialize_request(self, request, *args, **kwargs):
        setattr(request, 'csrf_processing_done', True)
        return super().initialize_request(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="user"),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['username', 'email', 'password'],
            example={
                'username': 'user',
                'email': 'user@gmail.com',
                'password': 'Passw0rd!',
            },
        ),
        responses={200: openapi.Response('Register new user', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                     description='user id'),
                'username': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='username'),
                'email': openapi.Schema(type=openapi.TYPE_STRING,
                                        description='user email'),
            },
        )),
        }
    )
    def post(self, request):
        # print(request.data)
        email = request.data['email']
        try:
            validate_email(email)
        except ValidationError:
            data = {
                "email": {
                    "message": "The field is not filled correctly!"
                }
            }
            return JsonResponse(data, status=400)

        password = request.data["password"]
        data = {
            "password": {
                "message": "The field must be at least 8 characters long and "
                           "contain uppercase, lowercase letters, numbers, and symbols!"
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


class UserView(APIView):
    def initialize_request(self, request, *args, **kwargs):
        setattr(request, 'csrf_processing_done', True)
        return super().initialize_request(request, *args, **kwargs)

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Not authorized!')

        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Not authorized!')

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


class ScorePredict(APIView):
    def initialize_request(self, request, *args, **kwargs):
        setattr(request, 'csrf_processing_done', True)
        return super().initialize_request(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ScoreModelSerializer,
    )
    def post(self, request):
        serializer = ScoreModelSerializer(data=request.data)
        if serializer.is_valid():
            dt = pd.DataFrame(request.data, index=[0])
            # print(data)
            prediction = predict_model(classifier, data=dt,
                                       raw_score=True, encoded_labels=True)
            # print(prediction)
            result = prediction.to_dict()
            res = {}

            for key in result:
                res[key] = result[key][0]

            res["probability_of_good"] = res["prediction_score_0"]
            res["probability_of_bad"] = res["prediction_score_1"]
            res.pop("prediction_score_0", None)
            res.pop("prediction_score_1", None)
            return JsonResponse(res, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)
