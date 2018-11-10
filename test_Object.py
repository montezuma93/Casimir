import unittest
from Object import CityObject, CountryObject, ContinentObject, ObjectType

class TestObject(unittest.TestCase):

    def test_city_object_is_initialized_correctly(self):
        city_object = CityObject("Berlin")
        self.assertEqual(city_object.object_type, ObjectType.City)
        self.assertEqual(city_object.name, "Berlin")

    def test_country_object_is_initialized_correctly(self):
        country_object = CountryObject("Germany")
        self.assertEqual(country_object.object_type, ObjectType.Country)
        self.assertEqual(country_object.name, "Germany")
    
    def test_continent_object_is_initialized_correctly(self):
        continent_object = ContinentObject("Europe")
        self.assertEqual(continent_object.object_type, ObjectType.Continent)
        self.assertEqual(continent_object.name, "Europe")