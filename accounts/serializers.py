from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    birthdate = serializers.DateField()
    bio = serializers.CharField(
        allow_blank=True, allow_null=True, default=None
    )
    is_critic = serializers.BooleanField(default=False)
    updated_at = serializers.DateTimeField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True, default=False)

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)
