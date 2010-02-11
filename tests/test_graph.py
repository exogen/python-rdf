import unittest

from rdf.uri import URI
from rdf.blanknode import BlankNode
from rdf.literal import Literal
from rdf.graph import Graph


class TestEmptyGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

    def test_is_set(self):
        self.assert_(isinstance(self.graph, set))

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.graph), "Graph()")

class TestSimpleGraph(unittest.TestCase):
    def setUp(self):
        self.triple = (URI('http://www.example.org/index.html'),
                       URI('http://purl.org/dc/elements/1.1/creator'),
                       URI('http://www.example.org/staffid/85740'))
        self.graph = Graph([self.triple])

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.graph), "Graph({{{!r}}})".format(self.triple))

class TestGroundGraph(unittest.TestCase):
    def setUp(self):
        self.triples = [(URI('http://www.example.org/index.html'),
                         URI('http://purl.org/dc/elements/1.1/creator'),
                         URI('http://www.example.org/staffid/85740')),
                        (URI('http://www.example.org/staffid/85740'),
                         URI('http://xmlns.com/foaf/0.1/name'),
                         Literal("John Smith"))]
        self.graph = Graph(self.triples)

    def test_is_ground_with_no_blank_nodes_is_true(self):
        self.assert_(self.graph.is_ground())

    def test_equal_to_graph_with_same_triples(self):
        self.assertEqual(self.graph, Graph(self.triples))

    def test_not_equal_to_graph_with_different_triples(self):
        triples = [(URI('http://www.example.org/index.html'),
                    URI('http://purl.org/dc/elements/1.1/creator'),
                    URI('http://www.example.org/staffid/85740')),
                   (URI('http://www.example.org/staffid/85740'),
                    URI('http://xmlns.com/foaf/0.1/name'),
                    Literal("John Doe"))]
        self.assertNotEqual(self.graph, Graph(triples))

class TestUngroundGraph(unittest.TestCase):
    def setUp(self):
        self.triples = [(URI('http://www.example.org/index.html'),
                         URI('http://purl.org/dc/elements/1.1/creator'),
                         BlankNode('john')),
                        (BlankNode('john'),
                         URI('http://xmlns.com/foaf/0.1/name'),
                         Literal("John Smith"))]
        self.graph = Graph(self.triples)

    def test_is_ground_with_blank_nodes_is_false(self):
        self.assertEqual(self.graph.is_ground(), False)

    def test_is_equal_to_graph_with_valid_bijection(self):
        triples = [(URI('http://www.example.org/index.html'),
                    URI('http://purl.org/dc/elements/1.1/creator'),
                    BlankNode('person')),
                   (BlankNode('person'),
                    URI('http://xmlns.com/foaf/0.1/name'),
                    Literal("John Smith"))]
        self.assertEqual(self.graph, Graph(triples))

