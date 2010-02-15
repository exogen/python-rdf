import unittest
import re
from xml.etree import cElementTree as ElementTree

from rdf.uri import URI
from rdf.namespace import Namespace, TEST, RDF, RDFS, XSD
from rdf.testcases.document import Document
from rdf.testcases.test import *

from util import open_data_file, EX, TESTS


class TestTest(unittest.TestCase):
    def setUp(self):
        self.test = Test(TEST.PositiveParserTest, EX.test)

    def test_is_positive_parser_test(self):
        self.assert_(isinstance(self.test, PositiveParserTest))

    def test_has_type(self):
        self.assertEqual(self.test.type, TEST.PositiveParserTest)

    def test_has_uri(self):
        self.assertEqual(self.test.uri, EX.test)

    def test_status_is_none(self):
        self.assertEqual(self.test.status, None)

    def test_description_is_none(self):
        self.assertEqual(self.test.description, None)

    def test_warning_is_none(self):
        self.assertEqual(self.test.warning, None)

    def test_can_set_status(self):
        self.test.status = 'APPROVED'
        self.assertEqual(self.test.status, 'APPROVED')

    def test_can_set_description(self):
        self.test.description = "Lorem ipsum dolor sit amet"
        self.assertEqual(self.test.description, "Lorem ipsum dolor sit amet")

    def test_can_set_warning(self):
        self.test.warning = "Lorem ipsum dolor sit amet"
        self.assertEqual(self.test.warning, "Lorem ipsum dolor sit amet")

class TestTestFromElement(unittest.TestCase):
    def setUp(self):
        if getattr(self, 'tag', None) is not None:
            xml = open_data_file('manifest.rdf').read()
            self.manifest = ElementTree.XML(xml)
            self.element = self.manifest.find(str(self.tag))
            self.test = Test.from_element(self.element)
        else:
            self.skipTest("'tag' attribute not set. abstract test case?")

    def assertTextEqual(self, a, b):
        ws = re.compile(r'\s+')
        return self.assertEqual(ws.sub(' ', a), ws.sub(' ', b))

    def test_is_test(self):
        self.assert_(isinstance(self.test, Test))

class TestPositiveParserTest(TestTestFromElement):
    tag = ElementTree.QName(TEST, 'PositiveParserTest')

    def test_is_positive_parser_test(self):
        self.assert_(isinstance(self.test, PositiveParserTest))

    def test_has_uri(self):
        self.assertEqual(self.test.uri,
                         TESTS['amp-in-url/Manifest.rdf#test001'])

    def test_has_type(self):
        self.assertEqual(self.test.type, TEST.PositiveParserTest)

    def test_has_status(self):
        self.assertEqual(self.test.status, 'APPROVED')

    def test_description_is_none(self):
        self.assertEqual(self.test.description, None)

    def test_has_input_documents(self):
        self.assertEqual(set(self.test.input_documents),
                         {Document(TEST['RDF-XML-Document'],
                                   TESTS['amp-in-url/test001.rdf'])})

    def test_has_output_document(self):
        self.assertEqual(self.test.output_document,
                         Document(TEST['NT-Document'],
                                  TESTS['amp-in-url/test001.nt']))

    def test_warning_is_none(self):
        self.assertEqual(self.test.warning, None)

class TestNegativeParserTest(TestTestFromElement):
    tag = ElementTree.QName(TEST, 'NegativeParserTest')

    def test_is_negative_parser_test(self):
        self.assert_(isinstance(self.test, NegativeParserTest))

    def test_has_uri(self):
        self.assertEqual(self.test.uri, TESTS['rdf-charmod-literals/Manifest.rdf#error001'])

    def test_has_type(self):
        self.assertEqual(self.test.type, TEST.NegativeParserTest)

    def test_has_status(self):
        self.assertEqual(self.test.status, 'WITHDRAWN')

    def test_has_description(self):
        self.assertTextEqual(self.test.description,
            " Does the treatment of literals conform to charmod ? "
            " Test for failure for literal not in Normal Form C "
            " This test case has been WITHDRAWN in light of changes to NFC handling in concepts ")

    def test_has_input_document(self):
        self.assertEqual(self.test.input_document,
                         Document(TEST['RDF-XML-Document'],
                                  TESTS['rdf-charmod-literals/error001.rdf']))

    def test_warning_is_none(self):
        self.assertEqual(self.test.warning, None)

