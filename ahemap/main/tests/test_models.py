from django.test import TestCase

from ahemap.main.models import Institution
from ahemap.main.tests.factories import InstitutionFactory


class InstitutionTest(TestCase):

    fields = [
        '123', '', '', '',
        'Example', 'https://www.columbia.edu', '0',
        'Private', '2 year', 'https://www.columbia.edu/foo.png',
        'address', 'city', 'NY', '40.8075', '-73.9626',
        '10', '20', '30', '40', 'https://www.columbia.edu',
        'Yes', 'No', 'Yes', 'standardized_test_notes', 'notes',
        'Yes', 'National', '', 'No', 'No', 'Yes',
        'Yes', '10', '10000', 'No', 'Yes',
        'Yes', 'vet_grants_scholarships_notes', '10000'
    ]

    def test_factory(self):
        inst = InstitutionFactory()
        self.assertIsNotNone(inst.latlng)

    def test_set_program_duration(self):
        inst = InstitutionFactory()

        inst.set_program_duration('')
        self.assertFalse(inst.two_year_program)
        self.assertFalse(inst.four_year_program)

        inst.set_program_duration('4 year')
        self.assertFalse(inst.two_year_program)
        self.assertTrue(inst.four_year_program)

        inst.set_program_duration('2 year, 4 Year')
        self.assertTrue(inst.two_year_program)
        self.assertTrue(inst.four_year_program)

    def test_set_latitude(self):
        inst = Institution()
        inst.set_latitude('40.8075')
        self.assertEqual(inst.latlng.coords[0], 40.8075)
        self.assertEqual(inst.latlng.coords[1], 0)

        inst.set_longitude('-73.9626')
        self.assertEqual(inst.latlng.coords[0], 40.8075)
        self.assertEqual(inst.latlng.coords[1], -73.9626)

    def test_set_longitude(self):
        inst = Institution()
        inst.set_longitude('-73.9626')
        self.assertEqual(inst.latlng.coords[0], 0)
        self.assertEqual(inst.latlng.coords[1], -73.9626)

        inst.set_latitude('40.8075')
        self.assertEqual(inst.latlng.coords[0], 40.8075)
        self.assertEqual(inst.latlng.coords[1], -73.9626)

    def test_set_accreditation_type(self):
        inst = InstitutionFactory()
        inst.set_accreditation_type('Regional')
        self.assertEqual(inst.accreditation_type, 'R')
        inst.set_accreditation_type('National')
        self.assertEqual(inst.accreditation_type, 'N')
        inst.set_accreditation_type('')
        self.assertIsNone(inst.accreditation_type)

    def test_find_or_create_by_external_id(self):
        i = InstitutionFactory()
        self.assertEqual(
            i,
            Institution.objects.find_or_create_by_external_id(i.external_id))

        i2 = Institution.objects.find_or_create_by_external_id(123)
        self.assertNotEqual(i, i2)
        self.assertEqual(i2.external_id, 123)

    def test_set_field_value(self):
        i = InstitutionFactory()

        Institution.objects._set_field_value(
            i, 'set_institution_type', 'Public')
        self.assertFalse(i.private)

        Institution.objects._set_field_value(i, 'set_latitude', '30.000')
        self.assertEqual(i.latlng.coords[0], 30)

        Institution.objects._set_field_value(i, 'set_longitude', '-30.123')
        self.assertEqual(i.latlng.coords[1], -30.123)

        Institution.objects._set_field_value(
            i, 'set_program_duration', '2 year, 4 year')
        self.assertTrue(i.two_year_program)
        self.assertTrue(i.four_year_program)

        Institution.objects._set_field_value(i, 'student_population', '10000')
        self.assertEqual(i.student_population, 10000)

        Institution.objects._set_field_value(i, 'student_population', '10,000')
        self.assertEqual(i.student_population, 10000)

        Institution.objects._set_field_value(i, 'city', 'foo')
        self.assertEqual(i.city, 'foo')

    def test_create(self):
        i = Institution.objects.update_or_create(self.fields)
        self.assertEqual(i.external_id, 123)
        self.assertEqual(i.title, 'Example')
        self.assertEqual(i.website_url, 'https://www.columbia.edu')
        self.assertEqual(i.student_population, 0)
        self.assertTrue(i.private)
        self.assertTrue(i.two_year_program)
        self.assertFalse(i.four_year_program)
        self.assertEqual(i.image, 'https://www.columbia.edu/foo.png')
        self.assertEqual(i.address, 'address')
        self.assertEqual(i.city, 'city')
        self.assertEqual(i.state, 'NY')
        self.assertEqual(i.latlng.coords[0], 40.8075)
        self.assertEqual(i.latlng.coords[1], -73.9626)
        self.assertEqual(i.undergrad_vet_population, 10)
        self.assertEqual(i.undergrad_vet_graduation_rate, 20)
        self.assertEqual(i.grad_vet_population, 30)
        self.assertEqual(i.grad_vet_graduation_rate, 40)
        self.assertEqual(i.admissions_url, 'https://www.columbia.edu',)
        self.assertTrue(i.vet_center)
        self.assertFalse(i.sva_chapter)
        self.assertTrue(i.standardized_test_required)
        self.assertEqual(i.standardized_test_notes, 'standardized_test_notes')
        self.assertEqual(i.notes, 'notes')
        self.assertTrue(i.accredited)
        self.assertEqual(i.accreditation_type, 'N')
        self.assertEqual(i.regional_accreditor, None)
        self.assertFalse(i.clep_credits_accepted)
        self.assertFalse(i.jst_credits_accepted)
        self.assertTrue(i.dsst_credits_accepted)
        self.assertTrue(i.yellow_ribbon)
        self.assertEqual(i.yellow_ribbon_slots, '10')
        self.assertEqual(i.yellow_ribbon_contribution, '10000')
        self.assertFalse(i.online_credits_accepted)
        self.assertTrue(i.application_fee_waived)
        self.assertTrue(i.vet_grants_scholarships)
        self.assertEqual(
            i.vet_grants_scholarships_notes, 'vet_grants_scholarships_notes')

    def test_update(self):
        i = InstitutionFactory()
        self.assertTrue(i.title.startswith('site'))

        self.fields[0] = str(i.external_id)
        Institution.objects.update_or_create(self.fields)

        i.refresh_from_db()
        self.assertEqual(i.external_id, i.external_id)
        self.assertEqual(i.title, 'Example')
        self.assertEqual(i.website_url, 'https://www.columbia.edu')
        self.assertEqual(i.student_population, 0)
        self.assertTrue(i.private)
        self.assertTrue(i.two_year_program)
        self.assertFalse(i.four_year_program)
        self.assertEqual(i.image, 'https://www.columbia.edu/foo.png')
        self.assertEqual(i.address, 'address')
        self.assertEqual(i.city, 'city')
        self.assertEqual(i.state, 'NY')
        self.assertEqual(i.latlng.coords[0], 40.8075)
        self.assertEqual(i.latlng.coords[1], -73.9626)
        self.assertEqual(i.undergrad_vet_population, 10)
        self.assertEqual(i.undergrad_vet_graduation_rate, 20)
        self.assertEqual(i.grad_vet_population, 30)
        self.assertEqual(i.grad_vet_graduation_rate, 40)
        self.assertEqual(i.admissions_url, 'https://www.columbia.edu',)
        self.assertTrue(i.vet_center)
        self.assertFalse(i.sva_chapter)
        self.assertTrue(i.standardized_test_required)
        self.assertEqual(i.standardized_test_notes, 'standardized_test_notes')
        self.assertEqual(i.notes, 'notes')
        self.assertTrue(i.accredited)
        self.assertEqual(i.accreditation_type, 'N')
        self.assertEqual(i.regional_accreditor, None)
        self.assertFalse(i.clep_credits_accepted)
        self.assertFalse(i.jst_credits_accepted)
        self.assertTrue(i.dsst_credits_accepted)
        self.assertTrue(i.yellow_ribbon)
        self.assertEqual(i.yellow_ribbon_slots, '10')
        self.assertEqual(i.yellow_ribbon_contribution, '10000')
        self.assertFalse(i.online_credits_accepted)
        self.assertTrue(i.application_fee_waived)
        self.assertTrue(i.vet_grants_scholarships)
        self.assertEqual(
            i.vet_grants_scholarships_notes, 'vet_grants_scholarships_notes')
