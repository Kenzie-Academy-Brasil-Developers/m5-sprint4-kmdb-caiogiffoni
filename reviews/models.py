from django.db import models

# Create your models here.


class RecomendationChoices(models.TextChoices):
    MUST_WATCH = "Must Watch"
    SHOULD_WATCH = "Should Watch"
    AVOID_WATCH = "Avoid Watch"
    DEFAULT = "No Opinion"


class Review(models.Model):
    stars = models.SmallIntegerField()
    review = models.TextField()
    spoilers = models.BooleanField(blank=True, null=True, default=False)
    recomendation = models.CharField(
        max_length=50,
        choices=RecomendationChoices.choices,
        default=RecomendationChoices.DEFAULT,
    )
    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE)
    critic = models.ForeignKey("accounts.User", on_delete=models.CASCADE)


    def __repr__(self) -> str:
        return f"<Review {self.id} - {self.review}>"
