from accounts.serializers import UserReviewSerializer
from movies.models import Movie
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review



class ReviewSerializer(serializers.ModelSerializer):
    stars = serializers.IntegerField(min_value=1, max_value=10)
    critic = UserReviewSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "stars",
            "review",
            "spoilers",
            "recomendation",
            "movie_id",
            "critic",
        ]
        read_only_fields = ["movie_id"]



