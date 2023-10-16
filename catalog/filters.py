from django_filters import FilterSet

from catalog.models import Performance, Song


class SongInstrumentFilter(FilterSet):
    class Meta:
        model = Performance
        fields = ["instruments"]


class SongDistinctFilter(FilterSet):
    class Meta:
        model = Song
        fields = ["albums__band"]

    @property
    def qs(self):
        parent = super().qs

        return parent.distinct()
