import unittest

from rdf.uri import URI
from rdf.literal import Literal, PlainLiteral, TypedLiteral

XSD_STRING = URI('http://www.w3.org/2001/XMLSchema#string')
XSD_INTEGER = URI('http://www.w3.org/2001/XMLSchema#integer')

class TestPlainLiteral(unittest.TestCase):
    def setUp(self):
        self.literal = PlainLiteral("cat", 'en')

    def test_is_literal(self):
        self.assert_(isinstance(self.literal, Literal))

    def test_is_plain_literal(self):
        self.assert_(isinstance(self.literal, PlainLiteral))

    def test_has_lexical_form(self):
        self.assertEqual(self.literal.lexical_form, "cat")

    def test_has_language_tag(self):
        self.assertEqual(self.literal.language, 'en')

    def test_language_tag_is_optional(self):
        literal = PlainLiteral("cat")
        self.assertEqual(literal.language, None)

    def test_language_tag_is_normalized_to_lowercase(self):
        literal = PlainLiteral("cat", 'EN')
        self.assertEqual(literal.language, 'en')

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.literal), "PlainLiteral('cat', 'en')")

    def test_repr_without_language_tag_omits_language(self):
        literal = PlainLiteral("cat")
        self.assertEqual(repr(literal), "PlainLiteral('cat')")

    def test_equal_to_plain_literal_with_same_lexical_form_and_language(self):
        self.assertEqual(self.literal, PlainLiteral("cat", 'en'))

    def test_not_equal_to_plain_literal_with_different_lexical_form(self):
        self.assertNotEqual(self.literal, PlainLiteral("dog", 'en'))

    def test_not_equal_to_plain_literal_with_different_language(self):
        self.assertNotEqual(self.literal, PlainLiteral("cat", 'es'))

    def test_not_equal_to_plain_literal_without_language(self):
        self.assertNotEqual(self.literal, PlainLiteral("cat"))

    def test_not_equal_to_typed_literal(self):
        self.assertNotEqual(self.literal, TypedLiteral("cat", XSD_STRING))

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
        self.assertNotEqual(hash(self.literal), hash(TypedLiteral("cat", XSD_STRING)))

    def test_hash_not_equal_to_string(self):
        self.assertNotEqual(hash(self.literal), hash("cat"))
    
class TestTypedLiteral(unittest.TestCase):
    def setUp(self):
        self.literal = TypedLiteral("1", XSD_STRING)

    def test_is_literal(self):
        self.assert_(isinstance(self.literal, Literal))

    def test_is_typed_literal(self):
        self.assert_(isinstance(self.literal, TypedLiteral))

    def test_has_lexical_form(self):
        self.assertEqual(self.literal.lexical_form, "1")

    def test_has_datatype(self):
        self.assertEqual(self.literal.datatype, XSD_STRING)
    
    def test_datatype_is_required(self):
        self.assertRaises(TypeError, TypedLiteral, "1")

    def test_repr_shows_constructor(self):
        self.assertEqual(repr(self.literal), "TypedLiteral('1', {!r})".format(XSD_STRING))

    def test_equal_to_typed_literal_with_same_lexical_form_and_datatype(self):
        self.assertEqual(self.literal, TypedLiteral("1", XSD_STRING))

    def test_not_equal_to_typed_literal_with_different_lexical_form(self):
        self.assertNotEqual(self.literal, TypedLiteral("dog", XSD_STRING))

    def test_not_equal_to_typed_literal_with_different_datatype(self):
        self.assertNotEqual(self.literal, TypedLiteral("1", XSD_INTEGER))

    def test_not_equal_to_plain_literal(self):
        self.assertNotEqual(self.literal, PlainLiteral("1"))

    def test_not_equal_to_string(self):
        self.assertNotEqual(self.literal, "1")

    def test_hash_equal_to_typed_literal_with_same_lexical_form_and_datatype(self):
        self.assertEqual(hash(self.literal), hash(TypedLiteral("1", XSD_STRING)))

    def test_hash_not_equal_to_typed_literal_with_different_lexical_form(self):
        self.assertNotEqual(hash(self.literal), hash(TypedLiteral("dog", XSD_STRING)))

    def test_hash_not_equal_to_typed_literal_with_different_datatype(self):
        self.assertNotEqual(hash(self.literal), hash(TypedLiteral("1", XSD_INTEGER)))

    def test_hash_not_equal_to_plain_literal(self):
        self.assertNotEqual(hash(self.literal), hash(PlainLiteral("1")))

    def test_hash_not_equal_to_plain_literal_with_language(self):
        literal = TypedLiteral("1", URI('en'))
        self.assertNotEqual(hash(literal), hash(PlainLiteral("1", 'en')))

    def test_hash_not_equal_to_string(self):
        self.assertNotEqual(hash(self.literal), hash("1"))

class TestLiteral(unittest.TestCase):
    def test_constructor_with_lexical_form_creates_plain_literal(self):
        literal = Literal("cat")
        self.assert_(isinstance(literal, PlainLiteral))

    def test_constructor_with_language_creates_plain_literal(self):
        literal = Literal("cat", 'en')
        self.assert_(isinstance(literal, PlainLiteral))

    def test_constructor_with_uri_creates_typed_literal(self):
        literal = Literal("cat", XSD_STRING)
        self.assert_(isinstance(literal, TypedLiteral))

if __name__ == '__main__':
    unittest.main()

