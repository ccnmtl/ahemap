from django.contrib.gis.db.models.fields import PointField
from django.db import models


class Institution(models.Model):
    title = models.TextField(unique=True)
    latlng = PointField()
