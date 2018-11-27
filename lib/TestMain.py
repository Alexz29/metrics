import unittest
from lib import Main


class MyTestCase(unittest.TestCase):

    def test_isset(self):
        main = Main()
        self.assertEqual(main.isset([{
            'name': 'test_name',
            'title': 2,
            'id': 4
        }
        ], 'test_name', 'name'), 4)

        self.assertEqual(main.isset([{
            'name': 'test_name',
            'title': 2,
            'id': 4
        }], 'test_name_wrong', 'name'), False)

    def test_get_ids_for_delete(self):
        main = Main()

        self.assertEquals(main.get_ids_for_delete(
            [{'attr': 'test', 'id': 1}],
            [{'attr': 'test'}],
            'attr'
        ), [])

        self.assertEquals(main.get_ids_for_delete(
            [{'attr': 'test', 'id': 2}, {'attr': 'test2', 'id': 1}],
            [{'attr': 'test'}],
            'attr'
        ), [1])


if __name__ == '__main__':
    unittest.main()


