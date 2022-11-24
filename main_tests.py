import unittest

import main


class TestMain(unittest.TestCase):

    def setUp(self) -> None:
        self.items = [
            {"id": 1, "parent": "root"},
            {"id": 2, "parent": 1, "type": "test"},
            {"id": 3, "parent": 1, "type": "test"},
            {"id": 4, "parent": 2, "type": "test"},
            {"id": 5, "parent": 2, "type": "test"},
            {"id": 6, "parent": 2, "type": "test"},
            {"id": 7, "parent": 4, "type": None},
            {"id": 8, "parent": 4, "type": None}
        ]
        self.ts = main.TreeStore(self.items)

    def test_create_items_1(self):
        self.assertRaisesRegex(KeyError, 'Объект не содержит id', main.TreeStore, [{'it': 1, 'parent': 'root'}])

    def test_create_items_2(self):
        test_list = [{"id": 1, "parent": "root"}, {"id": 2, "parent": 3, "type": "test"}]
        self.assertRaisesRegex(KeyError, 'Нет родителя с таким id', main.TreeStore, test_list)

    def test_get_all(self):
        self.assertEqual(self.ts.getAll(), self.items)

    def test_get_item_1(self):
        self.assertEqual(self.ts.getItem(1), self.items[0])

    def test_get_item_2(self):
        self.assertEqual(self.ts.getItem(8), self.items[7])

    def test_get_item_3(self):
        self.assertRaisesRegex(IndexError, "Нет объекта с таким id", self.ts.getItem, 9)

    def test_get_children_1(self):
        answer = [{'id': 2, 'parent': 1, 'type': 'test'}, {'id': 3, 'parent': 1, 'type': 'test'}]
        self.assertEqual(self.ts.getChildren(1), answer)

    def test_get_children_2(self):
        self.assertEqual(self.ts.getChildren(3), [])

    def test_get_all_parents_1(self):
        self.assertEqual(self.ts.getAllParents(1), [])

    def test_get_all_parents_2(self):
        self.assertEqual(self.ts.getAllParents(2), [{'id': 1, 'parent': 'root'}])

    def test_get_all_parents_3(self):
        right_answer = [{'id': 2, 'parent': 1, 'type': 'test'}, {'id': 1, 'parent': 'root'}]
        self.assertEqual(self.ts.getAllParents(4), right_answer)

    def test_get_all_parents_4(self):
        right_answer = [{'id': 4, 'parent': 2, 'type': 'test'}, {'id': 2, 'parent': 1, 'type': 'test'},
                        {'id': 1, 'parent': 'root'}]
        self.assertEqual(self.ts.getAllParents(7), right_answer)


if __name__ == '__main__':
    unittest.main()
