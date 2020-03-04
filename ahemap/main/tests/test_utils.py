from django.test import TestCase
from ahemap.main.utils import sanitize, validate_state


class UtilsTest(TestCase):

    def test_sanitize(self):
        self.assertEquals(sanitize('s\0s'), '')
        self.assertEquals(sanitize('\x00s\x00s'), '')
        self.assertEquals(sanitize('s\0s\x00'), '')
        self.assertEquals(sanitize('query'), 'query')

    def test_validate_state(self):
        self.assertFalse(validate_state(''))
        self.assertFalse(validate_state('NYC'))
        self.assertTrue(validate_state('NY'))
