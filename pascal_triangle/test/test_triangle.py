import unittest
import pascal_triangle.pascal as pascal


class TestPascalsTriangle(unittest.TestCase):

    def test_binomial_expansion(self):
        self.assertEqual(pascal.bin_expans(4, 2), 6)
