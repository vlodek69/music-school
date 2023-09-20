from django.urls import path

from catalog.views import index, MusicianListView, BandListView, SongListView, \
    SongDetailView, BandDetailView, MusicianDetailView, MusicianCreateView, \
    MusicianUpdateView, song_create_view, BandCreateView, album_create_view, \
    album_update_view

urlpatterns = [
    path("", index, name="index"),
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
    path("bands/", BandListView.as_view(), name="band-list"),
    path("bands/<int:pk>/", BandDetailView.as_view(), name="band-detail"),
    path("bands/create/", BandCreateView.as_view(), name="band-create"),
    path("album/create/", album_create_view, name="album-create"),
    path("album/<int:pk>/update", album_update_view, name="album-update"),
    path("songs/", SongListView.as_view(), name="song-list"),
    path("songs/<int:pk>/", SongDetailView.as_view(), name="song-detail"),
    path("songs/create/", song_create_view, name="song-create"),
]

app_name = "catalog"
