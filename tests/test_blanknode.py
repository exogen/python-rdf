import unittest

from rdf.resource import Resource
from rdf.blanknode import BlankNode


class TestBlankNode(unittest.TestCase):
    def setUp(self):
        self.b1 = BlankNode('b1')

    def test_is_resource(self):
        self.assert_(isinstance(self.b1, Resource))

    def test_is_created_with_node_id(self):
        self.assert_(isinstance(self.b1, BlankNode))

    def test_has_node_id(self):
        self.assert_(hasattr(self.b1, 'node_id'))
        self.assertEqual(self.b1.node_id, 'b1')

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.b1), "BlankNode('b1')")

    def test_equal_to_blank_node_with_same_node_id(self):
        self.assertEqual(self.b1, BlankNode('b1'))

    def test_hash_equal_to_blank_node_with_same_node_id(self):
        self.assertEqual(hash(self.b1), hash(BlankNode('b1')))

    def test_not_equal_to_blank_node_with_different_node_id(self):
        self.assertNotEqual(self.b1, BlankNode('b2'))

    def test_hash_not_equal_to_blank_node_with_different_node_id(self):
        self.assertNotEqual(hash(self.b1), hash(BlankNode('b2')))

    def test_not_equal_to_string(self):
        self.assertNotEqual(self.b1, 'b1')

    def test_resource_without_uri_is_blank_node(self):
        self.assert_(isinstance(Resource(), BlankNode))

