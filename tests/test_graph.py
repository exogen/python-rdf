import unittest

from rdf.blanknode import BlankNode
from rdf.uri import URI
from rdf.literal import Literal
from rdf.namespace import XSD
from rdf.graph import Graph

from util import EX


class TestEmptyGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

    def test_is_set(self):
        self.assertTrue(isinstance(self.graph, set))

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.graph), "Graph()")

    def test_equal_to_empty_set(self):
        self.assertEqual(self.graph, set())
        self.assertEqual(set(), self.graph)

    def test_empty_graph_is_a_subgraph(self):
        graph = Graph()
        self.assertTrue(graph <= self.graph)
        self.assertTrue(self.graph <= graph)

    def test_empty_graphs_are_equal(self):
        self.assertEqual(self.graph, Graph())

    def test_empty_graph_is_not_a_strict_subgraph(self):
        self.assertFalse(Graph() < self.graph)
        self.assertFalse(self.graph < Graph())

    def test_empty_graph_is_a_subgraph(self):
        self.assertTrue(Graph() <= self.graph)
        self.assertTrue(self.graph <= Graph())

    def test_empty_graph_is_not_a_strict_supergraph(self):
        self.assertFalse(Graph() > self.graph)
        self.assertFalse(self.graph > Graph())

    def test_empty_graph_is_a_supergraph(self):
        self.assertTrue(Graph() >= self.graph)
        self.assertTrue(self.graph >= Graph())

    def test_empty_set_is_equal(self):
        self.assertEqual(self.graph, set())

    def test_empty_frozenset_is_equal(self):
        self.assertEqual(self.graph, frozenset())

    def test_empty_set_is_not_a_strict_subset(self):
        self.assertFalse(set() < self.graph)

    def test_empty_frozenset_is_not_a_strict_subset(self):
        self.assertFalse(frozenset() < self.graph)

    def test_is_not_a_strict_subset_of_empty_set(self):
        self.assertFalse(self.graph < set())

    def test_is_not_a_strict_subset_of_empty_frozenset(self):
        self.assertFalse(self.graph < frozenset())

    def test_empty_set_is_a_subset(self):
        self.assertTrue(set() <= self.graph)

    def test_empty_frozenset_is_a_subset(self):
        self.assertTrue(frozenset() <= self.graph)

    def test_is_subset_of_empty_set(self):
        self.assertTrue(self.graph <= set())

    def test_is_subset_of_empty_frozenset(self):
        self.assertTrue(self.graph <= frozenset())

    def test_empty_set_is_not_a_strict_superset(self):
        self.assertFalse(set() > self.graph)

    def test_empty_frozenset_is_not_a_strict_superset(self):
        self.assertFalse(frozenset() > self.graph)

    def test_is_not_a_strict_superset_of_empty_set(self):
        self.assertFalse(self.graph > set())

    def test_is_not_a_strict_superset_of_empty_frozenset(self):
        self.assertFalse(self.graph > frozenset())

    def test_empty_set_is_a_superset(self):
        self.assertTrue(set() >= self.graph)

    def test_empty_frozenset_is_a_superset(self):
        self.assertTrue(frozenset() >= self.graph)

    def test_is_superset_of_empty_set(self):
        self.assertTrue(self.graph >= set())

    def test_is_superset_of_empty_frozenset(self):
        self.assertTrue(self.graph >= frozenset())

