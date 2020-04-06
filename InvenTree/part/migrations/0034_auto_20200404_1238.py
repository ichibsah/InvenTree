# Generated by Django 2.2.10 on 2020-04-04 12:38

from django.db import migrations
from django.db.utils import OperationalError, ProgrammingError

from part.models import Part
from stdimage.utils import render_variations


def create_thumbnails(apps, schema_editor):
    """
    Create thumbnails for all existing Part images.
    """

    try:
        for part in Part.objects.all():
            # Render thumbnail for each existing Part 
            if part.image:
                part.image.render_variations()
    except (OperationalError, ProgrammingError):
        # Migrations have not yet been applied - table does not exist
        print("Could not generate Part thumbnails")

class Migration(migrations.Migration):

    dependencies = [
        ('part', '0033_auto_20200404_0445'),
    ]

    operations = [
        migrations.RunPython(create_thumbnails),
    ]
