import unittest
from LongTermMemory import LongTermMemory, RelationToObjectsMapping, ObjectToRelationMapping
from Relation import EastCardinalRelation, NorthCardinalRelation, SouthCardinalRelation, PartOfTopologicalRelation, CardinalRelation, RelationCategory, CardinalRelationName, RelationType, TopologicalRelationName
from Object import CityObject, CountryObject

class TestLongTermMemory(unittest.TestCase):
    
    def test_long_term_memory_can_save_one_relation_correctly(self):
        long_term_memory = LongTermMemory()
        paris_city_object = CityObject("Paris")
        london_city_object = CityObject("London")
        north_cardinal_relation = NorthCardinalRelation()
        relation_to_objects_mapping_1 = RelationToObjectsMapping(north_cardinal_relation, [london_city_object, paris_city_object])

        long_term_memory.save_relation_object_mapping(relation_to_objects_mapping_1)

        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].relation.relation_type, RelationType.CardinalRelation)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].relation.name, CardinalRelationName.North)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].object_list[0].name, "London")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].object_list[1].name, "Paris")

    def test_long_term_memory_can_save_multiple_relation_correctly(self):
        long_term_memory = LongTermMemory()
        paris_city_object = CityObject("Paris")
        london_city_object = CityObject("London")
        north_cardinal_relation = NorthCardinalRelation()
        relation_to_objects_mapping_1 = RelationToObjectsMapping(north_cardinal_relation, [london_city_object, paris_city_object])
        kairo_city_object = CityObject("Kairo")
        south_cardinal_relation = SouthCardinalRelation()
        relation_to_objects_mapping_2 = RelationToObjectsMapping(south_cardinal_relation, [kairo_city_object, paris_city_object])

        long_term_memory.save_relation_object_mapping(relation_to_objects_mapping_1)
        long_term_memory.save_relation_object_mapping(relation_to_objects_mapping_2)

        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].relation.name, CardinalRelationName.North)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].object_list[0].name, "London")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].object_list[1].name, "Paris")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].relation.name, CardinalRelationName.South)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].object_list[0].name, "Kairo")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].object_list[1].name, "Paris")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].time_of_initialization, 2)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].amout_of_usages, 1)
        self.assertEqual(long_term_memory.stored_objects["Paris"].time_of_initialization, 1)
        self.assertEqual(long_term_memory.stored_objects["Paris"].amount_of_usages, 2)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[0], (RelationType.CardinalRelation, 0))
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[1], (RelationType.CardinalRelation, 1))

    def test_long_term_memory_can_save_multiple_relation_categories_correctly(self):
        long_term_memory = LongTermMemory()
        paris_city_object = CityObject("Paris")
        london_city_object = CityObject("London")
        north_cardinal_relation = NorthCardinalRelation()
        relation_to_objects_mapping_1 = RelationToObjectsMapping(north_cardinal_relation, [london_city_object, paris_city_object])
        
        france_country_object = CountryObject("France")
        part_of_topological_relation = PartOfTopologicalRelation()
        relation_to_objects_mapping_2 = RelationToObjectsMapping(part_of_topological_relation, [paris_city_object, france_country_object])

        kairo_city_object = CityObject("Kairo")
        south_cardinal_relation = SouthCardinalRelation()
        relation_to_objects_mapping_3 = RelationToObjectsMapping(south_cardinal_relation, [kairo_city_object, paris_city_object])

        long_term_memory.save_relation_object_mapping(relation_to_objects_mapping_1)
        long_term_memory.save_relation_object_mapping(relation_to_objects_mapping_2)
        long_term_memory.save_relation_object_mapping(relation_to_objects_mapping_3)

        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0], relation_to_objects_mapping_1)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0], relation_to_objects_mapping_2)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].time_of_initialization, 1)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].amout_of_usages, 1)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].time_of_initialization, 2)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].amout_of_usages, 1)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[0][0], RelationType.CardinalRelation)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[0][1], 0)
        self.assertEqual(long_term_memory.stored_objects["Paris"].stored_object, paris_city_object)
        self.assertEqual(long_term_memory.stored_objects["Paris"].time_of_initialization, 1)
        self.assertEqual(long_term_memory.stored_objects["Paris"].amount_of_usages, 3)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[1][0], RelationType.TopologicalRelation)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[1][1], 0)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[2][0], RelationType.CardinalRelation)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[2][1], 1)
        self.assertEqual(long_term_memory.stored_objects["France"].stored_object, france_country_object)

        
    def test_save_and_recieve_knowledge_fragment_based_on_papers_example(self):
        
        long_term_memory = LongTermMemory()

        paris_city_object = CityObject("Paris")
        prague_city_object = CityObject("Prague")
        london_city_object = CityObject("London")
        france_country_object = CountryObject("France")
        england_country_object = CountryObject("England")
        south_cardinal_relation = SouthCardinalRelation()
        east_cardinal_relation = EastCardinalRelation()
        part_of_topological_relation = PartOfTopologicalRelation()

        relation_to_objects_mapping_1 = RelationToObjectsMapping(east_cardinal_relation, [prague_city_object, paris_city_object])
        relation_to_objects_mapping_2 = RelationToObjectsMapping(south_cardinal_relation, [paris_city_object, london_city_object])
        relation_to_objects_mapping_3 = RelationToObjectsMapping(part_of_topological_relation, [paris_city_object, france_country_object])
        relation_to_objects_mapping_4 = RelationToObjectsMapping(part_of_topological_relation, [london_city_object, england_country_object])

        long_term_memory.save_relation_object_mapping(relation_to_objects_mapping_1)
        long_term_memory.save_relation_object_mapping(relation_to_objects_mapping_2)
        long_term_memory.save_relation_object_mapping(relation_to_objects_mapping_3)
        long_term_memory.save_relation_object_mapping(relation_to_objects_mapping_4)

        most_activated_fragments = long_term_memory.receive_knowledge_fragments([RelationType.CardinalRelation, paris_city_object, london_city_object])
        
        self.assertEqual(long_term_memory.stored_objects["France"].stored_object.activation, 0.061599999999999995)
        self.assertEqual(long_term_memory.stored_objects["England"].stored_object.activation, 0.05999999999999999)
        self.assertEqual(long_term_memory.stored_objects["Prague"].stored_object.activation, 0.06999999999999999)
        self.assertEqual(long_term_memory.stored_objects["London"].stored_object.activation, 0.4033333333333333)
        self.assertEqual(long_term_memory.stored_objects["Paris"].stored_object.activation, 0.4533333333333333)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].activation, 0.12066666666666664)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][1].activation, 0.142)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation, 0.18466666666666665)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].activation, 0.26666666666666666)
        