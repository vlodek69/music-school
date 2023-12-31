from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch, QuerySet
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.list import MultipleObjectMixin
from django_filters.views import FilterView

from catalog.filters import SongInstrumentFilter, SongBandFilterDistinct
from catalog.forms import (
    MusicianCreationForm,
    MusicianUpdateForm,
    SongForm,
    PerformanceForm,
    InstrumentCreationForm,
    AlbumForm,
    GenreCreationForm,
    MusicianSearchForm,
    ByNameSearchForm
)
from catalog.models import (
    Band,
    Song,
    Musician,
    Album,
    Performance,
    Instrument,
    Genre
)


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "catalog/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super(IndexView, self).get_context_data(**kwargs)
        context["num_musicians"] = get_user_model().objects.count()
        context["num_bands"] = Band.objects.count()
        context["num_songs"] = Song.objects.count()

        return context

    def get(self, request, *args, **kwargs) -> TemplateResponse:
        context = self.get_context_data(**kwargs)
        context["num_visits"] = request.session.get("num_visits", 0)
        request.session["num_visits"] = context["num_visits"] + 1

        return self.render_to_response(context)


class MusicianListView(LoginRequiredMixin, generic.ListView):
    model = Musician
    paginate_by = 10

    def get_context_data(self, *, object_list=None,
                         **kwargs) -> dict[str, Any]:
        context = super(MusicianListView, self).get_context_data(**kwargs)

        search_input = self.request.GET.get("search_input")

        context["search_form"] = MusicianSearchForm(initial={
            "search_input": search_input
        })
        return context

    def get_queryset(self) -> QuerySet:
        queryset = get_user_model().objects.all()
        form = MusicianSearchForm(self.request.GET)

        if form.is_valid():
            search_input = form.cleaned_data["search_input"]
            return queryset.filter(
                Q(full_name__icontains=search_input) |
                Q(username__icontains=search_input) |
                Q(pseudonym__icontains=search_input)
            )

        return queryset


class MusicianDetailView(LoginRequiredMixin, generic.DetailView):
    model = Musician
    queryset = Musician.objects.prefetch_related(
        Prefetch(
            "performance_set",
            Performance.objects.prefetch_related(
                "instruments"
            )
        )
    )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context_data = super(MusicianDetailView, self).get_context_data()
        musician_pk = self.kwargs.get("pk", None)
        query_filtered = SongInstrumentFilter(
            self.request.GET,
            queryset=Performance.objects.filter(musician_id=musician_pk).
            prefetch_related(
                Prefetch("songs", Song.objects.prefetch_related(
                    Prefetch("albums", Album.objects.select_related("band"))
                )),
                "instruments"
            )
        )
        context_data["filter"] = query_filtered
        return context_data


class MusicianCreateView(LoginRequiredMixin, generic.CreateView):
    model = Musician
    form_class = MusicianCreationForm


class MusicianUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Musician
    form_class = MusicianUpdateForm
    success_url = reverse_lazy("catalog:musician-list")


class BandListView(LoginRequiredMixin, generic.ListView):
    model = Band
    paginate_by = 10

    def get_context_data(self, *, object_list=None,
                         **kwargs) -> dict[str, Any]:
        context = super(BandListView, self).get_context_data(**kwargs)

        search_input = self.request.GET.get("search_input")

        context["search_form"] = ByNameSearchForm(initial={
            "search_input": search_input
        })
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Band.objects.all()
        form = ByNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["search_input"]
            )

        return queryset


class MusicianDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("catalog:musician-list")


class BandDetailView(
    LoginRequiredMixin, generic.DetailView, MultipleObjectMixin
):
    model = Band
    queryset = Band.objects.prefetch_related("members", "albums")
    paginate_by = 5

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        object_list = Album.objects.filter(band=self.get_object())
        context = super(BandDetailView, self).get_context_data(
            object_list=object_list, **kwargs)
        return context


class BandCreateView(LoginRequiredMixin, generic.CreateView):
    model = Band
    fields = "__all__"
    success_url = reverse_lazy("catalog:band-list")


class BandUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Band
    fields = "__all__"
    success_url = reverse_lazy("catalog:band-list")


class BandDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Band
    success_url = reverse_lazy("catalog:band-list")


class AlbumCreateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "catalog/album_form.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["album_form"] = AlbumForm()
        context["genre_form"] = GenreCreationForm()
        return context

    def post(self, request, *args, **kwargs) -> HttpResponse:
        if "album" in request.POST:
            album_form = AlbumForm(request.POST)
            if album_form.is_valid():
                album_form.save()
                return redirect(
                    "catalog:band-detail",
                    pk=album_form.cleaned_data.get("band").id
                )
        if "genre" in request.POST:
            genre_form = GenreCreationForm(request.POST)
            if genre_form.is_valid():
                genre_form.save()
                return redirect("catalog:album-create")


class AlbumUpdateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "catalog/album_form.html"

    def get_context_data(self, pk, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        album_obj = get_object_or_404(Album, id=pk)
        context["album_form"] = AlbumForm(instance=album_obj)
        context["genre_form"] = GenreCreationForm()
        return context

    def post(self, request, pk, *args, **kwargs) -> HttpResponse:
        album_obj = get_object_or_404(Album, id=pk)
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
            genre_form = GenreCreationForm(request.POST)
            if genre_form.is_valid():
                genre_form.save()
                return redirect("catalog:album-update", pk=pk)


class AlbumDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Album
    success_url = reverse_lazy("catalog:band-list")


class SongListView(LoginRequiredMixin, FilterView):
    model = Song
    paginate_by = 10
    filterset_class = SongBandFilterDistinct

    def get_context_data(self, *, object_list=None,
                         **kwargs) -> dict[str, Any]:
        context = super(SongListView, self).get_context_data(**kwargs)

        search_input = self.request.GET.get("search_input")

        context["search_form"] = ByNameSearchForm(initial={
            "search_input": search_input
        })
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Song.objects.prefetch_related(
            Prefetch(
                "albums",
                Album.objects.select_related("band")
            )
        )
        form = ByNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["search_input"]
            )

        return queryset


class SongDetailView(LoginRequiredMixin, generic.DetailView):
    model = Song
    queryset = Song.objects.prefetch_related("performances", "albums__band")


class SongCreateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "catalog/song_form.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["song_form"] = SongForm()
        context["performance_creation_form"] = PerformanceForm()
        context["instrument_creation_form"] = InstrumentCreationForm()
        return context

    def post(self, request, *args, **kwargs) -> HttpResponse:
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


class SongUpdateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "catalog/song_form.html"

    def get_context_data(self, pk, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        song_obj = get_object_or_404(Song, id=pk)
        context["song_form"] = SongForm(instance=song_obj)
        context["performance_creation_form"] = PerformanceForm()
        context["instrument_creation_form"] = InstrumentCreationForm()
        return context

    def post(self, request, pk, *args, **kwargs) -> HttpResponse:
        song_obj = get_object_or_404(Song, id=pk)
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


class SongDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Song
    success_url = reverse_lazy("catalog:song-list")


class PerformanceCreateView(LoginRequiredMixin, generic.CreateView):
    model = Performance
    form_class = PerformanceForm
    success_url = reverse_lazy("catalog:musician-list")


class PerformanceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Performance
    form_class = PerformanceForm
    success_url = reverse_lazy("catalog:musician-list")


class PerformanceDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Performance
    success_url = reverse_lazy("catalog:musician-list")


class InstrumentListView(LoginRequiredMixin, generic.ListView):
    model = Instrument


class InstrumentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Instrument
    fields = "__all__"
    success_url = reverse_lazy("catalog:instrument-list")


class InstrumentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Instrument
    fields = "__all__"
    success_url = reverse_lazy("catalog:instrument-list")


class InstrumentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Instrument
    success_url = reverse_lazy("catalog:instrument-list")


class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre


class GenreCreateView(LoginRequiredMixin, generic.CreateView):
    model = Genre
    fields = "__all__"
    success_url = reverse_lazy("catalog:genre-list")


class GenreUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Genre
    fields = "__all__"
    success_url = reverse_lazy("catalog:genre-list")


class GenreDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Genre
    success_url = reverse_lazy("catalog:genre-list")
