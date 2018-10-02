import unittest
from LongTermMemory import LongTermMemory, RelationObject
from Relation import NorthCardinalRelation, SouthCardinalRelation, PartOfTopologicalRelation, CardinalRelation, RelationCategory
from Object import CityObject, CountryObject

class TestLongTermMemory(unittest.TestCase):

    def test_long_term_memory_can_save_one_relation_correctly(self):
        longTermMemory = LongTermMemory()
        parisCityObject = CityObject("Paris")
        londonCityObject = CityObject("London")
        northCardinalRelation = NorthCardinalRelation()
        relationObject = RelationObject(northCardinalRelation, [londonCityObject, parisCityObject])

        longTermMemory.save(relationObject)

        self.assertEqual(longTermMemory.storedRelations["CardinalRelation"][0].relation.name, "North")
        self.assertEqual(longTermMemory.storedRelations["CardinalRelation"][0].objectList[0].name, "London")
        self.assertEqual(longTermMemory.storedRelations["CardinalRelation"][0].objectList[1].name, "Paris")

    def test_long_term_memory_can_save_multiple_relation_correctly(self):
        longTermMemory = LongTermMemory()
        parisCityObject = CityObject("Paris")
        londonCityObject = CityObject("London")
        northCardinalRelation = NorthCardinalRelation()
        relationObject1 = RelationObject(northCardinalRelation, [londonCityObject, parisCityObject])
        kairoCityObject = CityObject("Kairo")
        southCardinalRelation = SouthCardinalRelation()
        relationObject2 = RelationObject(southCardinalRelation, [kairoCityObject, parisCityObject])

        longTermMemory.save(relationObject1)
        longTermMemory.save(relationObject2)

        self.assertEqual(longTermMemory.storedRelations["CardinalRelation"][0].relation.name, "North")
        self.assertEqual(longTermMemory.storedRelations["CardinalRelation"][0].objectList[0].name, "London")
        self.assertEqual(longTermMemory.storedRelations["CardinalRelation"][0].objectList[1].name, "Paris")
        self.assertEqual(longTermMemory.storedRelations["CardinalRelation"][1].relation.name, "South")
        self.assertEqual(longTermMemory.storedRelations["CardinalRelation"][1].objectList[0].name, "Kairo")
        self.assertEqual(longTermMemory.storedRelations["CardinalRelation"][1].objectList[1].name, "Paris")

    def test_long_term_memory_can_save_multiple_relation_categories_correctly(self):
        longTermMemory = LongTermMemory()
        parisCityObject = CityObject("Paris")
        londonCityObject = CityObject("London")
        northCardinalRelation = NorthCardinalRelation()
        relationObject1 = RelationObject(northCardinalRelation, [londonCityObject, parisCityObject])

        franceCountryObject = CountryObject("France")
        partOfTopologicalRelation = PartOfTopologicalRelation()
        relationObject2 = RelationObject(partOfTopologicalRelation, [parisCityObject, franceCountryObject])

        longTermMemory.save(relationObject1)
        longTermMemory.save(relationObject2)

        self.assertEqual(longTermMemory.storedRelations["CardinalRelation"][0], relationObject1)
        self.assertEqual(longTermMemory.storedRelations["TopologicalRelation"][0], relationObject2)
