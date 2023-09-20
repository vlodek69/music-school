from django.urls import path

from catalog.views import index, MusicianListView, BandListView, SongListView, \
    SongDetailView, BandDetailView, MusicianDetailView, MusicianCreateView, \
    MusicianUpdateView, SongCreateView

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
    path("songs/", SongListView.as_view(), name="song-list"),
    path("songs/<int:pk>/", SongDetailView.as_view(), name="song-detail"),
    path("songs/create/", SongCreateView.as_view(), name="song-create"),
]

app_name = "catalog"
