import unittest

import string_operations
import number_operations

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

if __name__ == "__main__":
    unittest.main()
