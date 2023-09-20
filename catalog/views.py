from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from catalog.forms import MusicianCreationForm, MusicianUpdateForm, \
    SongCreationForm
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


class MusicianDetailView(generic.DetailView):
    model = Musician
    queryset = Musician.objects.prefetch_related(
        "performance_set",
        "performance_set__songs",
        "bands"
    )


class MusicianCreateView(generic.CreateView):
    model = Musician
    form_class = MusicianCreationForm


class MusicianUpdateView(generic.UpdateView):
    model = Musician
    form_class = MusicianUpdateForm
    success_url = reverse_lazy("catalog:musician-list")


class BandListView(generic.ListView):
    model = Band


class BandDetailView(generic.DetailView):
    model = Band
    queryset = Band.objects.prefetch_related("members", "albums")


class SongListView(generic.ListView):
    model = Song
    queryset = Song.objects.prefetch_related("albums", "albums__band")


class SongDetailView(generic.DetailView):
    model = Song
    queryset = Song.objects.prefetch_related("performances", "albums__band")


class SongCreateView(generic.CreateView):
    model = Song
    form_class = SongCreationForm
    success_url = reverse_lazy("catalog:song-list")
