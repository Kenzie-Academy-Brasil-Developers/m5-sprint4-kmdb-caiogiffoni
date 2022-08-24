from accounts.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status


class UserRegisterViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url = "/api/users/register/"
        cls.user_data = {
            "username": "lucira",
            "email": "lucira@mail.com",
            "birthdate": "1999-09-09",
            "first_name": "Lucira",
            "last_name": "Critica",
            "password": "1234",
            "is_critic": True,
        }

    def test_can_register_user(self):
        response = self.client.post(self.base_url, data=self.user_data)

        expect_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expect_status_code, result_status_code)

    def test_register_user_fields(self):
        response = self.client.post(self.base_url, data=self.user_data)
        expected_return_fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "birthdate",
            "bio",
            "is_critic",
            "updated_at",
            "is_superuser",
        )

        self.assertEqual(len(response.data.keys()), 10)

        for expected_field in expected_return_fields:
            self.assertIn(expected_field, response.data)

        result_return_fields = tuple(response.data.keys())
        self.assertTupleEqual(expected_return_fields, result_return_fields)


class LoginTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url = reverse("login-auth-token")

        cls.user_data = {
            "username": "lucira",
            "email": "lucira@mail.com",
            "birthdate": "1999-09-09",
            "first_name": "Lucira",
            "last_name": "Critica",
            "password": "1234",
            "is_critic": True,
        }

        cls.user_credentials = {
            "username": "lucira",
            "password": "1234",
        }

        cls.user = User.objects.create_user(**cls.user_data)

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.base_url, data=self.user_credentials)
        self.assertEqual(200, response.status_code)

    def test_token_field_is_returned(self):
        response = self.client.post(self.base_url, data=self.user_credentials)

        self.assertIn("token", response.data)
