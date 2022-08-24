from accounts.models import User
from django.urls import reverse
from movies.models import Movie
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import Response, status


class TestMovieAuth(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client: APIClient

        common_user_data = {
            "username": "lucira",
            "email": "lucira@mail.com",
            "birthdate": "1999-09-09",
            "first_name": "Lucira",
            "last_name": "Critica",
            "password": "1234",
            "is_critic": True,
        }

        admin_user_data = {
            "username": "gohan",
            "birthdate": "1993-03-03",
            "password": "1234abcd",
        }

        # Criando usuário comum e seu Token
        common_user = User.objects.create_user(**common_user_data)
        cls.common_token = Token.objects.create(user=common_user)

        # Criando usuário admin e seu Token
        admin_user = User.objects.create_superuser(**admin_user_data)
        cls.admin_token = Token.objects.create(user=admin_user)

        cls.movie_data_1 = {
            "title": "De volta para o futuro",
            "duration": "120m",
            "genres": [{"name": "Aventura"}, {"name": "Drama"}],
            "premiere": "1970-10-13",
            "classification": 12,
            "synopsis": "McFlay Corleone (Marlon Brando) é o chefe...",
        }

        movie_data_2 = {
            "title": "De volta para o futuro",
            "duration": "120m",
            "genres": [{"name": "Aventura"}, {"name": "Drama"}],
            "premiere": "1970-10-13",
            "classification": 12,
            "synopsis": "McFlay Corleone (Marlon Brando) é o chefe...",
        }


        cls.base_movie_url = reverse("movie-view")


    def test_common_user_cannot_add_movie(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.common_token.key
        )
        response: Response = self.client.post(
            self.base_movie_url, data=self.movie_data_1
        )

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_unauthenticated_user_cannot_add_movie(self):
        response: Response = self.client.post(
            self.base_movie_url, data=self.movie_data_1
        )

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_admin_user_can_add_movie(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.admin_token.key
        )
        response: Response = self.client.post(
            self.base_movie_url, data=self.movie_data_1, format="json"
        )
        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)