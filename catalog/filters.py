from django_filters import FilterSet

from catalog.models import Performance


class SongInstrumentFilter(FilterSet):
    class Meta:
        model = Performance
        fields = ["instruments"]
