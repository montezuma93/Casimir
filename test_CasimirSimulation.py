import unittest
from collections import OrderedDict
from CasimirSimulation import CasimirSimulation
from flask import Flask, request, json, jsonify
from flask_restplus import Resource, Api, reqparse, Swagger,fields
from flask.views import View
from mock import call, patch

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

        casimir_simulation.update_settings(1, 2, 3, 4,True, 5, False, True, False)
        
        mock_ltm_controller_update_settings.assert_has_calls([call(1, 2, 3, 4, True, 5, False, True)])
        mock_wm_controller_update_settings.assert_has_calls([call(False)])
    
    @patch('WorkingMemoryService.WorkingMemoryService.update_settings')
    @patch('LongTermMemoryService.LongTermMemoryService.update_settings')
    def test_update_setting_call_the_correct_methods_in_services(self, mock_ltm_service_update_settings, mock_wm_service_update_settings):
        casimir_simulation = CasimirSimulation(app)

        casimir_simulation.update_settings(1, 2, 3, 4,True, 5, False, True, False)

        mock_ltm_service_update_settings.assert_has_calls([call(1, 2, 3, 4, True, 5, False, True)])
        mock_wm_service_update_settings.assert_has_calls([call(False)])

    def test_reset_simulation(self):
        casimir_simulation = CasimirSimulation(app)
        casimir_simulation.long_term_memory_controller.long_term_memory_service.stored_objects["A"] = "Filled"
        casimir_simulation.working_memory_controller.working_memory_service.stored_spatial_mental_models.append("SMM")

        casimir_simulation.reset_simulation()

        self.assertFalse(casimir_simulation.long_term_memory_controller.long_term_memory_service.stored_objects.__contains__("A"))
        self.assertFalse(casimir_simulation.working_memory_controller.working_memory_service.stored_spatial_mental_models.__contains__("SMM"))