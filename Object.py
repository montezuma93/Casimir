from abc import ABC

class Object(ABC):

    def __init__(self):
        pass

class ObjectCategorie(Object):

    def __init__(self, category_name):
        self.category_name = category_name
        super().__init__()

class CityObject(ObjectCategorie):

    def __init__(self, name):
        self.name = name
        super().__init__("City")

class CountryObject(ObjectCategorie):

    def __init__(self, name):
        self.name = name
        super().__init__("Country")

class ContinentObject(ObjectCategorie):

    def __init__(self, name):
        self.name = name
        super().__init__("Continent")