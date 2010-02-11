import unittest

from rdf.resource import Resource
from rdf.blanknode import BlankNode


class TestBlankNode(unittest.TestCase):
    def setUp(self):
        self.b1 = BlankNode('b1')
        self.b2 = BlankNode()

    def test_is_resource(self):
        self.assert_(isinstance(self.b1, Resource))
    
    def test_is_blank_node(self):
        self.assert_(isinstance(self.b1, BlankNode))
        self.assert_(isinstance(self.b2, BlankNode))

    def test_constructor_sets_node_id(self):
        self.assertEqual(self.b1.node_id, 'b1')

    def test_default_node_id_is_none(self):
        self.assertEqual(self.b2.node_id, None)

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.b1), "BlankNode('b1')")

    def test_repr_without_node_id_omits_argument(self):
        self.assertEqual(repr(self.b2), "BlankNode()")

    def test_equal_to_blank_node_with_same_node_id(self):
        self.assertEqual(self.b1, BlankNode('b1'))

    def test_hash_equal_to_blank_node_with_same_node_id(self):
        self.assertEqual(hash(self.b1), hash(BlankNode('b1')))

    def test_not_equal_to_blank_node_with_different_node_id(self):
        self.assertNotEqual(self.b1, BlankNode('b2'))

    def test_hash_not_equal_to_blank_node_with_different_node_id(self):
        self.assertNotEqual(hash(self.b1), hash(BlankNode('b2')))

    def test_not_equal_to_blank_node_without_node_id(self):
        self.assertNotEqual(self.b2, BlankNode())

    def test_hash_not_equal_to_blank_node_without_node_id(self):
        self.assertNotEqual(hash(self.b2), hash(BlankNode()))

    def test_equal_to_same_instance(self):
        self.assertEqual(self.b2, self.b2)

    def test_hash_equal_to_hash_of_same_instance(self):
        self.assertEqual(hash(self.b2), hash(self.b2))

    def test_not_equal_to_string(self):
        self.assertNotEqual(self.b1, 'b1')

    def test_resource_without_uri_is_blank_node(self):
        self.assert_(isinstance(Resource(), BlankNode))