class TestGroundGraph(unittest.TestCase):
    def setUp(self):
        self.triples = {(URI('http://www.example.org/index.html'),
                         URI('http://purl.org/dc/elements/1.1/creator'),
                         URI('http://www.example.org/staffid/85740')),
                        (URI('http://www.example.org/staffid/85740'),
                         URI('http://xmlns.com/foaf/0.1/name'),
                         Literal("John Lennon", XSD.string))}
        self.graph = Graph(self.triples)

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.graph),
                         "Graph({!r})".format(self.triples))

    def test_is_ground_is_true(self):
        self.assertEqual(self.graph.is_ground(), True)

    def test_nodes_is_set_of_subjects_and_objects(self):
        self.assertEqual(self.graph.nodes(),
                         {URI('http://www.example.org/index.html'),
                          URI('http://www.example.org/staffid/85740'),
                          Literal("John Lennon", XSD.string)})

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
                        Literal("John Doe", XSD.string))})
        self.assertNotEqual(self.graph, graph)
        self.assertNotEqual(graph, self.graph)

    def test_equal_to_set_with_same_triples(self):
        self.assertEqual(self.triples, self.graph)
        self.assertEqual(self.graph, self.triples)

    def test_equal_to_frozenset_with_same_triples(self):
        self.assertEqual(frozenset(self.triples), self.graph)
        self.assertEqual(self.graph, frozenset(self.triples))

    def test_not_equal_to_set_with_different_triples(self):
        triples = {(URI('http://www.example.org/index.html'),
                    URI('http://purl.org/dc/elements/1.1/creator'),
                    URI('http://www.example.org/staffid/85740')),
                   (URI('http://www.example.org/staffid/85740'),
                    URI('http://xmlns.com/foaf/0.1/name'),
                    Literal("John Doe", XSD.string))}
        self.assertNotEqual(self.graph, triples)

    def test_not_equal_to_frozenset_with_different_triples(self):
        triples = {(URI('http://www.example.org/index.html'),
                    URI('http://purl.org/dc/elements/1.1/creator'),
                    URI('http://www.example.org/staffid/85740')),
                   (URI('http://www.example.org/staffid/85740'),
                    URI('http://xmlns.com/foaf/0.1/name'),
                    Literal("John Doe", XSD.string))}
        self.assertNotEqual(self.graph, frozenset(triples))

    def test_graph_with_same_triples_is_not_a_strict_subgraph(self):
        self.assertFalse(Graph(self.triples) < self.graph)
        self.assertFalse(self.graph < Graph(self.triples))

    def test_graph_with_same_triples_is_subgraph(self):
        self.assert_(Graph(self.triples) <= self.graph)
        self.assert_(self.graph <= Graph(self.triples))

    def test_empty_graph_is_a_subgraph(self):
        self.assert_(Graph() < self.graph)

    def test_empty_set_is_a_subset(self):
        self.assert_(set() < self.graph)

    def test_empty_frozenset_is_a_subset(self):
        self.assert_(frozenset() < self.graph)

    def test_set_with_same_triples_is_not_a_strict_subset(self):
        self.assertFalse(self.triples < self.graph)
        self.assertFalse(self.graph < self.triples)

    def test_set_with_same_triples_is_subset(self):
        self.assert_(self.triples <= self.graph)
        self.assert_(self.graph <= self.triples)

    def test_frozenset_with_same_triples_is_not_a_strict_subset(self):
        self.assertFalse(frozenset(self.triples) < self.graph)
        self.assertFalse(self.graph < frozenset(self.triples))

    def test_frozenset_with_same_triples_is_subset(self):
        self.assert_(frozenset(self.triples) <= self.graph)
        self.assert_(self.graph <= frozenset(self.triples))

    def test_graph_with_same_triples_is_not_a_strict_supergraph(self):
        self.assertFalse(Graph(self.triples) > self.graph)
        self.assertFalse(self.graph > Graph(self.triples))

    def test_graph_with_same_triples_is_supergraph(self):
        self.assert_(Graph(self.triples) >= self.graph)
        self.assert_(self.graph >= Graph(self.triples))

    def test_empty_graph_is_not_a_supergraph(self):
        self.assertFalse(Graph() >= self.graph)

    def test_is_supergraph_of_empty_graph(self):
        self.assert_(self.graph >= Graph())

    def test_is_superset_of_empty_set(self):
        self.assert_(self.graph > set())

    def test_is_superset_of_empty_frozenset(self):
        self.assert_(self.graph > frozenset())

    def test_set_with_same_triples_is_not_a_strict_superset(self):
        self.assertFalse(self.triples > self.graph)
        self.assertFalse(self.graph > self.triples)

    def test_set_with_same_triples_is_superset(self):
        self.assert_(self.triples >= self.graph)
        self.assert_(self.graph >= self.triples)

    def test_frozenset_with_same_triples_is_not_a_strict_superset(self):
        self.assertFalse(frozenset(self.triples) > self.graph)
        self.assertFalse(self.graph > frozenset(self.triples))

    def test_frozenset_with_same_triples_is_superset(self):
        self.assert_(frozenset(self.triples) >= self.graph)
        self.assert_(self.graph >= frozenset(self.triples))

