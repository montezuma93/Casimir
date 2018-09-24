from abc import ABC

class Relation(ABC):

    def __init__(self, category_name):
        self.category_name = category_name

class CategoryRelation(Relation):

    def __init__(self, category_name):
        super().__init__(category_name)

class ConcreteRelation(CategoryRelation):

    def __init__(self, category_name, name):
        self.name = name
        super().__init__(category_name)
