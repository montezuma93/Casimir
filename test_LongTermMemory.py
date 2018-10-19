import unittest
from unittest import mock
from mock import call, patch
from LongTermMemory import LongTermMemory, KnowledgeSubnet
from Relation import EastCardinalRelation, NorthCardinalRelation, SouthCardinalRelation, PartOfTopologicalRelation, CardinalRelation, RelationCategory, CardinalRelationName, RelationType, TopologicalRelationName
from Object import CityObject, CountryObject

class TestLongTermMemory(unittest.TestCase):

    def test_long_term_memory_can_save_multiple_relations_with_equal_category_correctly(self):
        long_term_memory = LongTermMemory()
        paris_city_object = CityObject("Paris")
        london_city_object = CityObject("London")
        north_cardinal_relation = NorthCardinalRelation()
        cairo_city_object = CityObject("Cairo")
        south_cardinal_relation = SouthCardinalRelation()

        long_term_memory.save_knowledge_fragment(north_cardinal_relation, [london_city_object, paris_city_object])
        long_term_memory.save_knowledge_fragment(south_cardinal_relation, [cairo_city_object, paris_city_object])

        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].relation.name, CardinalRelationName.North)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].objects[0], "London")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].objects[1], "Paris")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].time_of_creation, 1)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].amount_of_usages, 1)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].relation.name, CardinalRelationName.South)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].objects[0], "Cairo")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].objects[1], "Paris")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].time_of_creation, 2)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].amount_of_usages, 1)
        
        self.assertEqual(long_term_memory.stored_objects["Paris"].time_of_creation, 1)
        self.assertEqual(long_term_memory.stored_objects["Paris"].amount_of_usages, 2)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[0], (RelationType.CardinalRelation, 0))
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[1], (RelationType.CardinalRelation, 1))

    def test_long_term_memory_can_save_multiple_relations_with_different_categories_correctly(self):
        long_term_memory = LongTermMemory()
        paris_city_object = CityObject("Paris")
        london_city_object = CityObject("London")
        north_cardinal_relation = NorthCardinalRelation()      
        france_country_object = CountryObject("France")
        part_of_topological_relation = PartOfTopologicalRelation()
        cairo_city_object = CityObject("Cairo")
        south_cardinal_relation = SouthCardinalRelation()

        long_term_memory.save_knowledge_fragment(north_cardinal_relation, [london_city_object, paris_city_object])
        long_term_memory.save_knowledge_fragment(part_of_topological_relation, [paris_city_object, france_country_object])
        long_term_memory.save_knowledge_fragment(south_cardinal_relation, [cairo_city_object, paris_city_object])

        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].objects[0], "London")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].objects[1], "Paris")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].time_of_creation, 1)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].amount_of_usages, 1)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].objects[0], "Cairo")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].objects[1], "Paris")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].time_of_creation, 3)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].amount_of_usages, 1)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].objects[0], "Paris")
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].objects[1], "France")
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].time_of_creation, 2)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].amount_of_usages, 1)
        self.assertEqual(long_term_memory.stored_objects["Paris"].stored_object, paris_city_object)
        self.assertEqual(long_term_memory.stored_objects["Paris"].time_of_creation, 1)
        self.assertEqual(long_term_memory.stored_objects["Paris"].amount_of_usages, 3)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[0][0], RelationType.CardinalRelation)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[0][1], 0)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[1][0], RelationType.TopologicalRelation)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[1][1], 0)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[2][0], RelationType.CardinalRelation)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[2][1], 1)
    
    @patch('LongTermMemory.LongTermMemory._set_initial_activation_for_entity')
    @patch('LongTermMemory.LongTermMemory._update_activation_values')
    @patch('LongTermMemory.LongTermMemory._spread_activation_for_entity')
    def test_spread_activation_should_call_the_correct_methods(self, mock_spread_activation_for_entity, mock_update_activation_values, mock_set_initial_activation_for_entity):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory.DYNAMIC_FIRINGHOLD = True
        long_term_memory.spread_activation([long_term_memory.paris_city_object, long_term_memory.london_city_object])
        mock_set_initial_activation_for_entity.assert_has_calls([call(long_term_memory.paris_city_object, 0.5), call(long_term_memory.london_city_object, 0.5)])
        mock_spread_activation_for_entity.assert_has_calls([call(long_term_memory.paris_city_object), call(long_term_memory.london_city_object)])
        self.assertEqual(mock_update_activation_values.call_count, 2)
        self.assertEqual(mock_spread_activation_for_entity.call_count, 2)

    def test_save_and_spread_activation_based_on_papers_example_with_dynamic_firing_threshold(self):
       
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory.DYNAMIC_FIRING_THRESHOLD = True
        long_term_memory.BASE_ACTIVATION_DECAY = -0.87
        long_term_memory.INITIAL_ACTIVATION_VALUE = 1.7

        long_term_memory.NOISE_ON = False

        retrieved_fragments = long_term_memory.receive_knowledge_fragments([RelationType.CardinalRelation, long_term_memory.paris_city_object, long_term_memory.london_city_object])
        
        self.assertEqual(len(retrieved_fragments.objects), 3)
        self.assertEqual(len(retrieved_fragments.relations[RelationType.CardinalRelation]), 2)
        self.assertFalse(retrieved_fragments.objects.__contains__(long_term_memory.france_country_object))
        self.assertFalse(retrieved_fragments.objects.__contains__(long_term_memory.england_country_object))
        self.assertFalse(retrieved_fragments.relations.__contains__(RelationType.TopologicalRelation))
        self.assertEqual(retrieved_fragments.relations[RelationType.CardinalRelation][0].relation, long_term_memory.south_cardinal_relation)
        self.assertEqual(retrieved_fragments.relations[RelationType.CardinalRelation][1].relation, long_term_memory.east_cardinal_relation)
        self.assertEqual(retrieved_fragments.objects["Paris"].stored_object, long_term_memory.paris_city_object)
        self.assertEqual(retrieved_fragments.objects["London"].stored_object, long_term_memory.london_city_object)
        self.assertEqual(retrieved_fragments.objects["Prague"].stored_object, long_term_memory.prague_city_object)

    def create_long_term_memory_based_on_papers_example(self):

        long_term_memory = LongTermMemory()

        long_term_memory.paris_city_object = CityObject("Paris")
        long_term_memory.prague_city_object = CityObject("Prague")
        long_term_memory.london_city_object = CityObject("London")
        long_term_memory.france_country_object = CountryObject("France")
        long_term_memory.england_country_object = CountryObject("England")
        long_term_memory.south_cardinal_relation = SouthCardinalRelation()
        long_term_memory.east_cardinal_relation = EastCardinalRelation()
        long_term_memory.part_of_topological_relation = PartOfTopologicalRelation()
        
        long_term_memory.save_knowledge_fragment(long_term_memory.part_of_topological_relation, [long_term_memory.paris_city_object, long_term_memory.france_country_object])
        long_term_memory.save_knowledge_fragment(long_term_memory.part_of_topological_relation, [long_term_memory.london_city_object, long_term_memory.england_country_object])
        long_term_memory.save_knowledge_fragment(long_term_memory.south_cardinal_relation, [long_term_memory.paris_city_object, long_term_memory.london_city_object])
        long_term_memory.save_knowledge_fragment(long_term_memory.east_cardinal_relation, [long_term_memory.prague_city_object, long_term_memory.paris_city_object]) 

        
        return long_term_memory