class TestUngroundGraph(unittest.TestCase):
    def setUp(self):
        self.triples = {(URI('http://www.example.org/index.html'),
                         URI('http://purl.org/dc/elements/1.1/creator'),
                         BlankNode('john')),
                        (BlankNode('john'),
                         URI('http://xmlns.com/foaf/0.1/name'),
                         Literal("John Lennon", XSD.string)),
                        (BlankNode('john'),
                         URI('http://xmlns.com/foaf/0.1/knows'),
                         BlankNode('paul'))}
        self.bijection = {(URI('http://www.example.org/index.html'),
                           URI('http://purl.org/dc/elements/1.1/creator'),
                           BlankNode('lennon')),
                          (BlankNode('lennon'),
                           URI('http://xmlns.com/foaf/0.1/name'),
                           Literal("John Lennon", XSD.string)),
                          (BlankNode('lennon'),
                           URI('http://xmlns.com/foaf/0.1/knows'),
                           BlankNode('starr'))}
        self.graph = Graph(self.triples)

    def test_is_ground_is_false(self):
        self.assertEqual(self.graph.is_ground(), False)

    def test_nodes_is_set_of_subjects_and_objects(self):
        self.assertEqual(self.graph.nodes(),
                         {URI('http://www.example.org/index.html'),
                          BlankNode('john'), BlankNode('paul'),
                          Literal("John Lennon", XSD.string)})

    def test_names_is_set_of_uris_and_literals(self):
        self.assertEqual(self.graph.names(),
                         {URI('http://www.example.org/index.html'),
                          URI('http://purl.org/dc/elements/1.1/creator'),
                          URI('http://xmlns.com/foaf/0.1/name'),
                          URI('http://xmlns.com/foaf/0.1/knows'),
                          Literal("John Lennon", XSD.string),
                          XSD.string})

    def test_vocabulary_is_set_of_names_without_datatypes(self):
        self.assertEqual(self.graph.vocabulary(),
                         {URI('http://www.example.org/index.html'),
                          URI('http://purl.org/dc/elements/1.1/creator'),
                          URI('http://xmlns.com/foaf/0.1/name'),
                          URI('http://xmlns.com/foaf/0.1/knows'),
                          Literal("John Lennon", XSD.string)})

    def test_vocabulary_including_datatypes_is_set_of_names(self):
        self.assertEqual(self.graph.vocabulary(include_datatypes=True),
                         self.graph.names())

    def test_not_equal_to_graph_with_different_number_of_unground_triples(self):
        graph = Graph({(URI('http://www.example.org/index.html'),
                        URI('http://purl.org/dc/elements/1.1/creator'),
                        URI('john')),
                       (URI('john'),
                        URI('http://xmlns.com/foaf/0.1/name'),
                        Literal("John Lennon", XSD.string))})
        self.assertNotEqual(self.graph, graph)        
        self.assertNotEqual(graph, self.graph)        

    def test_not_equal_to_graph_with_different_number_of_unique_blank_nodes(self):
        graph = Graph({(URI('http://www.example.org/index.html'),
                        URI('http://purl.org/dc/elements/1.1/creator'),
                        BlankNode('john')),
                       (BlankNode('john'),
                        URI('http://xmlns.com/foaf/0.1/name'),
                        Literal("John Lennon", XSD.string)),
                       (BlankNode('john'),
                        URI('http://xmlns.com/foaf/0.1/knows'),
                        BlankNode("john"))})
        self.assertNotEqual(self.graph, graph)        
        self.assertNotEqual(graph, self.graph)        

    def test_equal_to_graph_with_valid_bijection(self):
        graph = Graph(self.bijection)
        self.assertEqual(self.graph, graph)
        self.assertEqual(graph, self.graph)

    def test_not_equal_to_graph_without_valid_bijection(self):
        graph = Graph({(URI('http://www.example.org/index.html'),
                        URI('http://purl.org/dc/elements/1.1/creator'),
                        BlankNode('john')),
                       (BlankNode('john'),
                        URI('http://xmlns.com/foaf/0.1/name'),
                        Literal("John Lennon", XSD.string)),
                       (BlankNode('paul'),
                        URI('http://xmlns.com/foaf/0.1/knows'),
                        BlankNode('john'))})
        self.assertNotEqual(self.graph, graph)
        self.assertNotEqual(graph, self.graph)
    
    def test_not_equal_to_set_with_valid_bijection(self):
        self.assertNotEqual(self.graph, self.bijection)

    def test_not_equal_to_frozenset_with_valid_bijection(self):
        self.assertNotEqual(self.graph, frozenset(self.bijection))

    def test_equal_to_set_with_identical_triples(self):
        self.assertEqual(self.graph, self.triples)

    def test_equal_to_frozenset_with_identical_triples(self):
        self.assertEqual(self.graph, frozenset(self.triples))

    def test_graph_with_valid_bijection_is_subgraph(self):
        self.assert_(Graph(self.bijection) <= self.graph)

    def graph_with_valid_bijection_is_not_a_strict_subgraph(self):
        self.assertFalse(Graph(self.bijection) < self.graph)

    def test_is_subgraph_of_graph_with_valid_bijection(self):
        self.assert_(self.graph <= Graph(self.bijection))

    def test_is_not_a_strict_subgraph_of_graph_with_valid_bijection(self):
        self.assertFalse(self.graph < Graph(self.bijection))

    def test_graph_with_valid_bijection_is_supergraph(self):
        self.assert_(Graph(self.bijection) >= self.graph)

    def graph_with_valid_bijection_is_not_a_strict_supergraph(self):
        self.assertFalse(Graph(self.bijection) > self.graph)

    def test_is_supergraph_of_graph_with_valid_bijection(self):
        self.assert_(self.graph >= Graph(self.bijection))

    def test_is_not_a_strict_supergraph_of_graph_with_valid_bijection(self):
        self.assertFalse(self.graph > Graph(self.bijection))

