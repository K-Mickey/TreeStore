class TreeStore:
    """
    Класс для хранения и выдачи по запросу массива данных, представленных в виде дерева.

    Массив состоит из списка словарей. В словаре обязательно наличие ключей 'id', 'parent'.
    'id' хранит уникальный номер объекта. 'parent' хранит id объекта для которого приходится ребёнком.
    Дополнительные поля не скажутся на работе класса. Класс организован таким образом, чтобы уменьшить
    время выдачи данных по запросу.
    Для этого вся обработка данных происходит при создании класса и добавлении массива данных.

    Основные методы класса:
    getAll() - Возврат всего массива данных
    getItem(id) - Возврат объекта массива по id
    getChildren(id) - Возврат детей объекта по id
    getAllParents(id) - Возврат родительского древа объекта по id
    """
    def __init__(self, items):
        """
        Конструктор класса

        вход: items - список словарей, в которых присутствуют ключи 'id', 'parent', 'type'.
        'id' должен быть уникальным, int
        'root' должен ссылаться на уже написанный ранее id, int. Первый объект принимает значение 'root'

        Пример создания объекта класса:
        ts = TreeStore([{'id': 1, 'parent': 'root'}, {'id': 2, 'parent': 1, 'type': 'test'}])

        вспомогательные словари:
        __id_to_items - ключ: id; значение: объект с таким же id
        __children_history - ключ: id; значение: список из словарей объектов детей ключа
        __parents_history - ключ: id; значение: список из словарей родительского древа ключа
        """
        self.__items = items
        self.__id_to_items = dict()
        self.__children_history = dict()
        self.__parents_history = dict()

        self.__append_to_dicts(items)

    def __append_to_dicts(self, items: dict) -> None:
        """Организация проверки и добавления значений в разные словари класса"""
        for obj in items:
            self.__check_dicts_key(obj, "id", "Передаваемое значение не имеет ключа 'id'")
            self.__check_dicts_key(obj, "parent", "Передаваемое значение не имеет ключа 'parent'")

            id = obj["id"]
            id_parent = obj["parent"]

            self.__check_id_invalid(id)
            self.__check_id_invalid(id_parent)

            self.__add_to_items_dict(id, obj)
            self.__add_to_children_history(id, id_parent, obj)
            self.__add_to_parents_history(id, id_parent)

    def __add_to_items_dict(self, id, obj):
        """Добавление объекта в список объектов"""
        self.__id_to_items[id] = obj

    def __add_to_children_history(self, id, id_parent, obj):
        """Добавление объекта в список детей"""
        self.__children_history[id] = []

        if id_parent != "root":
            message = 'Отсутствует родитель при добавлении в историю детей'
            self.__check_dicts_key(self.__children_history, id_parent, message)
            self.__children_history[id_parent].append(obj)

    def __add_to_parents_history(self, id, id_parent):
        """Добавление объекта в древо родителей"""
        if id_parent == "root":
            self.__parents_history[id] = []
        else:
            message = 'Отсутствует родитель при добавлении в древо родителей'
            self.__check_dicts_key(self.__parents_history, id_parent, message)

            history = self.__parents_history[id_parent][:]
            history.insert(0, self.__id_to_items[id_parent])
            self.__parents_history[id] = history

    def getAll(self) -> list:
        """Возврат всех объектов"""
        return self.__items

    def getItem(self, id: int) -> dict:
        """Возврат объекта по id"""
        self.__check_id_invalid(id)
        self.__check_id_in_dict(self.__id_to_items, id)
        return self.__id_to_items[id]

    def getChildren(self, id: int) -> list:
        """Возврат всех детей объекта по id"""
        self.__check_id_invalid(id)
        self.__check_id_in_dict(self.__children_history, id)
        return self.__children_history[id]

    def getAllParents(self, id: int) -> list:
        """Возврат древа родителей по id"""
        self.__check_id_invalid(id)
        self.__check_id_in_dict(self.__parents_history, id)
        return self.__parents_history[id]

    @staticmethod
    def __check_dicts_key(dictionary:dict, key: int or str, message: str):
        """Проверка ключей в словарях"""
        if key not in dictionary:
            raise KeyError(message)

    @staticmethod
    def __check_id_in_dict(dictionary: dict, id: int) -> None:
        """Проверка наличия id объекта в словаре"""
        if id not in dictionary:
            raise IndexError('Нет объекта с таким id')

    @staticmethod
    def __check_id_invalid(id: int) -> None:
        """Проверка id на соответствие типу данных"""
        if id != "root" and type(id) != int:
            raise TypeError('id должен быть int')


def main():
    items = [
        {"id": 1, "parent": "root"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 3, "parent": 1, "type": "test"},
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 5, "parent": 2, "type": "test"},
        {"id": 6, "parent": 2, "type": "test"},
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None}
    ]
    ts = TreeStore(items)

    ts.getAll()
    ts.getItem(7)
    ts.getChildren(4)
    ts.getChildren(5)
    ts.getAllParents(7)


if __name__ == '__main__':
    main()
