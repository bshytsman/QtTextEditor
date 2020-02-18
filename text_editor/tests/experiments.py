import unittest
from datetime import timedelta

from text_editor.util.file_utils import FileUtils


class ExperimentsTester(unittest.TestCase):

    def test_timedelta(self):
        print("test_one")

        td = timedelta(seconds=1, milliseconds=100.5)
        print(td.total_seconds())

    def test_hashing(self):
        str = "Some type of çßå∂ß∂ text here."
        hash_value = hash(str)
        print(str)
        print(hash_value)
        print(type(hash_value))

    def test_three(self):
        print("test_three()")
        print(FileUtils.argument)
        FileUtils.argument = 22
        print(FileUtils.argument)

