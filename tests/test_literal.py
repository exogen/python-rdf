import unittest
import operator

from rdf.blanknode import BlankNode
from rdf.uri import URI
from rdf.literal import Literal, PlainLiteral, TypedLiteral
from rdf.namespace import XSD


class TestSimpleLiteral(unittest.TestCase):
    def setUp(self):
        self.literal = PlainLiteral("cat")

    def test_language_tag_is_none(self):
        self.assertEqual(self.literal.language, None)

    def test_is_literal(self):
        self.assert_(isinstance(self.literal, Literal))

    def test_is_plain_literal(self):
        self.assert_(isinstance(self.literal, PlainLiteral))

    def test_has_lexical_form(self):
        self.assertEqual(self.literal.lexical_form, "cat")

    def test_repr_shows_constructor_without_language(self):
        self.assertEqual(repr(self.literal), "PlainLiteral('cat')")

    def test_hash_not_equal_to_string(self):
        self.assertNotEqual(hash(self.literal), hash("cat"))

    def test_compares_less_than_simple_literal_lexicographically(self):
        self.assert_(self.literal < PlainLiteral("cau"))

    def test_compares_greater_than_simple_literal_lexicographically(self):
        self.assert_(self.literal > PlainLiteral("cas"))

class TestPlainLiteral(unittest.TestCase):
    def setUp(self):
        self.literal = PlainLiteral("cat", 'en')

    def test_has_language_tag(self):
        self.assertEqual(self.literal.language, 'en')

    def test_language_tag_is_normalized_to_lowercase(self):
        literal = PlainLiteral("cat", 'EN')
        self.assertEqual(literal.language, 'en')

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.literal), "PlainLiteral('cat', 'en')")

    def test_equal_to_plain_literal_with_same_lexical_form_and_language(self):
        self.assertEqual(self.literal, PlainLiteral("cat", 'en'))

    def test_not_equal_to_plain_literal_with_different_lexical_form(self):
        self.assertNotEqual(self.literal, PlainLiteral("dog", 'en'))

    def test_not_equal_to_plain_literal_with_different_language(self):
        self.assertNotEqual(self.literal, PlainLiteral("cat", 'es'))

    def test_not_equal_to_simple_literal(self):
        self.assertNotEqual(self.literal, PlainLiteral("cat"))

    def test_not_equal_to_typed_literal(self):
        self.assertNotEqual(self.literal, TypedLiteral("cat", XSD.string))

    def test_not_equal_to_string(self):
        self.assertNotEqual(self.literal, "cat")

    def test_hash_equal_to_plain_literal_with_same_lexical_form_and_language(self):
        self.assertEqual(hash(self.literal), hash(PlainLiteral("cat", 'en')))

    def test_hash_not_equal_to_plain_literal_with_different_lexical_form(self):
        self.assertNotEqual(hash(self.literal), hash(PlainLiteral("dog", 'en')))

    def test_hash_not_equal_to_plain_literal_with_different_language(self):
        self.assertNotEqual(hash(self.literal), hash(PlainLiteral("cat", 'es')))

    def test_hash_not_equal_to_plain_literal_without_language(self):
        self.assertNotEqual(hash(self.literal), hash(PlainLiteral("cat")))

    def test_hash_not_equal_to_typed_literal(self):
        self.assertNotEqual(hash(self.literal), hash(TypedLiteral("cat", XSD.string)))

    def test_compares_greater_than_none(self):
        self.assert_(self.literal > None)
        self.assert_(not self.literal < None)

    def test_compares_greater_than_blank_node(self):
        bnode = BlankNode()
        self.assert_(self.literal > bnode)
        self.assert_(not self.literal < bnode)

    def test_compares_greater_than_uri(self):
        uri = URI('http://example.org/')
        self.assert_(self.literal > uri)
        self.assert_(not self.literal < uri)

    def test_does_not_compare_to_simple_literal(self):
        literal = PlainLiteral("cat")
        with self.assertRaises(TypeError):
            self.literal < literal
        with self.assertRaises(TypeError):
            self.literal > literal

    def test_does_not_compare_to_plain_literal(self):
        literal = PlainLiteral("cat", 'en')
        with self.assertRaises(TypeError):
            self.literal < literal
        with self.assertRaises(TypeError):
            self.literal > literal

    def test_does_not_compare_to_typed_literal(self):
        literal = TypedLiteral("1", XSD.string)
        with self.assertRaises(TypeError):
            self.literal < literal
        with self.assertRaises(TypeError):
            self.literal > literal

    def test_compares_less_than_xsd_string_with_same_lexical_form(self):
        literal = TypedLiteral("cat", XSD.string)
        self.assert_(self.literal < literal)
        self.assert_(not self.literal > literal)

