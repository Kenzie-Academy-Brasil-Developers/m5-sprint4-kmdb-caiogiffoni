from django.shortcuts import get_object_or_404
from genres.models import Genre
from genres.serializers import GenreSerializer
from rest_framework import serializers

from movies.models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10)
    premiere = serializers.DateField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()
    genres = GenreSerializer(many=True, allow_null=True)

    def create(self, validated_data: dict) -> Movie:
        genres_data = validated_data.pop("genres", [])
        genres = [
            Genre.objects.get_or_create(**genre)[0] for genre in genres_data
        ]
        movie = Movie.objects.create(**validated_data)
        movie.genres.add(*genres)

        return movie
