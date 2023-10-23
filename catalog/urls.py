from django.urls import path

from catalog.views import (
    IndexView,
    MusicianListView,
    MusicianDetailView,
    MusicianCreateView,
    MusicianUpdateView,
    MusicianDeleteView,
    PerformanceCreateView,
    PerformanceUpdateView,
    PerformanceDeleteView,
    BandListView,
    BandDetailView,
    BandCreateView,
    BandUpdateView,
    BandDeleteView,
    AlbumCreateView,
    AlbumUpdateView,
    AlbumDeleteView,
    SongListView,
    SongDetailView,
    SongCreateView,
    SongUpdateView,
    SongDeleteView,
    InstrumentListView,
    InstrumentCreateView,
    InstrumentUpdateView,
    InstrumentDeleteView,
    GenreListView,
    GenreCreateView,
    GenreUpdateView,
    GenreDeleteView
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("musicians/", MusicianListView.as_view(), name="musician-list"),
    path(
        "musicians/<int:pk>/",
        MusicianDetailView.as_view(),
        name="musician-detail"
    ),
    path(
        "musicians/create/",
        MusicianCreateView.as_view(),
        name="musician-create"
    ),
    path(
        "musicians/<int:pk>/update/",
        MusicianUpdateView.as_view(),
        name="musician-update"
    ),
    path(
        "musicians/<int:pk>/delete/",
        MusicianDeleteView.as_view(),
        name="musician-delete"
    ),
    path(
        "performance/create/",
        PerformanceCreateView.as_view(),
        name="performance-create"
    ),
    path(
        "performance/<int:pk>/update/",
        PerformanceUpdateView.as_view(),
        name="performance-update"
    ),
    path(
        "performance/<int:pk>/delete/",
        PerformanceDeleteView.as_view(),
        name="performance-delete"
    ),
    path("bands/", BandListView.as_view(), name="band-list"),
    path("bands/<int:pk>/", BandDetailView.as_view(), name="band-detail"),
    path("bands/create/", BandCreateView.as_view(), name="band-create"),
    path(
        "bands/<int:pk>/update/", BandUpdateView.as_view(), name="band-update"
    ),
    path(
        "bands/<int:pk>/delete/", BandDeleteView.as_view(), name="band-delete"
    ),
    path("album/create/", AlbumCreateView.as_view(), name="album-create"),
    path(
        "album/<int:pk>/update/",
        AlbumUpdateView.as_view(),
        name="album-update"
    ),
    path(
        "album/<int:pk>/delete/",
        AlbumDeleteView.as_view(),
        name="album-delete"
    ),
    path("songs/", SongListView.as_view(), name="song-list"),
    path("songs/<int:pk>/", SongDetailView.as_view(), name="song-detail"),
    path("songs/create/", SongCreateView.as_view(), name="song-create"),
    path(
        "songs/<int:pk>/update/", SongUpdateView.as_view(), name="song-update"
    ),
    path(
        "songs/<int:pk>/delete/", SongDeleteView.as_view(), name="song-delete"
    ),
    path("instruments/", InstrumentListView.as_view(), name="instrument-list"),
    path(
        "instruments/create/",
        InstrumentCreateView.as_view(),
        name="instrument-create"
    ),
    path(
        "instruments/<int:pk>/update/",
        InstrumentUpdateView.as_view(),
        name="instrument-update"
    ),
    path(
        "instruments/<int:pk>/delete/",
        InstrumentDeleteView.as_view(),
        name="instrument-delete"
    ),
    path("genres/", GenreListView.as_view(), name="genre-list"),
    path(
        "genres/create/",
        GenreCreateView.as_view(),
        name="genre-create"
    ),
    path(
        "genres/<int:pk>/update/",
        GenreUpdateView.as_view(),
        name="genre-update"
    ),
    path(
        "genres/<int:pk>/delete/",
        GenreDeleteView.as_view(),
        name="genre-delete"
    ),
]

app_name = "catalog"
