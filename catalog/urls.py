from django.urls import path

from catalog.views import index, MusicianListView

urlpatterns = [
    path("", index, name="index"),
    path("musicians/", MusicianListView.as_view(), name="musician-list"),
]

app_name = "catalog"
