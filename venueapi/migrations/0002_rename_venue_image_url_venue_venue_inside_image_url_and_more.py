# Generated by Django 4.2.8 on 2023-12-11 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venueapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='venue',
            old_name='venue_image_url',
            new_name='venue_inside_image_url',
        ),
        migrations.AddField(
            model_name='venue',
            name='venue_outer_image_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
