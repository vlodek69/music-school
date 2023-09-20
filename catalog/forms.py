from django.contrib.auth.forms import UserCreationForm

from catalog.models import Musician


class MusicianCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Musician
        fields = UserCreationForm.Meta.fields + (
            "full_name",
            "pseudonym",
        )
