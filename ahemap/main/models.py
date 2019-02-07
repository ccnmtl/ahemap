from django.contrib.gis.db.models.fields import PointField
from django.db import models


class Institution(models.Model):
    title = models.TextField(unique=True)
    latlng = PointField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
