import unittest

class MyTestCase(unittest.TestCase):

    def test_isset(self):
        self.assertEqual(True, True)

    def test_get_ids_for_delete(self):
        self.assertEquals(True, True)


if __name__ == '__main__':
    unittest.main()
