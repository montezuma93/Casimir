import unittest
from Relation import CardinalRelation, NorthCardinalRelation, TopologicalRelation, PartOfTopologicalRelation

class TestRelation(unittest.TestCase):

    def test_cardinal_relation_is_initialized_correctly(self):
        cardinal_relation = CardinalRelation()
        self.assertEqual(cardinal_relation.category_name, "CardinalRelation")
        self.assertEqual(cardinal_relation.amount_of_objects, 2)

    def test_north_cardinal_relation_is_initialized_correctly(self):
        north_relation = NorthCardinalRelation()
        self.assertEqual(north_relation.name, "North")
        self.assertEqual(north_relation.category_name, "CardinalRelation")
        self.assertEqual(north_relation.amount_of_objects, 2)

    def test_topological_relation_is_initialized_correctly(self):
        tolopological_relation = TopologicalRelation()
        self.assertEqual(tolopological_relation.category_name, "TopologicalRelation")
        self.assertEqual(tolopological_relation.amount_of_objects, 2)
    
    def test_part_of_topological_relation_is_initialized_correctly(self):
        part_of_relation = PartOfTopologicalRelation()
        self.assertEqual(part_of_relation.name, "PartOf")
        self.assertEqual(part_of_relation.category_name, "TopologicalRelation")
        self.assertEqual(part_of_relation.amount_of_objects, 2)