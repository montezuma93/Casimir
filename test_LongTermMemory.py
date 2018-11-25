import unittest
from unittest import mock
from mock import call, patch
from LongTermMemoryService import LongTermMemoryService, KnowledgeSubnet
from Relation import EastCardinalRelation, NorthCardinalRelation, SouthCardinalRelation, PartOfTopologicalRelation, CardinalRelation, RelationCategory, CardinalRelationName, RelationType, TopologicalRelationName
from Object import CityObject, CountryObject

class TestLongTermMemory(unittest.TestCase):

    def test_long_term_memory_can_save_multiple_relations_with_equal_category_correctly(self):
        long_term_memory = LongTermMemoryService()
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
        long_term_memory = LongTermMemoryService()
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
    
    @patch('LongTermMemoryService.LongTermMemoryService._set_initial_activation_for_entity')
    @patch('LongTermMemoryService.LongTermMemoryService._update_activation_values')
    @patch('LongTermMemoryService.LongTermMemoryService._spread_activation_for_entity')
    def test_spread_activation_should_call_the_correct_methods(self, mock_spread_activation_for_entity, mock_update_activation_values, mock_set_initial_activation_for_entity):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()

        long_term_memory.spread_activation([long_term_memory.paris_city_object, long_term_memory.london_city_object])

        mock_set_initial_activation_for_entity.assert_has_calls([call(long_term_memory.paris_city_object, 0.5), call(long_term_memory.london_city_object, 0.5)])
        self.assertEqual(mock_update_activation_values.call_count, 2)
        self.assertEqual(mock_spread_activation_for_entity.call_count, 2)

    @patch('LongTermMemoryService.LongTermMemoryService.spread_activation')
    @patch('LongTermMemoryService.LongTermMemoryService.calculate_base_activation')
    @patch('LongTermMemoryService.LongTermMemoryService.add_noise_to_activation')
    def test_calculate_activation_should_call_the_correct_methods_with_noise_off(self, mock_add_noise_to_activation, mock_calculate_base_activation, mock_spread_activation):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory.NOISE_ON = False

        long_term_memory.calculate_activation([long_term_memory.paris_city_object, long_term_memory.london_city_object])

        self.assertEqual(mock_calculate_base_activation.call_count, 1)
        mock_spread_activation.assert_has_calls([call([long_term_memory.paris_city_object, long_term_memory.london_city_object])])
        self.assertEqual(mock_add_noise_to_activation.call_count, 0)

    @patch('LongTermMemoryService.LongTermMemoryService.spread_activation')
    @patch('LongTermMemoryService.LongTermMemoryService.calculate_base_activation')
    @patch('LongTermMemoryService.LongTermMemoryService.add_noise_to_activation')
    def test_calculate_activation_should_call_the_correct_methods_with_noise_on(self, mock_add_noise_to_activation, mock_calculate_base_activation, mock_spread_activation):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory.NOISE_ON = True

        long_term_memory.calculate_activation([long_term_memory.paris_city_object])

        self.assertEqual(mock_calculate_base_activation.call_count, 1)
        mock_spread_activation.assert_has_calls([call([long_term_memory.paris_city_object])])
        self.assertEqual(mock_add_noise_to_activation.call_count, 1)

    def test_firing_threshold_should_be_set_correctly(self):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory.DYNAMIC_FIRING_THRESHOLD = True

        long_term_memory.spread_activation([long_term_memory.paris_city_object, long_term_memory.london_city_object])

        self.assertEqual(long_term_memory.FIRING_THRESHOLD, 0.0002)

    @patch('LongTermMemoryService.LongTermMemoryService._clean_up_activation_values')
    def test_set_initial_activation_should_set_activation_value_for_object_entity(self, mock__clean_up_activation_values):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()

        long_term_memory._set_initial_activation_for_entity(long_term_memory.paris_city_object, 1)

        self.assertEqual(mock__clean_up_activation_values.call_count, 1)
        self.assertEqual(long_term_memory.stored_objects["Paris"].is_active, True)
        self.assertEqual(long_term_memory.stored_objects["Paris"].activation_to_update, 1)
        self.assertEqual(long_term_memory.stored_objects["London"].is_active, False)
        self.assertEqual(long_term_memory.stored_objects["London"].activation_to_update, 0)
        self.assertEqual(long_term_memory.stored_objects["Prague"].is_active, False)
        self.assertEqual(long_term_memory.stored_objects["Prague"].activation_to_update, 0)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation_to_update, 0)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].is_active, False)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].activation_to_update, 0)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].is_active, False)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].activation_to_update, 0)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].is_active, False)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][1].activation_to_update, 0)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][1].is_active, False)
    
    @patch('LongTermMemoryService.LongTermMemoryService._clean_up_activation_values')
    def test_set_initial_activation_should_set_activation_value_for_relation_entity(self, mock_clean_up_activation_values):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()

        long_term_memory._set_initial_activation_for_entity(RelationType.CardinalRelation, 1)

        self.assertEqual(mock_clean_up_activation_values.call_count, 1)
        self.assertEqual(long_term_memory.stored_objects["Paris"].is_active, False)
        self.assertEqual(long_term_memory.stored_objects["Paris"].activation_to_update, 0)
        self.assertEqual(long_term_memory.stored_objects["London"].is_active, False)
        self.assertEqual(long_term_memory.stored_objects["London"].activation_to_update, 0)
        self.assertEqual(long_term_memory.stored_objects["Prague"].is_active, False)
        self.assertEqual(long_term_memory.stored_objects["Prague"].activation_to_update, 0)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation_to_update, 0.3)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].is_active, True)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].activation_to_update, 0.3)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].is_active, True)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].activation_to_update, 0)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].is_active, False)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][1].activation_to_update, 0)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][1].is_active, False)

    def test_spread_activation_for_object_should_spread_activation_correctly(self):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory.FIRING_THRESHOLD = 0.1
        long_term_memory.NOISE_ON = False
        long_term_memory._clean_up_activation_values()
        long_term_memory.stored_objects["Paris"].is_active = True
        long_term_memory.stored_objects["Paris"].activation_to_update = 1

        long_term_memory._spread_activation_for_entity()

        self.assertEqual(long_term_memory.stored_objects["Paris"].is_active, True)
        self.assertEqual(long_term_memory.stored_objects["Paris"].activation_to_update, 1)
        self.assertEqual(long_term_memory.stored_objects["London"].is_active, True)
        self.assertAlmostEqual(long_term_memory.stored_objects["London"].activation_to_update, 0.12)
        self.assertEqual(long_term_memory.stored_objects["Prague"].is_active, True)
        self.assertAlmostEqual(long_term_memory.stored_objects["Prague"].activation_to_update, 0.12)
        self.assertEqual(long_term_memory.stored_objects["France"].is_active, True)
        self.assertAlmostEqual(long_term_memory.stored_objects["France"].activation_to_update, 0.12)
        self.assertEqual(long_term_memory.stored_objects["England"].is_active, False)
        self.assertEqual(long_term_memory.stored_objects["England"].activation_to_update, 0)
        self.assertAlmostEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation_to_update, 0.2)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].is_active, True)
        self.assertAlmostEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].activation_to_update, 0.2)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].is_active, True)
        self.assertAlmostEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].activation_to_update, 0.2)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].is_active, True)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][1].activation_to_update, 0)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][1].is_active, False)
    
    def test_spread_activation_for_relation_should_be_called_correct_amount_of_times_spread_activation_correctly(self):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory.FIRING_THRESHOLD = 0.05
        long_term_memory.NOISE_ON = False
        long_term_memory._clean_up_activation_values()
        long_term_memory.stored_relations[RelationType.CardinalRelation][0].is_active = True
        long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation_to_update = 0.2
        long_term_memory.stored_relations[RelationType.CardinalRelation][1].is_active = True
        long_term_memory.stored_relations[RelationType.CardinalRelation][1].activation_to_update = 0.2

        long_term_memory._spread_activation_for_entity()

        self.assertEqual(long_term_memory.stored_objects["Paris"].is_active, True)
        self.assertEqual(long_term_memory.stored_objects["Paris"].activation_to_update, 0.12)
        self.assertEqual(long_term_memory.stored_objects["London"].is_active, True)
        self.assertEqual(long_term_memory.stored_objects["London"].activation_to_update, 0.06)
        self.assertEqual(long_term_memory.stored_objects["Prague"].is_active, True)
        self.assertEqual(long_term_memory.stored_objects["Prague"].activation_to_update, 0.06)
        self.assertEqual(long_term_memory.stored_objects["France"].is_active, False)
        self.assertEqual(long_term_memory.stored_objects["France"].activation_to_update, 0)
        self.assertEqual(long_term_memory.stored_objects["England"].is_active, False)
        self.assertEqual(long_term_memory.stored_objects["England"].activation_to_update, 0)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation_to_update, 0.2)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].is_active, True)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].activation_to_update, 0.2)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].is_active, True)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].activation_to_update, 0.072)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].is_active, True)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][1].activation_to_update, 0)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][1].is_active, False)

    def test_update_activation_values_correctly_updates_values_for_entities(self):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory._clean_up_activation_values()
        long_term_memory.stored_objects["Paris"].activation = 0.1
        long_term_memory.stored_objects["Paris"].activation_to_update = 0.1
        long_term_memory.stored_objects["London"].activation_to_update = 0.2
        long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation = 0.3
        long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation_to_update = 0.3
        long_term_memory.stored_relations[RelationType.TopologicalRelation][1].activation_to_update = 0.4

        long_term_memory._update_activation_values()

        self.assertEqual(long_term_memory.stored_objects["Paris"].activation, 0.2)
        self.assertEqual(long_term_memory.stored_objects["London"].activation, 0.2)
        self.assertEqual(long_term_memory.stored_objects["Prague"].activation, 0)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation, 0.6)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].activation, 0)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][1].activation, 0.4)

    @patch('LongTermMemoryService.LongTermMemoryService.calculate_activation')
    @patch('LongTermMemoryService.LongTermMemoryService._calculate_retrieval_threshold')
    @patch('LongTermMemoryService.LongTermMemoryService.get_knowledge_subnets')
    @patch('LongTermMemoryService.LongTermMemoryService.get_most_activated_knowledge_subnet')
    def test_receive_knowledge_fragments_should_call_the_right_methods(self, mock_get_most_activated_knowledge_subnet, mock_get_knowledge_subnets, mock_calculate_retrieval_threshold, mock_calculate_activation):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        mock_calculate_retrieval_threshold.return_value = 0.1
        expected_knowledge_subnets = [KnowledgeSubnet(long_term_memory.stored_relations[RelationType.CardinalRelation][0])]
        mock_get_knowledge_subnets.return_value = expected_knowledge_subnets
        
        long_term_memory.receive_knowledge_fragments([long_term_memory.paris_city_object])

        mock_calculate_activation.assert_has_calls([call([long_term_memory.paris_city_object])])   
        self.assertEqual(mock_calculate_retrieval_threshold.call_count, 1)
        mock_get_knowledge_subnets.assert_has_calls([call(0.1)])   
        mock_get_most_activated_knowledge_subnet.assert_has_calls([call(expected_knowledge_subnets)])

    @patch('LongTermMemoryService.LongTermMemoryService._calculate_base_activation_for_node')
    def test_calculate_base_activation_for_node_should_be_called_correct_amount_of_times(self, mock_calculate_base_activation_for_node):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        
        long_term_memory.calculate_base_activation()

        self.assertEqual(mock_calculate_base_activation_for_node.call_count, 9)

    def test_calculate_base_activation_for_node_with_multiple_usages_should_be_calculated_correctly(self):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory.BASE_ACTIVATION_DECAY = -0.5
        long_term_memory.time_since_initialization = 5
        long_term_memory.stored_objects["Paris"].usages = [1, 3, 4]

        self.assertAlmostEqual(long_term_memory._calculate_base_activation_for_node(long_term_memory.stored_objects["Paris"]), 0.79168250906)

    def test_calculate_base_activation_for_node_with_one_usage_should_be_calculated_correctly(self):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory.BASE_ACTIVATION_DECAY = -0.5
        long_term_memory.time_since_initialization = 5
        long_term_memory.stored_objects["Paris"].usages = [3]

        self.assertAlmostEqual(long_term_memory._calculate_base_activation_for_node(long_term_memory.stored_objects["Paris"]), -0.34657359028)

    @patch('LongTermMemoryService.LongTermMemoryService._calculate_noise_for_node')
    def test_calculate_noise(self, mock_calculate_noise_for_node):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        mock_calculate_noise_for_node.return_value = 0.1
        long_term_memory.stored_objects["Paris"].activation = 0.2

        long_term_memory.add_noise_to_activation()

        self.assertAlmostEqual(long_term_memory.stored_objects["Paris"].activation, 0.3)

    def test_relation_not_yet_used_in_knowledge_subnet_for_empty_knowledge_subnet_list(self):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()

        self.assertTrue(long_term_memory._relation_not_yet_used_in_knowledge_subnet([],long_term_memory.stored_relations[RelationType.CardinalRelation][0]))

    def test_relation_not_yet_used_in_knowledge_subnet_for_unused_relation(self):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        knowledge_subnet1 = KnowledgeSubnet(long_term_memory.stored_relations[RelationType.CardinalRelation][1])
        knowledge_subnet2 = KnowledgeSubnet(long_term_memory.stored_relations[RelationType.TopologicalRelation][0])
        knowledge_subnet2.relations[RelationType.TopologicalRelation].append(long_term_memory.stored_relations[RelationType.TopologicalRelation][1])
        knowledge_subnets = [knowledge_subnet1,knowledge_subnet2]

        self.assertTrue(long_term_memory._relation_not_yet_used_in_knowledge_subnet(knowledge_subnets,
         long_term_memory.stored_relations[RelationType.CardinalRelation][0]))
    
    def test_relation_not_yet_used_in_knowledge_subnet_for_used_relation(self):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        knowledge_subnet1 = KnowledgeSubnet(long_term_memory.stored_relations[RelationType.CardinalRelation][1])
        knowledge_subnet2 = KnowledgeSubnet(long_term_memory.stored_relations[RelationType.TopologicalRelation][0])
        knowledge_subnet2.relations[RelationType.TopologicalRelation].append(long_term_memory.stored_relations[RelationType.TopologicalRelation][1])
        knowledge_subnets = [knowledge_subnet1,knowledge_subnet2]

        self.assertFalse(long_term_memory._relation_not_yet_used_in_knowledge_subnet(knowledge_subnets,
         long_term_memory.stored_relations[RelationType.TopologicalRelation][1]))

    def test_retrieve_activated_nodes_through_knowledge_subnet_should_be_called_correct_amount_of_times(self):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        knowledge_subnet = KnowledgeSubnet(long_term_memory.stored_relations[RelationType.CardinalRelation][1])
        long_term_memory.stored_objects["Paris"].activation = 1
        long_term_memory.stored_objects["London"].activation = 1
        long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation = 1
        long_term_memory.stored_relations[RelationType.CardinalRelation][1].activation = 0

        long_term_memory.retrieve_activated_nodes_through_knowledge_subnet(knowledge_subnet, 0.5)

        self.assertTrue(knowledge_subnet.relations[RelationType.CardinalRelation][0].objects.__contains__("Paris"))
        self.assertFalse(knowledge_subnet.relations[RelationType.CardinalRelation][0].objects.__contains__("London"))
    
    def test_get_knowledge_subnets_returns_the_correct_subnet(self):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory.stored_objects["Paris"].activation = 1
        long_term_memory.stored_objects["London"].activation = 1
        long_term_memory.stored_objects["Prague"].activation = 1
        long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation = 1
        long_term_memory.stored_relations[RelationType.CardinalRelation][1].activation = 0
        long_term_memory.stored_relations[RelationType.TopologicalRelation][1].activation = 1
        long_term_memory.stored_relations[RelationType.TopologicalRelation][0].activation = 1

        actual_knowledge_subnets = long_term_memory.get_knowledge_subnets(0.5)

        self.assertEqual(len(actual_knowledge_subnets), 1)
        self.assertEqual(len(actual_knowledge_subnets[0].relations[RelationType.CardinalRelation]), 1)
        self.assertEqual(len(actual_knowledge_subnets[0].relations[RelationType.TopologicalRelation]), 2)
        self.assertEqual(len(actual_knowledge_subnets[0].objects), 2)

    def test_get_knowledge_subnets_returns_the_correct_subnets(self):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory.stored_objects["London"].activation = 1
        long_term_memory.stored_objects["Prague"].activation = 1
        long_term_memory.stored_objects["England"].activation = 1
        long_term_memory.stored_objects["France"].activation = 1
        long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation = 0
        long_term_memory.stored_relations[RelationType.CardinalRelation][1].activation = 1
        long_term_memory.stored_relations[RelationType.TopologicalRelation][1].activation = 1
        long_term_memory.stored_relations[RelationType.TopologicalRelation][0].activation = 1

        actual_knowledge_subnets = long_term_memory.get_knowledge_subnets(0.5)

        self.assertEqual(len(actual_knowledge_subnets), 3)
        self.assertEqual(len(actual_knowledge_subnets[0].relations[RelationType.TopologicalRelation]), 1)
        self.assertEqual(len(actual_knowledge_subnets[0].objects), 1)
        self.assertEqual(len(actual_knowledge_subnets[1].relations[RelationType.TopologicalRelation]), 1)
        self.assertEqual(len(actual_knowledge_subnets[1].objects), 2)
        self.assertEqual(len(actual_knowledge_subnets[2].relations[RelationType.CardinalRelation]), 1)
        self.assertEqual(len(actual_knowledge_subnets[2].objects), 1)

    
    def test_get_most_activated_knowledge_subnet(self):
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory.stored_objects["Paris"].activation = 1
        long_term_memory.stored_objects["London"].activation = 1
        long_term_memory.stored_objects["Prague"].activation = 1
        long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation = 1
        long_term_memory.stored_relations[RelationType.CardinalRelation][1].activation = 0
        long_term_memory.stored_relations[RelationType.TopologicalRelation][1].activation = 1
        long_term_memory.stored_relations[RelationType.TopologicalRelation][0].activation = 1

        actual_knowledge_subnets = long_term_memory.get_knowledge_subnets(0.5)
        most_activated_knowledge_subnet = long_term_memory.get_most_activated_knowledge_subnet(actual_knowledge_subnets)

        self.assertEquals(most_activated_knowledge_subnet.relations[RelationType.CardinalRelation][0], long_term_memory.stored_relations[RelationType.CardinalRelation][0])
        self.assertEquals(most_activated_knowledge_subnet.objects["Paris"].stored_object.name, "Paris")
        self.assertEquals(most_activated_knowledge_subnet.objects["London"].stored_object.name, "London")
    
    def test_save_and_spread_activation_based_on_papers_example_with_dynamic_firing_threshold(self): 
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory.DYNAMIC_FIRING_THRESHOLD = True
        long_term_memory.BASE_ACTIVATION_DECAY = -0.86
        long_term_memory.INITIAL_ACTIVATION_VALUE = 1.8
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
        self.assertEqual(long_term_memory.stored_objects["Paris"].usages, [1,3,4,5])
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].usages, [3,5])
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].usages, [4,5])
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].usages, [1])
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][1].usages, [2])
    
    def create_long_term_memory_based_on_papers_example(self):
        long_term_memory = LongTermMemoryService()
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
