from django.urls import path

from catalog.views import index, MusicianListView, BandListView, SongListView

urlpatterns = [
    path("", index, name="index"),
    path("musicians/", MusicianListView.as_view(), name="musician-list"),
    path("bands/", BandListView.as_view(), name="band-list"),
    path("songs/", SongListView.as_view(), name="song-list"),
]

app_name = "catalog"
