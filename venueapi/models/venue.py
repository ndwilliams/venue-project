from django.db import models

class Venue(models.Model):
    venue_outside_image_url = models.URLField(max_length=500, null=True, blank=True)
    venue_inside_image_url = models.URLField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    about_section = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True, blank=True)