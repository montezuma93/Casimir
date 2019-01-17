import unittest
from collections import OrderedDict
from CasimirSimulation import CasimirSimulation
from flask import Flask, request, json, jsonify
from flask_restplus import Resource, Api, reqparse, Swagger,fields
from flask.views import View
from mock import call, patch
from Object import MiscellaneousObject, CityObject
from LongTermMemoryService import KnowledgeSubnet
from Relation import NorthCardinalRelation, SouthCardinalRelation, EastCardinalRelation, CardinalRelation, RelationType, SpatialRelation, LeftSpatialRelation, RightSpatialRelation

app = Flask(__name__)

class TestCasimirSimulation(unittest.TestCase):
    
    def test_casimir_simulation_is_initialized_correctly(self):
        casimir_simulation = CasimirSimulation(app)
        self.assertIsNotNone(casimir_simulation.long_term_memory_controller)
        self.assertIsNotNone(casimir_simulation.long_term_memory_controller)

    @patch('WorkingMemoryController.WorkingMemoryController.update_settings')
    @patch('LongTermMemoryController.LongTermMemoryController.update_settings')
    def test_update_setting_call_the_correct_methods_in_controller(self, mock_ltm_controller_update_settings, mock_wm_controller_update_settings):
        casimir_simulation = CasimirSimulation(app)

        casimir_simulation.update_settings(1, 2, 3, 4,True, 5, False, True, False, 3)
        
        mock_ltm_controller_update_settings.assert_has_calls([call(1, 2, 3, 4, True, 5, False, True)])
        mock_wm_controller_update_settings.assert_has_calls([call(False)])
    
    @patch('WorkingMemoryService.WorkingMemoryService.update_settings')
    @patch('LongTermMemoryService.LongTermMemoryService.update_settings')
    def test_update_setting_call_the_correct_methods_in_services(self, mock_ltm_service_update_settings, mock_wm_service_update_settings):
        casimir_simulation = CasimirSimulation(app)

        casimir_simulation.update_settings(1, 2, 3, 4,True, 5, False, True, False, 3)

        mock_ltm_service_update_settings.assert_has_calls([call(1, 2, 3, 4, True, 5, False, True)])
        mock_wm_service_update_settings.assert_has_calls([call(False)])

    def test_reset_simulation(self):
        casimir_simulation = CasimirSimulation(app)
        casimir_simulation.long_term_memory_controller.long_term_memory_service.stored_objects["A"] = "Filled"
        casimir_simulation.working_memory_controller.working_memory_service.stored_spatial_mental_models.append("SMM")

        casimir_simulation.reset_simulation()

        self.assertFalse(casimir_simulation.long_term_memory_controller.long_term_memory_service.stored_objects.__contains__("A"))
        self.assertFalse(casimir_simulation.working_memory_controller.working_memory_service.stored_spatial_mental_models.__contains__("SMM"))
    
    @patch('LongTermMemoryService.LongTermMemoryService.save_knowledge_fragment')
    def test_save_knowledge_fragment_calling_the_correct_methods(self, mock_save_knowledge_fragment):
        casimir_simulation = CasimirSimulation(app)
        relation_to_save = NorthCardinalRelation()
        object1_to_save = MiscellaneousObject("A")
        object2_to_save = MiscellaneousObject("B")

        casimir_simulation.save_knowledge_fragment(relation_to_save, [object1_to_save, object2_to_save])

        mock_save_knowledge_fragment.assert_has_calls([call(relation_to_save, [object1_to_save, object2_to_save])])
    

    @patch('CasimirSimulation.CasimirSimulation._received_all_necessary_nodes')
    @patch('LongTermMemoryController.LongTermMemoryController.receive_knowledge_fragments')
    def test_create_mental_image_call_the_correct_methods(self, mock_receive_knowledge_fragments, mock_received_all_necessary_nodes):
        casimir_simulation = CasimirSimulation(app)
        casimir_simulation.MAX_AMOUNT_OF_RETRIES = 3
        paris_city_object = CityObject("Paris")
        prague_city_object = CityObject("Prague")
        london_city_object = CityObject("London")
        south_cardinal_relation = SouthCardinalRelation()
        east_cardinal_relation = EastCardinalRelation()
        casimir_simulation.save_knowledge_fragment(south_cardinal_relation, [paris_city_object, london_city_object])
        casimir_simulation.save_knowledge_fragment(east_cardinal_relation, [prague_city_object, paris_city_object])
        mock_receive_knowledge_fragments.side_effect = [KnowledgeSubnet(casimir_simulation.long_term_memory_controller.
          long_term_memory_service.stored_relations[RelationType.CardinalRelation][0]), KnowledgeSubnet(casimir_simulation.long_term_memory_controller.
          long_term_memory_service.stored_relations[RelationType.CardinalRelation][1])]
        mock_received_all_necessary_nodes.side_effect = [False, True]

        casimir_simulation.create_mental_image([CardinalRelation, [paris_city_object, london_city_object]])

        self.assertEqual(mock_received_all_necessary_nodes.call_count, 2)


    def test_get_all_objects_names_in_context_array(self):
        casimir_simulation = CasimirSimulation(app)
        paris_city_object = CityObject("Paris")
        london_city_object = CityObject("London")
        context_array = [CardinalRelation, paris_city_object, london_city_object]

        object_name_list = casimir_simulation._get_all_objects_names_in_context_array(context_array)
        self.assertEquals(object_name_list[0], "Paris")
        self.assertEquals(object_name_list[1], "London")

    def test_received_all_necessary_nodes_should_return_true(self):
        casimir_simulation = CasimirSimulation(app)
        paris_city_object = CityObject("Paris")
        prague_city_object = CityObject("Prague")
        london_city_object = CityObject("London")
        south_cardinal_relation = SouthCardinalRelation()
        east_cardinal_relation = EastCardinalRelation()
        casimir_simulation.save_knowledge_fragment(south_cardinal_relation, [paris_city_object, london_city_object])
        casimir_simulation.save_knowledge_fragment(east_cardinal_relation, [prague_city_object, paris_city_object])
        objects_to_receive = ["Paris", "London"]
        knowledge_subnet = KnowledgeSubnet(casimir_simulation.long_term_memory_controller.
          long_term_memory_service.stored_objects["Paris"])
        knowledge_subnet.objects["London"] = london_city_object

        self.assertTrue(casimir_simulation._received_all_necessary_nodes(objects_to_receive, knowledge_subnet))
    
    def test_received_all_necessary_nodes_should_return_false(self):
        casimir_simulation = CasimirSimulation(app)
        paris_city_object = CityObject("Paris")
        prague_city_object = CityObject("Prague")
        london_city_object = CityObject("London")
        south_cardinal_relation = SouthCardinalRelation()
        east_cardinal_relation = EastCardinalRelation()
        casimir_simulation.save_knowledge_fragment(south_cardinal_relation, [paris_city_object, london_city_object])
        casimir_simulation.save_knowledge_fragment(east_cardinal_relation, [prague_city_object, paris_city_object])
        objects_to_receive = ["Paris", "London"]
        
        knowledge_subnet = KnowledgeSubnet(casimir_simulation.long_term_memory_controller.
          long_term_memory_service.stored_objects["Paris"])
        knowledge_subnet.objects["Prague"] = prague_city_object

        self.assertFalse(casimir_simulation._received_all_necessary_nodes(objects_to_receive, knowledge_subnet))

    def test_received_all_necessary_nodes_if_received_knowledge_subnet_is_none(self):
        casimir_simulation = CasimirSimulation(app)
        objects_to_receive = ["Paris", "London"]   
        knowledge_subnet = None

        self.assertFalse(casimir_simulation._received_all_necessary_nodes(objects_to_receive, knowledge_subnet))
    
    def test_create_mental_image_without_recall(self):
        casimir_simulation = CasimirSimulation(app)
        casimir_simulation.MAX_AMOUNT_OF_RETRIES = 0
        paris_city_object = CityObject("Paris")
        prague_city_object = CityObject("Prague")
        london_city_object = CityObject("London")
        south_cardinal_relation = SouthCardinalRelation()
        east_cardinal_relation = EastCardinalRelation()
        casimir_simulation.save_knowledge_fragment(south_cardinal_relation, [paris_city_object, london_city_object])
        casimir_simulation.save_knowledge_fragment(east_cardinal_relation, [prague_city_object, paris_city_object])
        casimir_simulation.update_settings(-0.5, 0.6, 1, 0.1, True, 0.1, False, False, False, 0)
        
        created_spatial_mental_image = casimir_simulation.create_mental_image([RelationType.CardinalRelation, prague_city_object, london_city_object])

        self.assertEqual(created_spatial_mental_image['smm'][0]['south'], 'Paris')
        self.assertEqual(created_spatial_mental_image['smm'][0]['middle'], 'London')
        self.assertEqual(created_spatial_mental_image['smm'][1]['east'], 'Prague')
        self.assertEqual(created_spatial_mental_image['smm'][1]['middle'], 'Paris')

    def test_create_mental_image_with_only_one_relation(self):
        casimir_simulation = CasimirSimulation(app)
        casimir_simulation.MAX_AMOUNT_OF_RETRIES = 0
        paris_city_object = CityObject("Paris")
        london_city_object = CityObject("London")
        south_cardinal_relation = SouthCardinalRelation()
        casimir_simulation.save_knowledge_fragment(south_cardinal_relation, [paris_city_object, london_city_object])
        casimir_simulation.update_settings(-0.5, 0.6, 1, 0.1, True, 0.1, False, False, False, 0)
        
        created_spatial_mental_image = casimir_simulation.create_mental_image([RelationType.CardinalRelation, paris_city_object, london_city_object])
       
        self.assertEqual(created_spatial_mental_image['smm'][0]['middle'], None)

    def test_create_mental_image_with_only_one_relation_receive_just_complete_fragments(self):
        casimir_simulation = CasimirSimulation(app)
        casimir_simulation.MAX_AMOUNT_OF_RETRIES = 0
        paris_city_object = CityObject("Paris")
        london_city_object = CityObject("London")
        south_cardinal_relation = SouthCardinalRelation()
        casimir_simulation.save_knowledge_fragment(south_cardinal_relation, [paris_city_object, london_city_object])
        casimir_simulation.update_settings(-0.5, 0.6, 1, 0.1, True, 0.1, False, False, True, 0)
        
        created_spatial_mental_image = casimir_simulation.create_mental_image([RelationType.CardinalRelation, paris_city_object, london_city_object])
        
        self.assertEqual(len(created_spatial_mental_image['smm']), 0)

    def test_create_mental_image_for_spatial_relations(self):
        casimir_simulation = CasimirSimulation(app)
        a_object = MiscellaneousObject("A")
        b_object = MiscellaneousObject("B")
        c_object = MiscellaneousObject("C")
        left_spatial_relation = LeftSpatialRelation()
        right_spatial_relation = RightSpatialRelation()
        casimir_simulation.save_knowledge_fragment(left_spatial_relation, [a_object, b_object])
        casimir_simulation.save_knowledge_fragment(right_spatial_relation, [c_object, b_object])
        casimir_simulation.update_settings(-0.5, 0.6, 1, 0.1, True, 0.1, False, False, False, 3)
        
        created_spatial_mental_image = casimir_simulation.create_mental_image([RelationType.SpatialRelation, a_object, c_object])

        self.assertEqual(created_spatial_mental_image['smm'][0]['right'], 'C')
        self.assertEqual(created_spatial_mental_image['smm'][0]['middle'], 'B')
        self.assertEqual(created_spatial_mental_image['smm'][0]['left'], 'A')