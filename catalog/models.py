from django.contrib.auth.models import AbstractUser
from django.db import models


class Instrument(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Musician(AbstractUser):
    full_name = models.CharField(max_length=255)
    pseudonym = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["username"]
        verbose_name = "musician"

    def __str__(self) -> str:
        return self.full_name


class Performance(models.Model):
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    instruments = models.ManyToManyField(Instrument, related_name="performers")

    def __str__(self) -> str:
        instrument_list = [
            instrument.name for instrument in self.instruments.all()
        ]

        return f"{self.musician.full_name}({', '.join(instrument_list)})"


class Band(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(Musician, related_name="bands")

    def __str__(self) -> str:
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=255)
    performances = models.ManyToManyField(Performance, related_name="songs")

    def __str__(self) -> str:
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=255)
    band = models.ForeignKey(
        Band,
        on_delete=models.CASCADE,
        related_name="albums"
    )
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    year_published = models.IntegerField()
    songs = models.ManyToManyField(Song, related_name="albums")

    def __str__(self) -> str:
        return f"{self.name}({self.band.name})"