class TestPositiveEntailmentTest(TestTestFromElement):
    tag = ElementTree.QName(TEST, 'PositiveEntailmentTest')

    def test_is_positive_entailment_test(self):
        self.assert_(isinstance(self.test, PositiveEntailmentTest))

    def test_has_uri(self):
        self.assertEqual(self.test.uri,
            TESTS['datatypes-intensional/Manifest.rdf#xsd-integer-string-incompatible'])

    def test_has_type(self):
        self.assertEqual(self.test.type, TEST.PositiveEntailmentTest)

    def test_has_status(self):
        self.assertEqual(self.test.status, 'APPROVED')

    def test_has_description(self):
        self.assertTextEqual(self.test.description,
            " The claim that xsd:integer is a subClassOF xsd:string is "
            " incompatible with using the intensional semantics for datatypes. ")

    def test_has_entailment_rules(self):
        self.assertEqual(set(self.test.entailment_rules),
                         {RDF, RDFS, TESTS['datatypes#']})

    def test_has_datatype_support(self):
        self.assertEqual(set(self.test.datatype_support),
                         {XSD.integer, XSD.string})

    def test_has_premise_documents(self):
        self.assertEqual(set(self.test.premise_documents),
                         {Document(TEST['NT-Document'],
                                   TESTS['datatypes-intensional/test002.nt'])})

    def test_has_conclusion_document(self):
        self.assertEqual(self.test.conclusion_document,
                         Document(TEST['False-Document']))

    def test_warning_is_none(self):
        self.assertEqual(self.test.warning, None)

class TestNegativeEntailmentTest(TestTestFromElement):
    tag = ElementTree.QName(TEST, 'NegativeEntailmentTest')

    def test_is_negative_entailment_test(self):
        self.assert_(isinstance(self.test, NegativeEntailmentTest))

    def test_has_uri(self):
        self.assertEqual(self.test.uri,
            TESTS['datatypes-intensional/Manifest.rdf#xsd-integer-decimal-compatible'])

    def test_has_type(self):
        self.assertEqual(self.test.type, TEST.NegativeEntailmentTest)

    def test_has_status(self):
        self.assertEqual(self.test.status, 'APPROVED')

    def test_has_description(self):
        self.assertTextEqual(self.test.description,
            " The claim that xsd:integer is a subClassOF xsd:decimal is not "
            " incompatible with using the intensional semantics for datatypes. ")

    def test_has_entailment_rules(self):
        self.assertEqual(set(self.test.entailment_rules),
                         {RDF, RDFS, TESTS['datatypes#']})

    def test_has_datatype_support(self):
        self.assertEqual(set(self.test.datatype_support),
                         {XSD.integer, XSD.decimal})

    def test_has_premise_documents(self):
        self.assertEqual(set(self.test.premise_documents),
                         {Document(TEST['NT-Document'],
                                   TESTS['datatypes-intensional/test001.nt'])})

    def test_has_conclusion_document(self):
        self.assertEqual(self.test.conclusion_document,
                         Document(TEST['False-Document']))

    def test_warning_is_none(self):
        self.assertEqual(self.test.warning, None)

class TestMiscellaneousTest(TestTestFromElement):
    tag = ElementTree.QName(TEST, 'MiscellaneousTest')

    def test_has_uri(self):
        self.assertEqual(self.test.uri,
            TESTS['rdfms-uri-substructure/Manifest.rdf#error001'])

    def test_has_type(self):
        self.assertEqual(self.test.type, TEST.MiscellaneousTest)

    def test_has_status(self):
        self.assertEqual(self.test.status, 'APPROVED') 

    def test_has_description(self):
        self.assertTextEqual(self.test.description,
            " An RDF/XML serlializer is recommended to produce an exception if "
            " asked to serialize the following graph since there is no way "
            " to represent it in the RDF/XML syntax. ")

    def test_has_warning(self):
        self.assertTextEqual(self.test.warning,
            " An RDF/XML serlializer is recommended to produce an exception if "
            " asked to serialize the following graph since there is no way "
            " to represent it in the RDF/XML syntax. ")

    def test_has_documents(self):
        self.assertEqual(set(self.test.documents),
            {Document(TEST['NT-Document'],
                      TESTS['rdfms-uri-substructure/error001.nt'])})

