import random

from django.contrib.auth.models import User
from django.contrib.gis.geos.point import Point
import factory
from factory.fuzzy import BaseFuzzyAttribute

from ahemap.main.models import Institution


class FuzzyPoint(BaseFuzzyAttribute):
    def fuzz(self):
        return Point(random.uniform(-180.0, 180.0),
                     random.uniform(-90.0, 90.0))


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "user%03d" % n)
    password = factory.PostGenerationMethodCall('set_password', 'test')


class InstitutionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Institution

    title = factory.Sequence(lambda n: "site%03d" % n)
    latlng = FuzzyPoint()
