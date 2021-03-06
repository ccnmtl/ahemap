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


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "user%03d" % n)
    password = factory.PostGenerationMethodCall('set_password', 'test')


class InstitutionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Institution

    title = factory.Sequence(lambda n: "site%03d" % n)
    latlng = FuzzyPoint()

    external_id = factory.Sequence(lambda n: n)

    address = ''
    city = 'New York'
    state = 'NY'

    website_url = 'https://ctl.columbia.edu'

    private = False

    student_population = 20000
    undergraduate_population = 10000

    accredited = True

    standardized_test_required = True

    vet_center = True
    sva_chapter = True

    clep_credits_accepted = True
    jst_credits_accepted = True
    dsst_credits_accepted = True
    online_credits_accepted = True
    application_fee_waived = True

    vet_grants_scholarships = True

    yellow_ribbon = True

    four_year_program = True
    two_year_program = False
