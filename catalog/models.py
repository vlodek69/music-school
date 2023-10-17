from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Instrument(models.Model):
    name = models.CharField(max_length=255, unique=True)

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

    @property
    def instrument_list(self) -> list[str]:
        return list(set(
            instrument.name for performance in self.performance_set.all()
            for instrument in performance.instruments.all()
        ))

    def get_absolute_url(self) -> str:
        return reverse("catalog:musician-detail", kwargs={"pk": self.pk})


class Performance(models.Model):
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    instruments = models.ManyToManyField(Instrument, related_name="performers")

    class Meta:
        ordering = ["musician__full_name"]

    def __str__(self) -> str:
        instrument_list = [
            instrument.name for instrument in self.instruments.all()
        ]

        return f"{self.musician.full_name}({', '.join(instrument_list)})"


class Band(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(Musician, related_name="bands")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:band-detail", kwargs={"pk": self.pk})


class Song(models.Model):
    name = models.CharField(max_length=255)
    performances = models.ManyToManyField(Performance, related_name="songs")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("catalog:song-detail", kwargs={"pk": self.pk})


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
        return self.name
