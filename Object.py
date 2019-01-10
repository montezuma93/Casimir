from abc import ABC
from enum import Enum

class ObjectType(Enum):
    City = "City"
    Country = "Country"
    Continent = "Continent"
    Miscellaneous= "Miscellaneous"

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

class MiscellaneousObject(ObjectCategorie):
    object_type = ObjectType.Miscellaneous

    def __init__(self, name):
        super().__init__(name)
