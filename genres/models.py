from django.db import models

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=127)
    movies = models.ManyToManyField("movies.Movie", related_name="genres")

    def __repr__(self) -> str:
        return f"<Genre {self.id} - {self.name}>"
