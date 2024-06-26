from json import loads

from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls.base import reverse

from ahemap.main.forms import InstitutionImportForm
from ahemap.main.models import Institution
from ahemap.main.tests.factories import InstitutionFactory
from ahemap.main.views import SaveView, InstitutionImportView, BrowseView


class BasicTest(TestCase):
    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_smoketest(self):
        response = self.client.get("/smoketest/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PASS')


class BrowseViewTest(TestCase):

    def test_valid_context(self):
        ctx = {'a': 'false', 'b': '', 'c': 'true', 'd': 'something'}
        ctx = BrowseView().valid_context(ctx)

        self.assertEqual(ctx, {'c': 'true', 'd': 'something'})

    def test_get_context_data(self):
        url = reverse('browse-view')
        response = self.client.get(url)
        self.assertEqual(response.context_data['base_url'], '/browse/?&page=')
        self.assertEqual(response.context_data['twoyear'], 'false')
        self.assertEqual(response.context_data['fouryear'], 'false')
        self.assertEqual(response.context_data['public'], 'false')
        self.assertEqual(response.context_data['private'], 'false')
        self.assertEqual(response.context_data['state'], '')
        self.assertEqual(response.context_data['population'], '')
        self.assertEqual(response.context_data['query'], '')
        self.assertEqual(response.context_data['yellowribbon'], '')

    def test_get_null_bytes(self):
        params = ('fouryear=true&populationdata=&private=true&public=true'
                  '&q=%00&state=data&twoyear=trye')
        url = '{}?{}'.format(reverse('browse-view'), params)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['twoyear'], 'trye')
        self.assertEqual(response.context_data['fouryear'], 'true')
        self.assertEqual(response.context_data['public'], 'true')
        self.assertEqual(response.context_data['private'], 'true')
        self.assertEqual(response.context_data['state'], 'data')
        self.assertEqual(response.context_data['population'], '')
        self.assertEqual(response.context_data['query'], '\x00')
        self.assertEqual(response.context_data['yellowribbon'], '')


