# test functionality of generate.py
# run like this:
#   python -m unittest test_generate.py
# the output will be the result of the tests

import unittest
import os
import sys
from generate import generate_site
try:
    import filecmp
except ImportError:
    raise ImportError('Could not import filecmp')

def compare_files(path1, path2):
    """Compare contents of two files, ignoring the newlines"""
    content1 = ""
    with open(path1, 'r') as file:
        for line in file:
            line = line.strip('\r\n')
            content1 += line
        file.close()

    content2 = ""
    with open(path2, 'r') as file:
        for line in file:
            line = line.strip('\r\n')
            content2 += line
        file.close()

    return content1 == content2

class TestGenerateSite(unittest.TestCase):
    def test_output(self):
        """Compare output against expected_output."""
        source_path = os.path.join("test", "source")
        output_path = os.path.join("test", "output")
        ref_path = os.path.join("test", "expected_output")
        generate_site(source_path, output_path);
        for filename in os.listdir(output_path):
            self.assertTrue(compare_files(os.path.join(output_path, filename),
                os.path.join(ref_path, filename)))

    def test_input(self):
        """Check exceptions raised when given wrong source_path."""
        self.assertRaises(FileNotFoundError, generate_site, "foo", "output")
