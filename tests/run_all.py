#!/usr/bin/env python3
import os
import glob
import unittest


def all_tests():
    loader = unittest.TestLoader()
    filenames = glob.glob(os.path.join(os.path.dirname(__file__), 'test_*.py'))
    names = [os.path.basename(filename)[:-3] for filename in filenames]
    return loader.loadTestsFromNames(names)

if __name__ == '__main__':
    unittest.main(defaultTest='all_tests')
