import unittest
from LongTermMemory import LongTermMemory, StoredRelation, StoredObject
from Relation import NorthCardinalRelation, SouthCardinalRelation, PartOfTopologicalRelation, CardinalRelation, RelationCategory
from Object import CityObject, CountryObject

class TestLongTermMemory(unittest.TestCase):

    def test_long_term_memory_can_save_one_relation_correctly(self):
        long_term_memory = LongTermMemory()
        paris_city_object = CityObject("Paris")
        london_city_object = CityObject("London")
        north_cardinal_relation = NorthCardinalRelation()
        relation_object_1 = StoredRelation(north_cardinal_relation, [london_city_object, paris_city_object])

        long_term_memory.save_object_relation(relation_object_1)

        self.assertEqual(long_term_memory.stored_relations["CardinalRelation"][0].relation.name, "North")
        self.assertEqual(long_term_memory.stored_relations["CardinalRelation"][0].object_list[0].name, "London")
        self.assertEqual(long_term_memory.stored_relations["CardinalRelation"][0].object_list[1].name, "Paris")

    def test_long_term_memory_can_save_multiple_relation_correctly(self):
        long_term_memory = LongTermMemory()
        paris_city_object = CityObject("Paris")
        london_city_object = CityObject("London")
        north_cardinal_relation = NorthCardinalRelation()
        relation_object_1 = StoredRelation(north_cardinal_relation, [london_city_object, paris_city_object])
        kairoCityObject = CityObject("Kairo")
        south_cardinal_relation = SouthCardinalRelation()
        relation_object_2 = StoredRelation(south_cardinal_relation, [kairoCityObject, paris_city_object])

        long_term_memory.save_object_relation(relation_object_1)
        long_term_memory.save_object_relation(relation_object_2)

        self.assertEqual(long_term_memory.stored_relations["CardinalRelation"][0].relation.name, "North")
        self.assertEqual(long_term_memory.stored_relations["CardinalRelation"][0].object_list[0].name, "London")
        self.assertEqual(long_term_memory.stored_relations["CardinalRelation"][0].object_list[1].name, "Paris")
        self.assertEqual(long_term_memory.stored_relations["CardinalRelation"][1].relation.name, "South")
        self.assertEqual(long_term_memory.stored_relations["CardinalRelation"][1].object_list[0].name, "Kairo")
        self.assertEqual(long_term_memory.stored_relations["CardinalRelation"][1].object_list[1].name, "Paris")

    def test_long_term_memory_can_save_multiple_relation_categories_correctly(self):
        long_term_memory = LongTermMemory()
        paris_city_object = CityObject("Paris")
        london_city_object = CityObject("London")
        north_cardinal_relation = NorthCardinalRelation()
        relation_object_1 = StoredRelation(north_cardinal_relation, [london_city_object, paris_city_object])

        france_country_object = CountryObject("France")
        part_of_topological_relation = PartOfTopologicalRelation()
        relation_object_2 = StoredRelation(part_of_topological_relation, [paris_city_object, france_country_object])

        long_term_memory.save_object_relation(relation_object_1)
        long_term_memory.save_object_relation(relation_object_2)

        self.assertEqual(long_term_memory.stored_relations["CardinalRelation"][0], relation_object_1)
        self.assertEqual(long_term_memory.stored_relations["TopologicalRelation"][0], relation_object_2)
        self.assertEqual(long_term_memory.stored_objects["Paris"][0].relation_category,"CardinalRelation")
        self.assertEqual(long_term_memory.stored_objects["Paris"][0].reference_number, 0)
        self.assertEqual(long_term_memory.stored_objects["Paris"][1].relation_category,"TopologicalRelation")
        self.assertEqual(long_term_memory.stored_objects["Paris"][1].reference_number, 0)