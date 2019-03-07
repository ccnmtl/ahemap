from json import loads

from django.test import TestCase
from django.urls.base import reverse

from ahemap.main.models import Institution
from ahemap.main.tests.factories import InstitutionFactory
from ahemap.main.views import SaveView


class BasicTest(TestCase):
    def test_root(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)

    def test_smoketest(self):
        response = self.client.get("/smoketest/")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'PASS')


class InstitutionViewSetTest(TestCase):

    def setUp(self):
        self.inst1 = InstitutionFactory()
        self.inst2 = InstitutionFactory()

    def test_list(self):
        url = '/api/institution/'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEquals(len(the_json), 2)
        self.assertEquals(the_json[0]['id'], self.inst1.id)
        self.assertEquals(the_json[1]['id'], self.inst2.id)

    def test_filter_list(self):
        url = '/api/institution/?q={}'.format(self.inst1.title)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEquals(len(the_json), 1)
        self.assertEquals(the_json[0]['id'], self.inst1.id)

    def test_filter_program_duration(self):
        url = '/api/institution/?twoyear=true'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEquals(len(the_json), 0)

        url = '/api/institution/?fouryear=true'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEquals(len(the_json), 2)

    def test_filter_state(self):
        url = '/api/institution/?state=NJ'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEquals(len(the_json), 0)

        url = '/api/institution/?state=NY'
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEquals(len(the_json), 2)
        self.assertEquals(the_json[0]['id'], self.inst1.id)
        self.assertEquals(the_json[1]['id'], self.inst2.id)

    def test_get(self):
        url = '/api/institution/{}/'.format(self.inst1.id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        the_json = loads(response.content.decode('utf-8'))
        self.assertEquals(the_json['id'], self.inst1.id)

    def test_post(self):
        url = '/api/institution/{}/'.format(self.inst1.id)
        response = self.client.post(url, {'id': self.inst1.id, 'title': 'foo'})
        self.assertEquals(response.status_code, 403)

    def test_put(self):
        url = '/api/institution/{}/'.format(self.inst1.id)
        response = self.client.put(url, {'id': self.inst1.id, 'title': 'foo'})
        self.assertEquals(response.status_code, 403)


class SaveViewTest(TestCase):

    def setUp(self):
        self.inst1 = InstitutionFactory()
        self.inst2 = InstitutionFactory()
        self.inst3 = InstitutionFactory()

    def test_get_row(self):
        row = SaveView().get_row(self.inst1)

        expected = [
            self.inst1.title, '', 'New York', 'NY', 'https://ctl.columbia.edu',
            None, 'Public', 20000, None, None, None, None, None, True, True,
            True, None, True, True, True, True, True, True, True, True, None,
            True, None, None, None]
        self.assertEquals(expected, row)

    def test_get_rows(self):
        rows = SaveView().get_rows(Institution.objects.all().order_by('id'))

        self.assertEquals(next(rows)[0], 'Institution')
        self.assertEquals(next(rows)[0], self.inst1.title)
        self.assertEquals(next(rows)[0], self.inst2.title)
        self.assertEquals(next(rows)[0], self.inst3.title)

    def test_get(self):
        url = reverse('save-view')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 405)

    def test_post(self):
        url = reverse('save-view')
        response = self.client.post(url, {'q': self.inst1.title})
        self.assertEquals(response.status_code, 200)

        value = next(response.streaming_content)
        self.assertTrue(value.startswith(b'Institution,Address,City,State'))

        value = next(response.streaming_content)
        self.assertTrue(value.startswith(str.encode(self.inst1.title)))

        with self.assertRaises(StopIteration):
            next(response.streaming_content)
