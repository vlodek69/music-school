# Generated by Django 4.2.5 on 2023-10-16 16:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0003_alter_instrument_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="band",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="performance",
            options={"ordering": ["musician__full_name"]},
        ),
        migrations.AlterModelOptions(
            name="song",
            options={"ordering": ["name"]},
        ),
    ]
