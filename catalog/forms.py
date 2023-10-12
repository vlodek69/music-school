from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from catalog.models import (
    Musician,
    Song,
    Performance,
    Instrument,
    Album,
    Genre
)


class MusicianCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Musician
        fields = UserCreationForm.Meta.fields + (
            "full_name",
            "pseudonym",
        )


class MusicianUpdateForm(forms.ModelForm):
    class Meta:
        model = Musician
        fields = ["username", "full_name", "pseudonym"]


class MusicianSearchForm(forms.Form):
    search_input = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search by name..."
        })
    )


class SongForm(forms.ModelForm):
    song = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    performances = forms.ModelMultipleChoiceField(
        queryset=Performance.objects.select_related("musician").prefetch_related("instruments")
    )

    class Meta:
        model = Song
        fields = "__all__"


class ByNameSearchForm(forms.Form):
    search_input = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search by name..."
        })
    )


class PerformanceForm(forms.ModelForm):
    performance = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Performance
        fields = "__all__"

    def clean_instruments(self):
        return validate_unique_instruments_set(
            self.cleaned_data["musician"],
            self.cleaned_data["instruments"]
        )


def validate_unique_instruments_set(musician, instruments):
    instrument_sets = [
        list(performance.instruments.all().order_by("id")) for performance in
        Performance.objects.filter(musician=musician)
    ]
    if list(instruments.order_by("id")) in instrument_sets:
        raise ValidationError("Create unique performance for this musician")

    return instruments



class InstrumentCreationForm(forms.ModelForm):
    instrument = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Instrument
        fields = "__all__"


class AlbumForm(forms.ModelForm):
    album = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Album
        fields = "__all__"


class GenreCreationForm(forms.ModelForm):
    genre = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Genre
        fields = "__all__"
