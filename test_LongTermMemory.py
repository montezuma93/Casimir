import unittest
from LongTermMemory import LongTermMemory, RelationToObjectsMapping, ObjectToRelationMapping
from Relation import NorthCardinalRelation, SouthCardinalRelation, PartOfTopologicalRelation, CardinalRelation, RelationCategory, CardinalRelationName, RelationType
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
        self.assertEqual(long_term_memory.stored_objects["Paris"][0].relation_type, RelationType.CardinalRelation)
        self.assertEqual(long_term_memory.stored_objects["Paris"][0].reference_number, 0)
        self.assertEqual(long_term_memory.stored_objects["Paris"][0].stored_object, paris_city_object)
        self.assertEqual(long_term_memory.stored_objects["Paris"][1].relation_type, RelationType.TopologicalRelation)
        self.assertEqual(long_term_memory.stored_objects["Paris"][1].reference_number, 0)
        self.assertEqual(long_term_memory.stored_objects["Paris"][1].stored_object, paris_city_object)
        self.assertEqual(long_term_memory.stored_objects["Paris"][2].relation_type, RelationType.CardinalRelation)
        self.assertEqual(long_term_memory.stored_objects["Paris"][2].reference_number, 1)
        self.assertEqual(long_term_memory.stored_objects["Paris"][2].stored_object, paris_city_object)
        self.assertEqual(long_term_memory.stored_objects["France"][0].stored_object, france_country_object)

    def test_receive_knowledge_fragments_correctly(self):
        long_term_memory = LongTermMemory()

        paris_city_object = CityObject("Paris")
        london_city_object = CityObject("London")
        north_cardinal_relation = NorthCardinalRelation()
        relation_to_objects_mapping_1 = RelationToObjectsMapping(north_cardinal_relation, [london_city_object, paris_city_object])

        kairo_city_object = CityObject("Kairo")
        south_cardinal_relation = SouthCardinalRelation()
        relation_to_objects_mapping_2 = RelationToObjectsMapping(south_cardinal_relation, [kairo_city_object, paris_city_object])

        france_country_object = CountryObject("France")
        part_of_topological_relation = PartOfTopologicalRelation()
        relation_to_objects_mapping_3 = RelationToObjectsMapping(part_of_topological_relation, [paris_city_object, france_country_object])

        aberdeen_city_object = CityObject("Aberdeen")
        relation_to_objects_mapping_4 = RelationToObjectsMapping(north_cardinal_relation, [aberdeen_city_object, london_city_object])

        long_term_memory.save_relation_object_mapping(relation_to_objects_mapping_1)
        long_term_memory.save_relation_object_mapping(relation_to_objects_mapping_2)
        long_term_memory.save_relation_object_mapping(relation_to_objects_mapping_3)

        long_term_memory._set_initial_activation(north_cardinal_relation.relation_type, aberdeen_city_object, london_city_object)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation, 1)
        self.assertEqual(long_term_memory.stored_objects["Paris"][0].activation, 0)
        self.assertEqual(long_term_memory.stored_objects["London"][0].activation, 1)
        self.assertEqual(long_term_memory._firing_node_exists(), True)

        long_term_memory._update_linked_activation_for_relation(long_term_memory.stored_relations[RelationType.CardinalRelation][0])

        self.assertEqual(long_term_memory.stored_objects["Paris"][0].activation, 0.675)
        self.assertEqual(long_term_memory.stored_objects["Paris"][1].activation, 0.675)
        self.assertEqual(long_term_memory.stored_objects["Paris"][2].activation, 0.675)
        self.assertEqual(long_term_memory.stored_objects["London"][0].activation, 1)

        long_term_memory._update_linked_activation_for_object(long_term_memory.stored_objects["London"][0])

        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation, 1)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].activation, 1)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].activation, 0)

        long_term_memory._update_unchanged_activation_mappings()
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].activation, 0.9)

        long_term_memory.DECAY = 0.75
        long_term_memory.FIRING_THRESHOLD = 0.75
        long_term_memory.RELATION_OBJECT_LINK_WEIGHT = 0.5
        long_term_memory.OBJECT_RELATION_LINK_WEIGHT = 0.25
        long_term_memory.RETRIEVAL_ACTIVATION_THRESHOLD = 0.6

        long_term_memory._spread_activation(part_of_topological_relation.relation_type, london_city_object, aberdeen_city_object)
        
        self.assertEqual(long_term_memory.stored_objects["France"][0].activation, 0.65625)
        self.assertEqual(long_term_memory.stored_objects["London"][0].activation, 0.5625)
        self.assertEqual(long_term_memory.stored_objects["Paris"][0].activation, 0.65625)
        self.assertEqual(long_term_memory.stored_objects["Paris"][1].activation, 0.65625)
        self.assertEqual(long_term_memory.stored_objects["Paris"][2].activation, 0.65625)
        self.assertEqual(long_term_memory.stored_objects["Kairo"][0].activation, 0)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation, 0.328125)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].activation, 0.0)
       
        most_activated_fragments = long_term_memory._get_most_activated_fragments()

        self.assertEqual(len(most_activated_fragments), 4)

        self.assertEqual(most_activated_fragments[0].stored_object, paris_city_object)
        self.assertEqual(most_activated_fragments[0].relation_type, RelationType.CardinalRelation)
        self.assertEqual(most_activated_fragments[0].reference_number, 0)