class TestTypedLiteral(unittest.TestCase):
    def setUp(self):
        self.literal = TypedLiteral("1", XSD.string)

    def test_is_literal(self):
        self.assert_(isinstance(self.literal, Literal))

    def test_is_typed_literal(self):
        self.assert_(isinstance(self.literal, TypedLiteral))

    def test_has_lexical_form(self):
        self.assertEqual(self.literal.lexical_form, "1")

    def test_has_datatype(self):
        self.assertEqual(self.literal.datatype, XSD.string)
    
    def test_datatype_is_required(self):
        self.assertRaises(TypeError, TypedLiteral, "1")

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.literal), "TypedLiteral('1', {!r})".format(XSD.string))

    def test_equal_to_typed_literal_with_same_lexical_form_and_datatype(self):
        self.assertEqual(self.literal, TypedLiteral("1", XSD.string))

    def test_not_equal_to_typed_literal_with_different_lexical_form(self):
        self.assertNotEqual(self.literal, TypedLiteral("dog", XSD.string))

    def test_not_equal_to_typed_literal_with_different_datatype(self):
        self.assertNotEqual(self.literal, TypedLiteral("1", XSD.integer))

    def test_not_equal_to_plain_literal(self):
        self.assertNotEqual(self.literal, PlainLiteral("1"))

    def test_not_equal_to_string(self):
        self.assertNotEqual(self.literal, "1")

    def test_hash_equal_to_typed_literal_with_same_lexical_form_and_datatype(self):
        self.assertEqual(hash(self.literal), hash(TypedLiteral("1", XSD.string)))

    def test_hash_not_equal_to_typed_literal_with_different_lexical_form(self):
        self.assertNotEqual(hash(self.literal), hash(TypedLiteral("dog", XSD.string)))

    def test_hash_not_equal_to_typed_literal_with_different_datatype(self):
        self.assertNotEqual(hash(self.literal), hash(TypedLiteral("1", XSD.integer)))

    def test_hash_not_equal_to_plain_literal(self):
        self.assertNotEqual(hash(self.literal), hash(PlainLiteral("1")))

    def test_hash_not_equal_to_plain_literal_with_language(self):
        literal = TypedLiteral("1", URI('en'))
        self.assertNotEqual(hash(literal), hash(PlainLiteral("1", 'en')))

    def test_hash_not_equal_to_string(self):
        self.assertNotEqual(hash(self.literal), hash("1"))

    def test_compares_greater_than_none(self):
        self.assert_(self.literal > None)
        self.assert_(not self.literal < None)

    def test_compares_greater_than_blank_node(self):
        bnode = BlankNode()
        self.assert_(self.literal > bnode)
        self.assert_(not self.literal < bnode)

    def test_compares_greater_than_uri(self):
        uri = URI('http://example.org/')
        self.assert_(self.literal > uri)
        self.assert_(not self.literal < uri)

    def test_does_not_compare_to_simple_literal(self):
        literal = PlainLiteral("cat")
        with self.assertRaises(TypeError):
            self.literal < literal
        with self.assertRaises(TypeError):
            self.literal > literal

    def test_does_not_compare_to_plain_literal(self):
        literal = PlainLiteral("cat", 'fr')
        with self.assertRaises(TypeError):
            self.literal < literal
        with self.assertRaises(TypeError):
            self.literal > literal

    def test_does_not_compare_to_typed_literal_with_different_datatype(self):
        literal = TypedLiteral("1", XSD.integer)
        with self.assertRaises(TypeError):
            self.literal < literal
        with self.assertRaises(TypeError):
            self.literal > literal

    def test_compares_greater_than_simple_literal_with_same_lexical_form(self):
        self.assert_(self.literal > PlainLiteral("1"))

    def test_compares_greater_than_plain_literal_with_same_lexical_form(self):
        self.assert_(self.literal > PlainLiteral("1", 'en'))

    def test_compares_less_than_xsd_string_lexicographically(self):
        self.assert_(self.literal < TypedLiteral("20", XSD.string))

    def test_compares_greater_than_xsd_string_lexicographically(self):
        self.assert_(self.literal > TypedLiteral("0", XSD.string))

class TestLiteral(unittest.TestCase):
    def test_constructor_with_only_lexical_form_creates_plain_literal(self):
        literal = Literal("cat")
        self.assert_(isinstance(literal, PlainLiteral))

    def test_constructor_with_language_creates_plain_literal(self):
        literal = Literal("cat", 'en')
        self.assert_(isinstance(literal, PlainLiteral))

    def test_constructor_with_uri_creates_typed_literal(self):
        literal = Literal("cat", XSD.string)
        self.assert_(isinstance(literal, TypedLiteral))

