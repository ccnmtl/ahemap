from json import loads

from django.test import TestCase

from ahemap.main.tests.factories import InstitutionFactory


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
