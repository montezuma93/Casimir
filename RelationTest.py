import unittest
from Relation import ConcreteRelation

class TestRelation(unittest.TestCase):

    def test_relation_category_is_initialized_correctly(self):
        concrete_relation = ConcreteRelation("cardinal_direction", "north")
        self.assertEqual(concrete_relation.category_name, 'cardinal_direction')
        self.assertEqual(concrete_relation.name, 'north')
