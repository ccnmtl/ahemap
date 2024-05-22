from django.test import TestCase
from ahemap.main.utils import sanitize, validate_state


class UtilsTest(TestCase):

    def test_sanitize(self):
        self.assertEqual(sanitize('s\0s'), '')
        self.assertEqual(sanitize('\x00s\x00s'), '')
        self.assertEqual(sanitize('s\0s\x00'), '')
        self.assertEqual(sanitize('query'), 'query')

    def test_validate_state(self):
        self.assertFalse(validate_state(''))
        self.assertFalse(validate_state('NYC'))
        self.assertTrue(validate_state('NY'))
