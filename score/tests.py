from django.test import TestCase
from django.urls import reverse
from .models import *
import json


class ServerTestCase(TestCase):
    def test_post_add_user(self):
        """
        Check post method that saves new user to the DataBase
        :return:
        """

        test_set = [
            {
                "data": {
                        "username": "",
                        "email": "user1@mail.ru",
                        "password": "Abcd123!"
                },
                "status_code": 400

            },
            {
                "data": {
                    "username": "user1",
                    "email": "",
                    "password": "Abcd123!"
                },
                "status_code": 400

            },
            {
                "data": {
                    "username": "user1",
                    "email": "user1mail.ru",
                    "password": "Abcd123!"
                },
                "status_code": 400

            },
            {
                "data": {
                    "username": "user1",
                    "email": "user1@mail.ru",
                    "password": ""
                },
                "status_code": 400

            },
            {
                "data": {
                    "username": "user1",
                    "email": "user1@mail.ru",
                    "password": "Abcd!"
                },
                "status_code": 400

            },
            {
                "data": {
                    "username": "user1",
                    "email": "user1@mail.ru",
                    "password": "Abcd1234"
                },
                "status_code": 400

            },
            {
                "data": {
                    "username": "user1",
                    "email": "user1@mail.ru",
                    "password": "Abcd!wew"
                },
                "status_code": 400

            },
            {
                "data": {
                    "username": "user1",
                    "email": "user1@mail.ru",
                    "password": "12323!11"
                },
                "status_code": 400

            },
            {
                "data": {
                    "username": "user1",
                    "email": "user1@mail.ru",
                    "password": "Abcd123!"
                },
                "status_code": 200

            },
        ]
        for test in test_set:
            response = self.client.post(
                reverse('register'),
                data=json.dumps(test["data"]),
                content_type="application/json"
            )
            self.assertEqual(response.status_code, test["status_code"])


    def test_post_login(self):
        """
        Check post method for user logging in
        :return:
        """
        test_set = [
            {
                "data": {
                    "username": "user100",
                    "password": "Abcd123!"
                },
                "status_code": 403
            },
            {
                "data": {
                    "username": "user10",
                    "password": "Abcd124!"
                },
                "status_code": 403
            },
            {
                "data": {
                    "username": "user1",
                    "password": "Abcd123!"
                },
                "status_code": 200
            },
        ]

        self.client.post(
            reverse('register'),
            data=json.dumps({
                "username": "user1",
                "email": "user1@mail.ru",
                "password": "Abcd123!"
            }),
            content_type="application/json"
        )

        for test in test_set:
            response = self.client.post(
                reverse('login'),
                data=json.dumps(test["data"]),
                content_type="application/json"
            )
            self.assertEqual(response.status_code, test["status_code"])

    def test_get_logged_user(self):
        """
        Check getting logged user
        :return:
        """
        # register user
        self.client.post(
            reverse('register'),
            data=json.dumps({
                "username": "user1",
                "email": "user1@mail.ru",
                "password": "Abcd123!"
            }),
            content_type="application/json"
        )

        # login user
        self.client.post(
            reverse('login'),
            data=json.dumps({
                "username": "user1",
                "password": "Abcd123!"
            }),
            content_type="application/json"
        )
        # test logged user
        response = self.client.get(
            reverse('user')
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], "user1@mail.ru")

    def test_post_logout(self):
        # register user
        self.client.post(
            reverse('register'),
            data=json.dumps({
                "username": "user1",
                "email": "user1@mail.ru",
                "password": "Abcd123!"
            }),
            content_type="application/json"
        )

        # login user
        self.client.post(
            reverse('login'),
            data=json.dumps({
                "username": "user1",
                "password": "Abcd123!"
            }),
            content_type="application/json"
        )

        # test logout
        response = self.client.post(
            reverse('logout')
        )
        self.assertEqual(response.status_code, 200)
