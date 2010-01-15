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

    def test_equal_to_plain_literal_with_same_lexical_form_and_language(self):
        self.assertEqual(self.literal, PlainLiteral("cat", 'en'))

    def test_not_equal_to_plain_literal_with_different_lexical_form(self):
        self.assertNotEqual(self.literal, PlainLiteral("dog", 'en'))

    def test_not_equal_to_plain_literal_with_different_language(self):
        self.assertNotEqual(self.literal, PlainLiteral("cat", 'es'))

    def test_not_equal_to_typed_literal(self):
        self.assertNotEqual(self.literal, TypedLiteral("cat", XSD_STRING))

    def test_not_equal_to_string(self):
        self.assertNotEqual(self.literal, "cat")

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

if __name__ == '__main__':
    unittest.main()