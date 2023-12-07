from django.db import models

class Band(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)