from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404, render
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView, Request, Response, status

from accounts.models import User
from accounts.permissions import IsAdminOrOwner
from accounts.serializers import LoginSerializer, UserSerializer


class UserRegister(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        users = User.objects.all()
        result_page = self.paginate_queryset(users, request, view=self)
        serializer = UserSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class UserViewUnique(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrOwner]

    def get(self, request: Request, user_id) -> Response:
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)

        return Response(serializer.data)


class AuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if not user:
            return Response(
                {"detail": "invalid credentials"}, status.HTTP_400_BAD_REQUEST
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
            }
        )
