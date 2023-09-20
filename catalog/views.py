from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from catalog.forms import MusicianCreationForm, MusicianUpdateForm, \
    SongCreationForm, PerformanceCreationForm, InstrumentCreationForm
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


class BandCreateView(generic.CreateView):
    model = Band
    fields = "__all__"
    success_url = reverse_lazy("catalog:band-list")


class SongListView(generic.ListView):
    model = Song
    queryset = Song.objects.prefetch_related("albums", "albums__band")


class SongDetailView(generic.DetailView):
    model = Song
    queryset = Song.objects.prefetch_related("performances", "albums__band")


def song_create_view(request):
    song_creation_form = SongCreationForm()
    performance_creation_form = PerformanceCreationForm()
    instrument_creation_form = InstrumentCreationForm()
    if request.method == "POST":
        if "song" in request.POST:
            song_creation_form = SongCreationForm(request.POST)
            if song_creation_form.is_valid():
                song_creation_form.save()
                return redirect("catalog:song-list")
        if "performance" in request.POST:
            performance_creation_form = PerformanceCreationForm(request.POST)
            if performance_creation_form.is_valid():
                performance_creation_form.save()
                return redirect("catalog:song-create")
        if "instrument" in request.POST:
            instrument_creation_form = InstrumentCreationForm(request.POST)
            if instrument_creation_form.is_valid():
                instrument_creation_form.save()
                return redirect("catalog:song-create")
    context = {
        "song_creation_form": song_creation_form,
        "performance_creation_form": performance_creation_form,
        "instrument_creation_form": instrument_creation_form,
    }
    return render(request, "catalog/song_form.html", context=context)
