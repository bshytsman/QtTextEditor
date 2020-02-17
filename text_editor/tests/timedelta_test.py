import unittest
from datetime import timedelta


class TimedeltaTester(unittest.TestCase):

    def test_one(self):
        print("test_one")

        td = timedelta(seconds=1, milliseconds=100.5)
        print(td.total_seconds())



