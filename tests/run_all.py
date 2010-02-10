#!/usr/bin/env python3
import os
import glob
import unittest


LOADER = unittest.TestLoader()
GLOB = os.path.join(os.path.dirname(__file__), 'test_*.py')

def all_tests():
    filenames = glob.glob(GLOB)
    names = [os.path.basename(filename)[:-3] for filename in filenames]
    suite = LOADER.loadTestsFromNames(names)
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='all_tests')

