import unittest
from Object import ConcreteObject

class TestRelation(unittest.TestCase):

    def test_relation_category_is_initialized_correctly(self):
        concrete_object = ConcreteObject("cardinal_direction", "north")
        self.assertEqual(concrete_object.category_name, 'cardinal_direction')
        self.assertEqual(concrete_object.name, 'north')
