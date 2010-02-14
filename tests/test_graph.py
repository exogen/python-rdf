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

    def test_not_equal_to_set(self):
        self.assertNotEqual(self.graph, set())
        self.assertNotEqual(set(), self.graph)

class TestGroundGraph(unittest.TestCase):
    def setUp(self):
        self.triples = {(URI('http://www.example.org/index.html'),
                         URI('http://purl.org/dc/elements/1.1/creator'),
                         URI('http://www.example.org/staffid/85740')),
                        (URI('http://www.example.org/staffid/85740'),
                         URI('http://xmlns.com/foaf/0.1/name'),
                         Literal("John Lennon"))}
        self.graph = Graph(self.triples)

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.graph),
                         "Graph({!r})".format(self.triples))

    def test_is_ground_is_true(self):
        self.assertEqual(self.graph.is_ground(), True)

    def test_equal_to_graph_with_same_triples(self):
        self.assertEqual(self.graph, Graph(self.triples))

    def test_not_equal_to_graph_of_different_size(self):
        graph = Graph(list(self.triples)[0])
        self.assertNotEqual(self.graph, graph)
        self.assertNotEqual(graph, self.graph)

    def test_not_equal_to_graph_with_different_triples(self):
        graph = Graph({(URI('http://www.example.org/index.html'),
                        URI('http://purl.org/dc/elements/1.1/creator'),
                        URI('http://www.example.org/staffid/85740')),
                       (URI('http://www.example.org/staffid/85740'),
                        URI('http://xmlns.com/foaf/0.1/name'),
                        Literal("John Doe"))})
        self.assertNotEqual(self.graph, graph)
        self.assertNotEqual(graph, self.graph)

class TestUngroundGraph(unittest.TestCase):
    def setUp(self):
        self.triples = {(URI('http://www.example.org/index.html'),
                         URI('http://purl.org/dc/elements/1.1/creator'),
                         BlankNode('john')),
                        (BlankNode('john'),
                         URI('http://xmlns.com/foaf/0.1/name'),
                         Literal("John Lennon")),
                        (BlankNode('john'),
                         URI('http://xmlns.com/foaf/0.1/knows'),
                         BlankNode('paul'))}
        self.graph = Graph(self.triples)

    def test_is_ground_is_false(self):
        self.assertEqual(self.graph.is_ground(), False)

    def test_not_equal_to_graph_with_different_number_of_unground_triples(self):
        graph = Graph({(URI('http://www.example.org/index.html'),
                        URI('http://purl.org/dc/elements/1.1/creator'),
                        URI('john')),
                       (URI('john'),
                        URI('http://xmlns.com/foaf/0.1/name'),
                        Literal("John Lennon"))})
        self.assertNotEqual(self.graph, graph)        
        self.assertNotEqual(graph, self.graph)        

    def test_not_equal_to_graph_with_different_number_of_unique_blank_nodes(self):
        graph = Graph({(URI('http://www.example.org/index.html'),
                        URI('http://purl.org/dc/elements/1.1/creator'),
                        BlankNode('john')),
                       (BlankNode('john'),
                        URI('http://xmlns.com/foaf/0.1/name'),
                        Literal("John Lennon")),
                       (BlankNode('john'),
                        URI('http://xmlns.com/foaf/0.1/knows'),
                        BlankNode("john"))})
        self.assertNotEqual(self.graph, graph)        
        self.assertNotEqual(graph, self.graph)        

    def test_equal_to_graph_with_valid_bijection(self):
        graph = Graph({(URI('http://www.example.org/index.html'),
                        URI('http://purl.org/dc/elements/1.1/creator'),
                        BlankNode('paul')),
                       (BlankNode('paul'),
                        URI('http://xmlns.com/foaf/0.1/name'),
                        Literal("John Lennon")),
                       (BlankNode('paul'),
                        URI('http://xmlns.com/foaf/0.1/knows'),
                        BlankNode('john'))})
        self.assertEqual(self.graph, graph)
        self.assertEqual(graph, self.graph)

    def test_not_equal_to_graph_without_valid_bijection(self):
        graph = Graph({(URI('http://www.example.org/index.html'),
                        URI('http://purl.org/dc/elements/1.1/creator'),
                        BlankNode('john')),
                       (BlankNode('john'),
                        URI('http://xmlns.com/foaf/0.1/name'),
                        Literal("John Lennon")),
                       (BlankNode('paul'),
                        URI('http://xmlns.com/foaf/0.1/knows'),
                        BlankNode('john'))})
        self.assertNotEqual(self.graph, graph)
        self.assertNotEqual(graph, self.graph)

