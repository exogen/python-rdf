#!/usr/bin/env python3
import unittest
from rdf.testcases.manifest import Manifest
from rdf.testcases.unittest import RDFTestSuite
from util import open_data_file, TEST_OPENER


def testcases():
    manifest = Manifest(open_data_file('rdf-testcases/Manifest.rdf'))
    return RDFTestSuite.from_manifest(manifest, opener=TEST_OPENER)

if __name__ == '__main__':
    unittest.main(defaultTest='testcases')

