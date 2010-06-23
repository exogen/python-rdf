#!/usr/bin/env python3
import sys
import unittest

from rdf.namespace import TEST
from rdf.testcases.manifest import Manifest
from rdf.testcases.unittest import RDFTestSuite
from util import open_data_file, TEST_OPENER


TEST_URIS = set()

def testcases():
    manifest = Manifest(open_data_file('rdfcore/Manifest.rdf'))
    rdf_suite = RDFTestSuite.from_manifest(manifest, opener=TEST_OPENER)
    if not TEST_URIS:
        return rdf_suite
    else:
        suite = RDFTestSuite()
        for test in rdf_suite:
            if test.id() in TEST_URIS:
                suite.addTest(test)
        return suite

if __name__ == '__main__':
    argv = sys.argv[:1]
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            argv.append(arg)
        else:
            TEST_URIS.add(arg)
    unittest.main(defaultTest='testcases', argv=argv)

