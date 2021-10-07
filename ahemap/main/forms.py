import csv
import io

from ahemap.main.models import Institution
from django import forms
from django.utils.encoding import force_text, DjangoUnicodeDecodeError


class InstitutionImportForm(forms.Form):
    INVALID_FILE_FORMAT = ("The selected file is not formatted properly. "
                           "Please select a valid data file.")
    INVALID_ENCODING = (
        "The selected file is not encoded properly. Batch files must be "
        "encoded using the UTF-8 standard to ensure special characters are "
        "translated correctly.<br /><br /> The full error is:<br />{}.")

    URL_FIELD_TOO_LONG = (
        "Row Id {}: The {} field must be less than 200 characters.")

    csvfile = forms.FileField(required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(InstitutionImportForm, self).__init__(*args, **kwargs)

    def csvfile_reader(self):
        csv_file = self.request.FILES['csvfile']
        csv_file.seek(0)
        as_string = io.StringIO(csv_file.read().decode('utf-8'))
        return csv.reader(as_string)

    def validate_column_count(self, row):
        return len(row) == len(Institution.objects.FIELD_MAPPING)

    def validate_encoding(self, row):
        for col in row:
            try:
                force_text(col)
            except DjangoUnicodeDecodeError as e:
                return False, e

        return True, ''

    def validate_url_field(self, row, field_name):
        idx = Institution.objects.FIELD_MAPPING.index(field_name)
        if len(row[idx]) <= 200:
            return True

        msg = self.URL_FIELD_TOO_LONG.format(row[0], field_name)
        self._errors[field_name] = self.error_class([msg])
        return False

    def clean(self):
        cleaned_data = super(InstitutionImportForm, self).clean()
        if 'csvfile' not in cleaned_data:
            self._errors['csvfile'] = self.error_class([
                'Please select a data file'])
            return cleaned_data

        self.validate_clean_data(cleaned_data)
        return cleaned_data

    def validate_clean_data(self, cleaned_data):
        # do some rudimentary validation on the file
        try:
            for row in self.csvfile_reader():
                if not self.validate_column_count(row):
                    self._errors['csvfile'] = self.error_class([
                        self.INVALID_FILE_FORMAT])
                    break

                valid, e = self.validate_encoding(row)
                if not valid:
                    self._errors['csvfile'] = self.error_class([
                        self.INVALID_ENCODING.format(e)])
                    break

                if not self.validate_url_field(row, 'website_url'):
                    break

                if not self.validate_url_field(row, 'image'):
                    break

                if not self.validate_url_field(row, 'admissions_url'):
                    break

        except UnicodeDecodeError:
            self._errors['csvfile'] = self.error_class([
                self.INVALID_FILE_FORMAT])

        except csv.Error:
            self._errors['csvfile'] = self.error_class([
                self.INVALID_FILE_FORMAT])
