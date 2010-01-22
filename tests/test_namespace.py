import unittest

from rdf.uri import URI
from rdf.namespace import Namespace


class TestNamespace(unittest.TestCase):
    def setUp(self):
        self.namespace = Namespace('http://example.org/')

    def test_is_namespace(self):
        self.assert_(isinstance(self.namespace, Namespace))

    def test_is_uri(self):
        self.assert_(isinstance(self.namespace, URI))

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.namespace), "Namespace('http://example.org/')")

    def test_compares_equal_to_string(self):
        self.assertEqual(self.namespace, 'http://example.org/')

    def test_compares_equal_to_uri(self):
        self.assertEqual(self.namespace, URI('http://example.org/'))

    def test_getitem_returns_new_uri(self):
        self.assertEqual(self.namespace['test'], URI('http://example.org/test'))

    def test_getitem_with_number_returns_character(self):
        self.assertEqual(self.namespace[0], 'h')

    def test_getitem_with_slice_returns_string(self):
        self.assertEqual(self.namespace[7:14], 'example')

    def test_getattr_returns_new_uri(self):
        self.assertEqual(self.namespace.test, URI('http://example.org/test'))

    def test_new_uri_is_uri_and_not_namespace(self):
        self.assert_(isinstance(self.namespace.test, URI))
        self.assert_(isinstance(self.namespace['test'], URI))
        self.assert_(not isinstance(self.namespace.test, Namespace))
        self.assert_(not isinstance(self.namespace['test'], Namespace))

