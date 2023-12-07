from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_favorites')
    concert = models.ForeignKey('Concert', on_delete=models.CASCADE, related_name='concert_favorites')