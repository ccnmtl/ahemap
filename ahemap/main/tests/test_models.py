from django.test import TestCase
from ahemap.main.tests.factories import InstitutionFactory


class InstitutionTest(TestCase):

    def test_factory(self):
        inst = InstitutionFactory()
        self.assertIsNotNone(inst.latlng)
