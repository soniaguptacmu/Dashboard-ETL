import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('hello','hello1')

if __name__ == '__main__':
    unittest.main()