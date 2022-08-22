from django.shortcuts import get_object_or_404, render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView, Request, Response, status

from accounts.models import User
from accounts.permissions import IsAdminOrOwner
from accounts.serializers import UserSerializer


class UserRegister(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request: Request) -> Response:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)


class UserViewUnique(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrOwner]

    def get(self, request: Request, user_id) -> Response:
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)

        return Response(serializer.data)
