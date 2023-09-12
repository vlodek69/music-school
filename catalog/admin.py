from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from catalog.models import (
    Musician,
    Instrument,
    Genre,
    Performance,
    Band,
    Song,
    Album
)


@admin.register(Musician)
class MusicianAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "full_name",
        "pseudonym",
    )
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": (
            "full_name",
            "pseudonym",
            "instruments",
        )}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "full_name",
                        "pseudonym",
                        "instruments",
                    )
                },
            ),
        )
    )


admin.site.register(Instrument)
admin.site.register(Genre)
admin.site.register(Performance)
admin.site.register(Band)
admin.site.register(Song)
admin.site.register(Album)
