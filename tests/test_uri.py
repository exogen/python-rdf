# -*- coding: utf-8 -*-
import unittest
from xml.etree.ElementTree import QName

from rdf.resource import Resource
from rdf.blanknode import BlankNode
from rdf.uri import URI
from rdf.literal import Literal
from rdf.namespace import XSD


class TestURI(unittest.TestCase):
    def setUp(self):
        self.uri = URI('test')

    def test_is_resource(self):
        self.assert_(isinstance(self.uri, Resource))

    def test_is_string(self):
        self.assert_(isinstance(self.uri, str))

    def test_is_created_with_string(self):
        self.assert_(isinstance(self.uri, URI))

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.uri), "URI('test')")

    def test_equal_to_string(self):
        self.assertEqual(self.uri, "test")

    def test_resource_with_uri_is_uri(self):
        self.assert_(isinstance(Resource('test'), URI))

    def test_can_create_empty_uri(self):
        self.assertEqual(URI(), '')

    def test_converts_qname_to_uri(self):
        qname = QName('http://example.org/', 'test')
        self.assertEqual(URI(qname), URI('http://example.org/test'))

    def test_resource_with_qname_is_uri(self):
        qname = QName('http://example.org/', 'test')
        self.assertEqual(Resource(qname), URI('http://example.org/test'))

    def test_compares_greater_than_none(self):
        self.assert_(self.uri > None)
        self.assert_(not self.uri < None)

    def test_compares_greater_than_blank_node(self):
        bnode = BlankNode()
        self.assert_(self.uri > bnode)
        self.assert_(not self.uri < bnode)

    def test_compares_to_uri_lexicographically(self):
        self.assert_(URI('http://script.example/Latin') <
                     URI('http://script.example/Кириллица') <
                     URI('http://script.example/漢字') <
                     self.uri)
        self.assert_(self.uri > 
                     URI('http://script.example/漢字') >
                     URI('http://script.example/Кириллица') >
                     URI('http://script.example/Latin'))

    def test_compares_less_than_plain_literal(self):
        literal = Literal("a")
        self.assert_(self.uri < literal)
        self.assert_(not self.uri > literal)

    def test_compares_less_than_typed_literal(self):
        literal = Literal("1", XSD.integer)
        self.assert_(self.uri < literal)
        self.assert_(not self.uri > literal)

