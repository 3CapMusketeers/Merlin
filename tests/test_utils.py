import os
import unittest

from utils.file_utils import write_file


class FileUtilsTestCase(unittest.TestCase):

    def test_write_file(self):
        write_file('test.txt', b"this is a test")
        with open("test.txt") as file:
            assert file.read() == "this is a test"
        os.remove('test.txt')