class InstitutionViewSetTest(TestCase):

    def setUp(self):
        self.inst1 = InstitutionFactory()
        self.inst2 = InstitutionFactory()

    def test_list(self):
        url = '/api/institution/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 2)
        self.assertEqual(the_json[0]['id'], self.inst1.id)
        self.assertEqual(the_json[1]['id'], self.inst2.id)

    def test_filter_list(self):
        url = '/api/institution/?q={}'.format(self.inst1.title)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 1)
        self.assertEqual(the_json[0]['id'], self.inst1.id)

    def test_filter_program_duration(self):
        self.inst2.two_year_program = True
        self.inst2.four_year_program = False
        self.inst2.save()

        url = '/api/institution/?twoyear=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 1)
        self.assertEqual(the_json[0]['id'], self.inst2.id)

        url = '/api/institution/?fouryear=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 1)
        self.assertEqual(the_json[0]['id'], self.inst1.id)

        url = '/api/institution/?twoyear=true&fouryear=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 2)
        self.assertEqual(the_json[0]['id'], self.inst1.id)
        self.assertEqual(the_json[1]['id'], self.inst2.id)

    def test_filter_yellow_ribbon(self):
        self.inst2.yellow_ribbon = False
        self.inst2.save()

        url = '/api/institution/?yellowribbon=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 1)
        self.assertEqual(the_json[0]['id'], self.inst1.id)

        url = '/api/institution/?yellowribbon='
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 2)
        self.assertEqual(the_json[0]['id'], self.inst1.id)
        self.assertEqual(the_json[1]['id'], self.inst2.id)

    def test_filter_public_private(self):
        private_institution = InstitutionFactory(private=True)

        url = '/api/institution/?public=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 2)
        self.assertEqual(the_json[0]['id'], self.inst1.id)
        self.assertEqual(the_json[1]['id'], self.inst2.id)

        url = '/api/institution/?private=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 1)
        self.assertEqual(the_json[0]['id'], private_institution.id)

        url = '/api/institution/?public=true&private=true'
        response = self.client.get(url)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 3)

        url = '/api/institution/?public=false&private=false'
        response = self.client.get(url)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 3)

    def test_filter_by_population(self):
        small_inst = InstitutionFactory(undergraduate_population=1000)
        url = '/api/institution/?population=small'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 1)
        self.assertEqual(the_json[0]['id'], small_inst.id)

        url = '/api/institution/?population=medium'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 2)
        self.assertEqual(the_json[0]['id'], self.inst1.id)
        self.assertEqual(the_json[1]['id'], self.inst2.id)

        large_inst = InstitutionFactory(undergraduate_population=10001)
        url = '/api/institution/?population=large'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 1)
        self.assertEqual(the_json[0]['id'], large_inst.id)

    def test_filter_state(self):
        url = '/api/institution/?state=NJ'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 0)

        url = '/api/institution/?state=NY'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(len(the_json), 2)
        self.assertEqual(the_json[0]['id'], self.inst1.id)
        self.assertEqual(the_json[1]['id'], self.inst2.id)

    def test_get(self):
        url = '/api/institution/{}/'.format(self.inst1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEqual(the_json['id'], self.inst1.id)

    def test_post(self):
        url = '/api/institution/{}/'.format(self.inst1.id)
        response = self.client.post(url, {'id': self.inst1.id, 'title': 'foo'})
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        url = '/api/institution/{}/'.format(self.inst1.id)
        response = self.client.put(url, {'id': self.inst1.id, 'title': 'foo'})
        self.assertEqual(response.status_code, 403)


class InstitutionImportViewTest(TestCase):

    def setUp(self):
        self.view = InstitutionImportView()
        self.view.request = RequestFactory().post('/', {})

        setattr(self.view.request, 'session', 'session')
        self.messages = FallbackStorage(self.view.request)
        setattr(self.view.request, '_messages', self.messages)

    def test_get_form_kwargs(self):
        self.assertTrue('request' in self.view.get_form_kwargs())

    def test_get_success_url(self):
        self.view.total = 10

        self.assertEqual(self.view.get_success_url(),
                         '/admin/import/institution/')
        self.assertEqual('10 institutions imported.',
                         self.messages._queued_messages[0].message)

    def test_form_valid(self):
        fields = [
            b'123', b'admin_name', b'admin@email.com', b'7777777777',
            b'Example', b'https://www.columbia.edu', b'0',
            b'Private', b'2 year', b'https://www.columbia.edu/foo.png',
            b'address', b'city', b'NY', b'40.8075', b'-73.9626',
            b'10', b'20', b'30', b'40', b'https://www.columbia.edu',
            b'Yes', b'No', b'Yes', b'standardized_test_notes', b'notes',
            b'Yes', b'National', b'', b'No', b'No', b'Yes',
            b'Yes', b'10', b'10000', b'No', b'Yes',
            b'Yes', b'vet_grants_scholarships_notes', b'28000'
        ]
        content = b',' * (len(Institution.objects.FIELD_MAPPING) - 1) + b'\r\n'
        content += b','.join(fields)

        form = InstitutionImportForm(request=self.view.request)
        form._errors = {}

        csv_file = SimpleUploadedFile('file.csv', content)
        form.cleaned_data = {'csvfile': csv_file}
        form.request.FILES['csvfile'] = csv_file

        self.view.form_valid(form)
        Institution.objects.get(external_id=123)


class SaveViewTest(TestCase):

    def setUp(self):
        self.inst1 = InstitutionFactory()
        self.inst2 = InstitutionFactory()
        self.inst3 = InstitutionFactory()

    def test_get_row(self):
        row = SaveView().get_row(self.inst1)

        expected = [
            self.inst1.title, '', 'New York', 'NY', 'https://ctl.columbia.edu',
            None, 'Public', 20000, 10000, None, None, None, None, False, True,
            True, True, None, True, True, True, True, True, True, True, True,
            None, True, None, None, None]
        self.assertEqual(expected, row)

    def test_get_rows(self):
        rows = SaveView().get_rows(Institution.objects.all().order_by('id'))

        self.assertEqual(next(rows)[0], 'Institution')
        self.assertEqual(next(rows)[0], self.inst1.title)
        self.assertEqual(next(rows)[0], self.inst2.title)
        self.assertEqual(next(rows)[0], self.inst3.title)

    def test_post(self):
        url = reverse('save-view')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)

    def test_get_filter(self):
        url = reverse('save-view')
        response = self.client.get(url, {'q': self.inst1.title})
        self.assertEqual(response.status_code, 200)

        value = next(response.streaming_content)
        self.assertTrue(value.startswith(b'Institution,Address,City,State'))

        value = next(response.streaming_content)
        self.assertTrue(value.startswith(str.encode(self.inst1.title)))

        with self.assertRaises(StopIteration):
            next(response.streaming_content)

    def test_get_site(self):
        url = reverse('save-view')
        response = self.client.get(url, {'siteid': self.inst2.id})
        self.assertEqual(response.status_code, 200)

        value = next(response.streaming_content)
        self.assertTrue(value.startswith(b'Institution,Address,City,State'))

        value = next(response.streaming_content)
        self.assertTrue(value.startswith(str.encode(self.inst2.title)))

        with self.assertRaises(StopIteration):
            next(response.streaming_content)
