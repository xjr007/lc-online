import unittest

import search_algorithms
import register_functions
import track_time_functions


class TestAllFunctions(unittest.TestCase):

    def test_search(self):
        self.assertEqual(search_algorithms.binary_search([1, 2, 3, 4, 5], 1), 1)

    def test_register_funcs(self):
        self.assertFalse(register_functions.username_valid(1))
        self.assertTrue(register_functions.password_valid("1234"))

    def test_track_time_funcs(self):
        self.assertEqual(track_time_functions.get_day(), track_time_functions.get_day())
        self.assertNotEqual(track_time_functions.get_time(), "not equal")


if __name__ == '__main__':
    unittest.main()
