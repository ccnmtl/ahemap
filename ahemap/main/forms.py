import csv
import io

from django import forms
from django.utils.encoding import force_text, DjangoUnicodeDecodeError

from ahemap.main.models import Institution


class InstitutionImportForm(forms.Form):
    INVALID_FILE_FORMAT = ("The selected file is not formatted properly. "
                           "Please select a valid data file.")
    INVALID_ENCODING = (
        "The selected file is not encoded properly. Batch files must be "
        "encoded using the UTF-8 standard to ensure special characters are "
        "translated correctly.<br /><br /> The full error is:<br />{}.")

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
        except UnicodeDecodeError:
            self._errors['csvfile'] = self.error_class([
                self.INVALID_FILE_FORMAT])
        except csv.Error:
            self._errors['csvfile'] = self.error_class([
                self.INVALID_FILE_FORMAT])