class TestMixedGraph(unittest.TestCase):
    def setUp(self):
        self.triples = {(URI('http://www.example.org/index.html'),
                         URI('http://purl.org/dc/elements/1.1/creator'),
                         BlankNode('john')),
                        (BlankNode('john'),
                         URI('http://xmlns.com/foaf/0.1/name'),
                         Literal("John Lennon", XSD.string)),
                        (BlankNode('john'),
                         URI('http://xmlns.com/foaf/0.1/knows'),
                         BlankNode('paul')),
                        (EX.a, EX.property, EX.b),
                        (EX.b, EX.property, EX.c)}
        self.bijection = {(URI('http://www.example.org/index.html'),
                           URI('http://purl.org/dc/elements/1.1/creator'),
                           BlankNode('lennon')),
                          (BlankNode('lennon'),
                           URI('http://xmlns.com/foaf/0.1/name'),
                           Literal("John Lennon", XSD.string)),
                          (BlankNode('lennon'),
                           URI('http://xmlns.com/foaf/0.1/knows'),
                           BlankNode('starr'))}
        self.graph = Graph(self.triples)
        self.subgraph = Graph(self.bijection)

    def test_is_ground_is_false(self):
        self.assertEqual(self.graph.is_ground(), False)

    def test_valid_bijection_of_subset_is_a_strict_subgraph(self):
        self.assert_(self.subgraph < self.graph)

    def test_valid_bijection_of_subset_is_a_subgraph(self):
        self.assert_(self.subgraph <= self.graph)

    def test_is_a_strict_supergraph_of_valid_bijection_of_subset(self):
        self.assert_(self.graph > self.subgraph)

    def test_is_a_supergraph_of_valid_bijection_of_subset(self):
        self.assert_(self.graph >= self.subgraph)

    def test_is_not_a_subgraph_of_valid_bijection_of_subset(self):
        self.assertFalse(self.graph <= self.subgraph)

    def test_is_not_a_strict_subgraph_of_valid_bijection_of_subset(self):
        self.assertFalse(self.graph < self.subgraph)

    def test_is_not_equal_to_subgraph(self):
        self.assert_(self.graph != self.subgraph)
        self.assert_(self.subgraph != self.graph)

