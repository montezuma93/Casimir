from abc import ABC
from enum import Enum

class ObjectType(Enum):
    City = 1
    Country = 2
    Continent = 3

class Object(ABC):

    def __init__(self):
        pass

class ObjectCategorie(Object):

    def __init__(self, name):
        self.name = name

class CityObject(ObjectCategorie):
    object_type = ObjectType.City

    def __init__(self, name):
        super().__init__(name)

class CountryObject(ObjectCategorie):
    object_type = ObjectType.Country

    def __init__(self, name):
        super().__init__(name)

class ContinentObject(ObjectCategorie):
    object_type = ObjectType.Continent

    def __init__(self, name):
        super().__init__(name)
