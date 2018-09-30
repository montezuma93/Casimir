import unittest
from Object import CityObject, CountryObject, ContinentObject

class TestObject(unittest.TestCase):

    def test_city_object_is_initialized_correctly(self):
        city_object = CityObject("Berlin")
        self.assertEqual(city_object.category_name, "City")
        self.assertEqual(city_object.name, "Berlin")

    def test_country_object_is_initialized_correctly(self):
        country_object = CountryObject("Germany")
        self.assertEqual(country_object.category_name, "Country")
        self.assertEqual(country_object.name, "Germany")
    
    def test_continent_object_is_initialized_correctly(self):
        continent_object = ContinentObject("Europe")
        self.assertEqual(continent_object.category_name, "Continent")
        self.assertEqual(continent_object.name, "Europe")