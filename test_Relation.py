import unittest
from Relation import CardinalRelation, NorthCardinalRelation, TopologicalRelation, PartOfTopologicalRelation, RelationType, CardinalRelationName, TopologicalRelationName

class TestRelation(unittest.TestCase):

    def test_north_cardinal_relation_is_initialized_correctly(self):
        north_relation = NorthCardinalRelation()
        self.assertEqual(north_relation.name, CardinalRelationName.North)
        self.assertEqual(north_relation.relation_type, RelationType.CardinalRelation)
        self.assertEqual(north_relation.amount_of_objects, 2)
    
    def test_part_of_topological_relation_is_initialized_correctly(self):
        part_of_relation = PartOfTopologicalRelation()
        self.assertEqual(part_of_relation.name, TopologicalRelationName.PartOf)
        self.assertEqual(part_of_relation.relation_type, RelationType.TopologicalRelation)
        self.assertEqual(part_of_relation.amount_of_objects, 2)