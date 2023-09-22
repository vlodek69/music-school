from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from catalog.forms import MusicianCreationForm, MusicianUpdateForm, \
    SongForm, PerformanceForm, InstrumentCreationForm, \
    AlbumForm, GenreCreationForm
from catalog.models import Band, Song, Musician, Album, Performance, \
    Instrument, Genre


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


class BandUpdateView(generic.UpdateView):
    model = Band
    fields = "__all__"
    success_url = reverse_lazy("catalog:band-list")


def album_create_view(request):
    album_form = AlbumForm()
    genre_creation_form = GenreCreationForm()
    if request.method == "POST":
        if "album" in request.POST:
            album_form = AlbumForm(request.POST)
            if album_form.is_valid():
                album_form.save()
                return redirect(
                    "catalog:band-detail",
                    pk=album_form.cleaned_data.get("band").id
                )
        if "genre" in request.POST:
            genre_creation_form = GenreCreationForm(request.POST)
            if genre_creation_form.is_valid():
                genre_creation_form.save()
                return redirect("catalog:album-create")
    context = {
        "album_form": album_form,
        "genre_creation_form": genre_creation_form,
    }
    return render(request, "catalog/album_form.html", context=context)


def album_update_view(request, pk):
    album_obj = get_object_or_404(Album, id=pk)
    album_form = AlbumForm(instance=album_obj)
    genre_creation_form = GenreCreationForm()
    if request.method == "POST":
        if "album" in request.POST:
            album_form = AlbumForm(
                request.POST,
                instance=album_obj
            )
            if album_form.is_valid():
                album_form.save()
                return redirect(
                    "catalog:band-detail",
                    pk=album_form.cleaned_data.get("band").id
                )
        if "genre" in request.POST:
            genre_creation_form = GenreCreationForm(request.POST)
            if genre_creation_form.is_valid():
                genre_creation_form.save()
                return redirect("catalog:album-update", pk=pk)
    context = {
        "album_form": album_form,
        "genre_creation_form": genre_creation_form,
    }
    return render(request, "catalog/album_form.html", context=context)


class SongListView(generic.ListView):
    model = Song
    queryset = Song.objects.prefetch_related("albums", "albums__band")


class SongDetailView(generic.DetailView):
    model = Song
    queryset = Song.objects.prefetch_related("performances", "albums__band")


def song_create_view(request):
    song_form = SongForm()
    performance_creation_form = PerformanceForm()
    instrument_creation_form = InstrumentCreationForm()
    if request.method == "POST":
        if "song" in request.POST:
            song_form = SongForm(request.POST)
            if song_form.is_valid():
                song_form.save()
                return redirect("catalog:song-list")
        if "performance" in request.POST:
            performance_creation_form = PerformanceForm(request.POST)
            if performance_creation_form.is_valid():
                performance_creation_form.save()
                return redirect("catalog:song-create")
        if "instrument" in request.POST:
            instrument_creation_form = InstrumentCreationForm(request.POST)
            if instrument_creation_form.is_valid():
                instrument_creation_form.save()
                return redirect("catalog:song-create")
    context = {
        "song_form": song_form,
        "performance_creation_form": performance_creation_form,
        "instrument_creation_form": instrument_creation_form,
    }
    return render(request, "catalog/song_form.html", context=context)


def song_update_view(request, pk):
    song_obj = get_object_or_404(Song, id=pk)
    song_form = SongForm(instance=song_obj)
    performance_creation_form = PerformanceForm()
    instrument_creation_form = InstrumentCreationForm()
    if request.method == "POST":
        if "song" in request.POST:
            song_form = SongForm(request.POST, instance=song_obj)
            if song_form.is_valid():
                song_form.save()
                return redirect("catalog:song-detail", pk=song_obj.id)
        if "performance" in request.POST:
            performance_creation_form = PerformanceForm(request.POST)
            if performance_creation_form.is_valid():
                performance_creation_form.save()
                return redirect("catalog:song-update", pk=song_obj.id)
        if "instrument" in request.POST:
            instrument_creation_form = InstrumentCreationForm(request.POST)
            if instrument_creation_form.is_valid():
                instrument_creation_form.save()
                return redirect("catalog:song-update", pk=song_obj.id)
    context = {
        "song_form": song_form,
        "performance_creation_form": performance_creation_form,
        "instrument_creation_form": instrument_creation_form,
    }
    return render(request, "catalog/song_form.html", context=context)


class PerformanceCreateView(generic.CreateView):
    model = Performance
    form_class = PerformanceForm
    success_url = reverse_lazy("catalog:musician-list")


class PerformanceUpdateView(generic.UpdateView):
    model = Performance
    form_class = PerformanceForm
    success_url = reverse_lazy("catalog:musician-list")


class PerformanceDeleteView(generic.DeleteView):
    model = Performance
    success_url = reverse_lazy("catalog:musician-list")


class InstrumentListView(generic.ListView):
    model = Instrument


class InstrumentCreateView(generic.CreateView):
    model = Instrument
    fields = "__all__"
    success_url = reverse_lazy("catalog:instrument-list")


class InstrumentUpdateView(generic.UpdateView):
    model = Instrument
    fields = "__all__"
    success_url = reverse_lazy("catalog:instrument-list")


class InstrumentDeleteView(generic.DeleteView):
    model = Instrument
    success_url = reverse_lazy("catalog:instrument-list")


class GenreListView(generic.ListView):
    model = Genre


class GenreCreateView(generic.CreateView):
    model = Genre
    fields = "__all__"
    success_url = reverse_lazy("catalog:genre-list")


class GenreUpdateView(generic.UpdateView):
    model = Genre
    fields = "__all__"
    success_url = reverse_lazy("catalog:genre-list")


class GenreDeleteView(generic.DeleteView):
    model = Genre
    success_url = reverse_lazy("catalog:genre-list")
