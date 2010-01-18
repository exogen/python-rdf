import unittest
from itertools import islice

from rdf.blanknode import BlankNode
from rdf.uri import URI
from rdf.namespace import Namespace
from rdf.literal import PlainLiteral, TypedLiteral
from rdf.ntriples import NTriplesReader, ParseError
from util import open_data_file


EX = Namespace('http://example.org/')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')

class TestNTriples(unittest.TestCase):
    def setUp(self):
        self.reader = NTriplesReader()
        self.triples = self.reader.read(open_data_file('test.nt'))

    def _get_triple(self, index):
        for triple in islice(self.triples, index, index + 1):
            return triple
        raise IndexError

    def test_is_ntriples_reader(self):
        self.assert_(isinstance(self.reader, NTriplesReader))

    def test_no_subject_raises_error(self):
        document = "."
        self.assertRaises(ParseError, next, self.reader.read(document))

    def test_no_predicate_raises_error(self):
        document = "<http://example.org/test>"
        self.assertRaises(ParseError, next, self.reader.read(document))
        self.assertRaises(ParseError, next, self.reader.read(document + "."))

    def test_no_object_raises_error(self):
        document = "<http://example.org/test> <http://example.org/property>"
        self.assertRaises(ParseError, next, self.reader.read(document))
        self.assertRaises(ParseError, next, self.reader.read(document + "."))

    def test_invalid_escape_sequence_raises_error(self):
        document = '<a> <b> "invalid:\\c" .'
        self.assertRaises(ParseError, next, self.reader.read(document))

    def test_empty_document_yields_no_triples(self):
        triples = list(self.reader.read(""))
        self.assertEqual(triples, [])

    def test_no_unexpected_triples(self):
        self.assertEqual(len(list(self.triples)), 30)

    def test_triple_1_uri(self):
        triple = self._get_triple(0)
        self.assertEqual(triple,
            (EX.resource1, EX.property, EX.resource2))

    def test_triple_2_blank_node_subject(self):
        triple = self._get_triple(1)
        self.assertEqual(triple,
            (BlankNode('anon'), EX.property, EX.resource2))

    def test_triple_3_blank_node_object(self):
        triple = self._get_triple(2)
        self.assertEqual(triple,
            (EX.resource2, EX.property, BlankNode('anon')))

    def test_triples_4_spaces_and_tabs(self):
        triple = self._get_triple(3)
        self.assertEqual(triple,
            (EX.resource3, EX.property, EX.resource2))

    def test_triple_5_line_ending_CRLF(self):
        triple = self._get_triple(4)
        self.assertEqual(triple,
            (EX.resource4, EX.property, EX.resource2))

    def test_triple_6_line_ending_CR(self):
        triple = self._get_triple(5)
        self.assertEqual(triple,
            (EX.resource5, EX.property, EX.resource2))

    def test_triple_7_line_ending_CR(self):
        triple = self._get_triple(6)
        self.assertEqual(triple,
            (EX.resource6, EX.property, EX.resource2))

    def test_triple_8_plain_literal(self):
        triple = self._get_triple(7)
        self.assertEqual(triple,
            (EX.resource7, EX.property, PlainLiteral("simple literal")))

    def test_triple_9_literal_escape_backslash(self):
        triple = self._get_triple(8)
        self.assertEqual(triple,
            (EX.resource8, EX.property, PlainLiteral("backslash:\\")))

    def test_triple_10_literal_escape_double_quote(self):
        triple = self._get_triple(9)
        self.assertEqual(triple,
            (EX.resource9, EX.property, PlainLiteral("dquote:\"")))

    def test_triple_11_literal_escape_newline(self):
        triple = self._get_triple(10)
        self.assertEqual(triple,
            (EX.resource10, EX.property, PlainLiteral("newline:\n")))

    def test_triple_12_literal_escape_return(self):
        triple = self._get_triple(11)
        self.assertEqual(triple,
            (EX.resource11, EX.property, PlainLiteral("return\r")))

    def test_triple_13_literal_escape_tab(self):
        triple = self._get_triple(12)
        self.assertEqual(triple,
            (EX.resource12, EX.property, PlainLiteral("tab:\t")))

    def test_triple_14_optional_space_before_dot(self):
        triple = self._get_triple(13)
        self.assertEqual(triple,
            (EX.resource13, EX.property, EX.resource2))

    def test_triple_15_optional_space_before_dot(self):
        triple = self._get_triple(14)
        self.assertEqual(triple,
            (EX.resource14, EX.property, PlainLiteral("x")))

    def test_triple_16_optional_space_before_dot(self):
        triple = self._get_triple(15)
        self.assertEqual(triple,
            (EX.resource15, EX.property, BlankNode('anon')))

    def test_triple_17_unicode_e_acute(self):
        triple = self._get_triple(16)
        self.assertEqual(triple,
            (EX.resource16, EX.property, PlainLiteral("\u00E9")))

    def test_triple_18_unicode_euro_symbol(self):
        triple = self._get_triple(17)
        self.assertEqual(triple,
            (EX.resource17, EX.property, PlainLiteral("\u20AC")))

    def test_triple_19_typed_literal_xml_literal(self):
        triple = self._get_triple(18)
        self.assertEqual(triple,
            (EX.resource21, EX.property, TypedLiteral("", RDFS.XMLLiteral)))

    def test_triple_20_typed_literal_xml_literal(self):
        triple = self._get_triple(19)
        self.assertEqual(triple,
            (EX.resource22, EX.property, TypedLiteral(" ", RDFS.XMLLiteral)))

    def test_triple_21_typed_literal_xml_literal(self):
        triple = self._get_triple(20)
        self.assertEqual(triple,
            (EX.resource23, EX.property, TypedLiteral("x", RDFS.XMLLiteral)))

    def test_triple_22_typed_literal_xml_literal(self):
        triple = self._get_triple(21)
        self.assertEqual(triple,
            (EX.resource23, EX.property, TypedLiteral("\"", RDFS.XMLLiteral)))

    def test_triple_23_typed_literal_xml_literal(self):
        triple = self._get_triple(22)
        self.assertEqual(triple,
            (EX.resource24, EX.property, TypedLiteral("<a></a>", RDFS.XMLLiteral)))

    def test_triple_24_typed_literal_xml_literal(self):
        triple = self._get_triple(23)
        self.assertEqual(triple,
            (EX.resource25, EX.property, TypedLiteral("a <b></b>", RDFS.XMLLiteral)))

    def test_triple_25_typed_literal_xml_literal(self):
        triple = self._get_triple(24)
        self.assertEqual(triple,
            (EX.resource26, EX.property, TypedLiteral("a <b></b> c", RDFS.XMLLiteral)))

    def test_triple_26_typed_literal_xml_literal(self):
        triple = self._get_triple(25)
        self.assertEqual(triple,
            (EX.resource26, EX.property, TypedLiteral("a\n<b></b>\nc", RDFS.XMLLiteral)))

    def test_triple_27_typed_literal_xml_literal(self):
        triple = self._get_triple(26)
        self.assertEqual(triple,
            (EX.resource27, EX.property, TypedLiteral("chat", RDFS.XMLLiteral)))

    def test_triple_28_plain_literal_with_language_fr(self):
        triple = self._get_triple(27)
        self.assertEqual(triple,
            (EX.resource30, EX.property, PlainLiteral("chat", 'fr')))

    def test_triple_29_plain_literal_with_language_en(self):
        triple = self._get_triple(28)
        self.assertEqual(triple,
            (EX.resource31, EX.property, PlainLiteral("chat", 'en')))

    def test_triple_30_typed_literal_example_datatype(self):
        triple = self._get_triple(29)
        self.assertEqual(triple,
            (EX.resource32, EX.property, TypedLiteral("abc", EX.datatype1)))

