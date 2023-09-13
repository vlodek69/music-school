from django.urls import path

from catalog.views import index, MusicianListView, BandListView

urlpatterns = [
    path("", index, name="index"),
    path("musicians/", MusicianListView.as_view(), name="musician-list"),
    path("bands/", BandListView.as_view(), name="band-list"),
]

app_name = "catalog"
