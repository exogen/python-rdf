#!/usr/bin/env python3
import unittest

from rdf.namespace import TEST
from rdf.testcases.manifest import Manifest
from rdf.testcases.unittest import RDFTestSuite
from util import open_data_file, TEST_OPENER


def testcases():
    manifest = Manifest(open_data_file('rdfcore/Manifest.rdf'))
    suite = unittest.TestSuite()
    for test_case in RDFTestSuite.from_manifest(manifest, opener=TEST_OPENER):
        if test_case.test.type in {TEST.PositiveParserTest, TEST.NegativeParserTest}:
            suite.addTest(test_case)
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='testcases')

