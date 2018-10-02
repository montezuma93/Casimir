from abc import ABC

class Object(ABC):
    def __init__(self):
        pass

class ObjectCategorie(Object):

    def __init__(self, name):
        self.name = name

class CityObject(ObjectCategorie):
    category_name = "City"

    def __init__(self, name):
        super().__init__(name)

class CountryObject(ObjectCategorie):
    category_name = "Country"

    def __init__(self, name):
        super().__init__(name)

class ContinentObject(ObjectCategorie):
    category_name = "Continent"

    def __init__(self, name):
        super().__init__(name)
