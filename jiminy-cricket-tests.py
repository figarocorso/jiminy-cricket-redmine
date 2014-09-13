import unittest

from pytz import timezone
from datetime import datetime, timedelta

import string_operations
import number_operations
import date_operations

class JiminyCricketTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Testing string operations
    def testStringOperations(self):
        # string_equal
        self.assertTrue(string_operations.string_equal('c', 'c'))
        self.assertTrue(string_operations.string_equal('cow', 'cow'))
        self.assertTrue(string_operations.string_equal('COW', 'cow'))
        self.assertTrue(string_operations.string_equal('cow', 'COw'))
        self.assertFalse(string_operations.string_equal('vaca', 'cow'))

        # string_contain
        self.assertTrue(string_operations.string_contain('cow', 'c'))
        self.assertTrue(string_operations.string_contain('cow', 'cow'))
        self.assertTrue(string_operations.string_contain('cow', 'COW'))
        self.assertTrue(string_operations.string_contain('a complex cow phrase', 'COW'))
        self.assertFalse(string_operations.string_contain('cow', 'woc'))
        self.assertFalse(string_operations.string_contain('cow', 'COWY'))

    # Testing number operations
    def testNumberOperations(self):
        # number less
        self.assertTrue(number_operations.number_less(69, 666))
        self.assertFalse(number_operations.number_less(69, 69))
        self.assertFalse(number_operations.number_less(666, 69))
        self.assertTrue(number_operations.number_less('69', '666'))
        self.assertFalse(number_operations.number_less('69', 69))

    # Testing date operations
    def testDateOperations(self):
        # date_less
        now = datetime.now(timezone('UTC'))
        compared_date = now - timedelta(days=1, hours=1)
        compared_date = compared_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.assertTrue(date_operations.date_interval(compared_date, 1440))
        self.assertFalse(date_operations.date_interval(compared_date, 2880))


if __name__ == "__main__":
    unittest.main()
