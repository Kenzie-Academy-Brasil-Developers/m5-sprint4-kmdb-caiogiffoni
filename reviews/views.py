from django.shortcuts import get_list_or_404, get_object_or_404, render
from movies.models import Movie
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView, Request, Response, status

from reviews.models import Review
from reviews.permissions import IsAdminOrCriticOrReadOnly, IsAdminOrOwner
from reviews.serializers import ReviewSerializer

# Create your views here.


class ValidationUniqueError(Exception):
    ...


class ReviewView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrCriticOrReadOnly]

    def get(self, request: Request, movie_id: int) -> Response:
        reviews = get_list_or_404(Review, movie_id=movie_id)
        result_page = self.paginate_queryset(reviews, request, view=self)
        serializer = ReviewSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        reviews = Review.objects.filter(
            movie_id=movie.id, critic=request.user.id
        )
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            if len(reviews) > 0:
                raise ValidationUniqueError
        except ValidationUniqueError:
            return Response(
                {"detail": "Review already exists."}, status.HTTP_403_FORBIDDEN
            )

        serializer.save(critic=request.user, movie=movie)

        return Response(serializer.data, status.HTTP_201_CREATED)


class ReviewDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrOwner]

    def get(self, request: Request, movie_id: int, review_id: int) -> Response:

        movie = get_object_or_404(Movie, id=movie_id)
        review = get_object_or_404(Review, id=review_id, movie_id=movie_id)
        serializer = ReviewSerializer(review)

        return Response(serializer.data)

    def delete(
        self, request: Request, movie_id: int, review_id: int
    ) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        review = get_object_or_404(Review, movie_id=movie_id, id=review_id)
        self.check_object_permissions(request, review)

        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
