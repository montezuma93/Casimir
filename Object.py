from abc import ABC

class Object(ABC):

    def __init__(self, category_name):
        self.category_name = category_name

class CategoryObject(Object):

    def __init__(self, category_name):
        super().__init__(category_name)

class ConcreteObject(CategoryObject):

    def __init__(self, category_name, name):
        self.name = name
        super().__init__(category_name)
