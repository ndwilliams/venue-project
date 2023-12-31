# Generated by Django 4.2.8 on 2023-12-21 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('genre', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doors_open', models.DateTimeField()),
                ('show_starts', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='concerts_this_band_plays', to='venueapi.band')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue_outside_image_url', models.URLField(blank=True, max_length=500, null=True)),
                ('venue_inside_image_url', models.URLField(blank=True, max_length=500, null=True)),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('capacity', models.IntegerField(blank=True, null=True)),
                ('about_section', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Opener',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='times_band_opened', to='venueapi.band')),
                ('concert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='openers', to='venueapi.concert')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='concert_favorites', to='venueapi.concert')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='concert',
            name='opening_bands',
            field=models.ManyToManyField(related_name='concerts_opened', through='venueapi.Opener', to='venueapi.band'),
        ),
        migrations.AddField(
            model_name='concert',
            name='users_who_favorited',
            field=models.ManyToManyField(related_name='concerts_favorited', through='venueapi.Favorite', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='concert',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='concerts_at_this_venue', to='venueapi.venue'),
        ),
    ]
