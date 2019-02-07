from django.contrib import admin
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos.point import Point
from django.forms.widgets import MultiWidget, TextInput

from ahemap.main.models import Institution


class LatLongWidget(MultiWidget):
    """
    A Widget that splits Point input into latitude/longitude text inputs.
    https://stackoverflow.com/questions/19231109/
    geodjango-pointfield-admin-visualization
    by César
    """

    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (TextInput(attrs=attrs),
                   TextInput(attrs=attrs))
        super(LatLongWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return tuple(value.coords)
        return (None, None)

    def value_from_datadict(self, data, files, name):
        mylat = data[name + '_0']
        mylong = data[name + '_1']

        try:
            point = Point(float(mylat), float(mylong))
        except ValueError:
            return ''

        return point


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    formfield_overrides = {
        geomodels.PointField: {'widget': LatLongWidget},
    }
