from django.db import models

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10)
    premiere = models.DateField()
    classification = models.SmallIntegerField()
    synopsis = models.TextField()

    def __repr__(self) -> str:
        return f"<Movie {self.id} - {self.title}>"
