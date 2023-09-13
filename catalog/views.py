from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import generic

from catalog.models import Band, Song, Musician


def index(request):
    num_musicians = get_user_model().objects.count()
    num_bands = Band.objects.count()
    num_songs = Song.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_musicians": num_musicians,
        "num_bands": num_bands,
        "num_songs": num_songs,
        "num_visits": num_visits + 1,
    }

    return render(request, "catalog/index.html", context=context)


class MusicianListView(generic.ListView):
    model = Musician

