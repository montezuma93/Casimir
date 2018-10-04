import unittest
from collections import OrderedDict
from CasimirSimulation import CasimirSimulation

class TestCasimirSimulation(unittest.TestCase):

    def test_casimir_simulation_is_initialized_correctly(self):
        casimir_simulation = CasimirSimulation()
        self.assertEqual(casimir_simulation.long_term_memory.stored_objects, OrderedDict())
        self.assertEqual(casimir_simulation.long_term_memory.stored_relations, OrderedDict())