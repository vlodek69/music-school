from django_filters import FilterSet

from catalog.models import Performance, Song


class SongInstrumentFilter(FilterSet):
    class Meta:
        model = Performance
        fields = ["instruments"]

    def __init__(self, *args, **kwargs):
        super(SongInstrumentFilter, self).__init__(*args, **kwargs)
        self.filters["instruments"]._label = "Filter by instruments"


class SongBandFilterDistinct(FilterSet):
    class Meta:
        model = Song
        fields = ["albums__band"]

    def __init__(self, *args, **kwargs):
        super(SongBandFilterDistinct, self).__init__(*args, **kwargs)
        self.filters["albums__band"]._label = "Filter by band"

    @property
    def qs(self):
        parent = super().qs

        return parent.distinct()
