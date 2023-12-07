from django.db import models

class Opener(models.Model):
    concert = models.ForeignKey('Concert', on_delete=models.CASCADE, related_name='openers')
    band = models.ForeignKey('Band', on_delete=models.CASCADE, related_name='times_band_opened')