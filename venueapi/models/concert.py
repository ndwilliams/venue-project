from django.db import models
from django.contrib.auth.models import User

class Concert(models.Model):
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE, related_name='concerts_at_this_venue')
    band = models.ForeignKey('Band', on_delete=models.CASCADE, related_name='concerts_this_band_plays')
    doors_open = models.DateTimeField(auto_now_add=False)
    show_starts = models.DateTimeField(auto_now_add=False)
    users_who_favorited = models.ManyToManyField(User, through='Favorite', related_name='concerts_favorited')
    opening_bands = models.ManyToManyField('Band', through='Opener', related_name='concerts_opened')