from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from catalog.models import Musician, Song


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
    class Meta:
        model = Song
        fields = "__all__"
