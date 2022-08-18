from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status

from accounts.serializers import UserSerializer

# Create your views here.


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)