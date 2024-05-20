from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import RequestFactory
from django.test.testcases import TestCase

from ahemap.main.forms import InstitutionImportForm
from ahemap.main.models import Institution


class InstitutionFormTest(TestCase):

    def setUp(self):
        self.request = RequestFactory()
        self.form = InstitutionImportForm(request=self.request)
        self.form._errors = {}
        self.form.cleaned_data = {}

    def test_init(self):
        self.assertEqual(self.form.request, self.request)

    def test_validate_column_count(self):
        self.assertFalse(self.form.validate_column_count([]))

    def test_clean(self):
        self.form.clean()
        self.assertTrue('csvfile' in self.form._errors.keys())

    def test_form_clean_invalid_file_format(self):
        content = b',' * (len(Institution.objects.FIELD_MAPPING) - 1) + b'\r\n'
        content += b'1,2,3,'
        csvfile = SimpleUploadedFile('file.csv', content)

        self.form.cleaned_data = {'csvfile': csvfile}
        setattr(self.form.request, 'FILES', {'csvfile': csvfile})

        self.form.clean()
        self.assertTrue('csvfile' in self.form._errors.keys())
        self.assertEqual(self.form._errors['csvfile'],
                         [self.form.INVALID_FILE_FORMAT])

    def test_form_clean_valid_file_format(self):
        content = b',' * (len(Institution.objects.FIELD_MAPPING) - 1) + b'\r\n'
        content += b',' * (len(Institution.objects.FIELD_MAPPING) - 1)
        csvfile = SimpleUploadedFile('file.csv', content)

        self.form.cleaned_data = {'csvfile': csvfile}
        setattr(self.form.request, 'FILES', {'csvfile': csvfile})

        self.form.clean()
        self.assertFalse('csvfile' in self.form._errors.keys())

    def test_validate_url(self):
        row = ['a', 'a', 'a', 'a', 'a', 'a' * 300]

        self.assertFalse(self.form.validate_url_field(row, 'website_url'))
        self.assertTrue('website_url' in self.form._errors.keys())
