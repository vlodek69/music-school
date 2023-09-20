from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from catalog.models import Musician, Song, Performance, Instrument, Album, \
    Genre


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


class SongCreationForm(forms.ModelForm):
    song = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Song
        fields = "__all__"


class PerformanceCreationForm(forms.ModelForm):
    performance = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Performance
        fields = "__all__"


class InstrumentCreationForm(forms.ModelForm):
    instrument = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Instrument
        fields = "__all__"


class AlbumCreationForm(forms.ModelForm):
    album = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Album
        fields = "__all__"


class GenreCreationForm(forms.ModelForm):
    genre = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Genre
        fields = "__all__"
