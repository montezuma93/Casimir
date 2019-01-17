import unittest
from unittest import mock
from mock import call, patch
from LongTermMemoryService import LongTermMemoryService, KnowledgeSubnet
from Relation import (EastCardinalRelation, NorthCardinalRelation, SouthCardinalRelation,
 PartOfTopologicalRelation, CardinalRelation, RelationCategory, CardinalRelationName,
 NorthEastCardinalRelation, SouthWestCardinalRelation, RelationType, TopologicalRelationName,
 SouthEastCardinalRelation, NorthWestCardinalRelation, LeftSpatialRelation, RightSpatialRelation)
from Object import CityObject, CountryObject
from WorkingMemoryService import WorkingMemoryService, SpatialMentalModel
from LongTermMemoryService import StoredRelation

class TestLongTermMemoryService(unittest.TestCase):
    
    @patch('WorkingMemoryService.WorkingMemoryService.create_smm_json')
    @patch('WorkingMemoryService.WorkingMemoryService.add_relation_and_opposite_to_smm')
    @patch('WorkingMemoryService.WorkingMemoryService._relation_is_complete')
    def test_construction_in_working_memory_call_the_correct_methods_if_incomplete_fragments_allowed(self, mock_relation_is_complete,
     mock_add_relation_and_opposite_to_smm, mock_create_smm_json):
        working_memory = WorkingMemoryService()
        working_memory.USE_ONLY_COMPLETE_FRAGMENTS = False
        relation = StoredRelation(SouthCardinalRelation(), ["Paris", "London"], 1)
        knowledge_subnet = KnowledgeSubnet(relation)
        working_memory.construction(knowledge_subnet)

        self.assertEqual(mock_relation_is_complete.call_count, 0)
        mock_add_relation_and_opposite_to_smm.assert_has_calls([call(relation)])
        self.assertEqual(mock_create_smm_json.call_count, 1)
    
    @patch('WorkingMemoryService.WorkingMemoryService.create_smm_json')
    @patch('WorkingMemoryService.WorkingMemoryService.add_relation_and_opposite_to_smm')
    @patch('WorkingMemoryService.WorkingMemoryService._relation_is_complete')
    def test_construction_in_working_memory_call_the_correct_methods_if_incomplete_fragments_not_allowed(self, mock_relation_is_complete,
     mock_add_relation_and_opposite_to_smm, mock_create_smm_json):
        working_memory = WorkingMemoryService()
        working_memory.USE_ONLY_COMPLETE_FRAGMENTS = True
        relation = StoredRelation(SouthCardinalRelation(), ["Paris", "London"], 1)
        knowledge_subnet = KnowledgeSubnet(relation)
        working_memory.construction(knowledge_subnet)

        self.assertEqual(mock_relation_is_complete.call_count, 1)
        mock_add_relation_and_opposite_to_smm.assert_has_calls([call(relation)])
        self.assertEqual(mock_create_smm_json.call_count, 1)

    def test_relation_is_complete_works_correctly_for_complete_knowledge_subnet(self):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(SouthCardinalRelation(), ["Paris", "London"], 1)
        self.assertEquals(working_memory._relation_is_complete(relation), True)

    def test_relation_is_complete_works_correctly_for_incomplete_knowledge_subnet(self):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(SouthCardinalRelation(), ["Paris", "London"], 1)
        relation.objects_received[0] = False
        self.assertEquals(working_memory._relation_is_complete(relation), False)

    
    @patch('WorkingMemoryService.WorkingMemoryService.use_relation_for_smm')
    @patch('WorkingMemoryService.WorkingMemoryService.create_opposite')
    def test_add_knowledge_fragment_to_smm_call_the_correct_methods_for_complete_relation(self, mock_create_opposite, mock_use_relation_for_smm):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(SouthCardinalRelation(), ["Paris", "London"], 1)

        working_memory.add_relation_and_opposite_to_smm(relation)

        self.assertEqual(mock_create_opposite.call_count, 1)
        self.assertEqual(mock_use_relation_for_smm.call_count, 2)
    
    @patch('WorkingMemoryService.WorkingMemoryService.use_relation_for_smm')
    @patch('WorkingMemoryService.WorkingMemoryService.create_opposite')
    def test_add_knowledge_fragment_to_smm_call_the_correct_methods_for_topological_relation(self, mock_create_opposite, mock_use_relation_for_smm):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(PartOfTopologicalRelation(), ["Paris", "France"], 1)
        mock_create_opposite.return_value = None
        working_memory.add_relation_and_opposite_to_smm(relation)

        self.assertEqual(mock_create_opposite.call_count, 1)
        self.assertEqual(mock_use_relation_for_smm.call_count, 1)

    
    @patch('WorkingMemoryService.WorkingMemoryService.use_relation_for_smm')
    @patch('WorkingMemoryService.WorkingMemoryService.create_opposite')
    def test_add_knowledge_fragment_to_smm_call_the_correct_methods_for_incomplete_relation(self, mock_create_opposite, mock_use_relation_for_smm):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(SouthCardinalRelation(), ["Freiburg", "Hamburg"], 1)
        relation.objects_received[1] = False

        working_memory.add_relation_and_opposite_to_smm(relation)

        self.assertEqual(mock_create_opposite.call_count, 1)
        self.assertEqual(mock_use_relation_for_smm.call_count, 2)
    
    def test_create_opposite_for_topological_relation(self):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(PartOfTopologicalRelation(), ["Freiburg", "Germany"], 1)

        opposite_relation = working_memory.create_opposite(relation)

        self.assertIsNone(opposite_relation)

    def test_create_opposite_for_complete_cardinal_relation(self):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(SouthCardinalRelation(), ["Freiburg", "Hamburg"], 1)

        opposite_relation = working_memory.create_opposite(relation)

        self.assertEquals(opposite_relation.relation.name.value, "North")
        self.assertEquals(opposite_relation.objects[0], "Hamburg")
        self.assertEquals(opposite_relation.objects[1], "Freiburg")
        self.assertEquals(opposite_relation.objects_received[0], True)
        self.assertEquals(opposite_relation.objects_received[1], True)

    def test_add_multiple_relations_to_smm(self):
        working_memory = WorkingMemoryService()
        relation1 = StoredRelation(SouthEastCardinalRelation(), ["Munich", "Cologne"], 1)
        relation2 = StoredRelation(NorthEastCardinalRelation(), ["Berlin", "Cologne"], 1)
        relation3 = StoredRelation(SouthWestCardinalRelation(), ["Freiburg", "Berlin"], 1)
        relation4 = StoredRelation(SouthWestCardinalRelation(), ["Basel", "Freiburg"], 1)

        working_memory.add_relation_and_opposite_to_smm(relation1)
        working_memory.add_relation_and_opposite_to_smm(relation2)
        working_memory.add_relation_and_opposite_to_smm(relation3)
        working_memory.add_relation_and_opposite_to_smm(relation4)

        stored_spatial_mental_models = working_memory.stored_spatial_mental_models
        self.assertEquals(stored_spatial_mental_models[0].middle, "Cologne")
        self.assertEquals(stored_spatial_mental_models[0].south_east, "Munich")
        self.assertEquals(stored_spatial_mental_models[0].north_east, "Berlin")
        self.assertEquals(stored_spatial_mental_models[1].middle, "Munich")
        self.assertEquals(stored_spatial_mental_models[2].outer_south_west, "Freiburg")
        self.assertEquals(stored_spatial_mental_models[3].south_west, "Basel")

    def test_create_opposite_for_incomplete_cardinal_relation_and_first_object_not_received(self):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(SouthCardinalRelation(), ["Freiburg", "Hamburg"], 1)
        relation.objects_received[0] = False

        opposite_relation = working_memory.create_opposite(relation)

        self.assertEquals(opposite_relation.relation.name.value, "North")
        self.assertEquals(opposite_relation.objects[0], "Hamburg")
        self.assertEquals(opposite_relation.objects[1], "Freiburg")
        self.assertEquals(opposite_relation.objects_received[0], True)
        self.assertEquals(opposite_relation.objects_received[1], False)

    def test_create_opposite_for_incomplete_cardinal_relation_and_second_object_not_received(self):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(NorthEastCardinalRelation(), ["Berlin", "Freiburg"], 1)
        relation.objects_received[1] = False

        opposite_relation = working_memory.create_opposite(relation)

        self.assertEquals(opposite_relation.relation.name.value, "SouthWest")
        self.assertEquals(opposite_relation.objects[0], "Freiburg")
        self.assertEquals(opposite_relation.objects[1], "Berlin")
        self.assertEquals(opposite_relation.objects_received[0], False)
        self.assertEquals(opposite_relation.objects_received[1], True)

    def test_create_opposite_for_inter_cardinal_direction(self):
        working_memory = WorkingMemoryService()
        relation1 = StoredRelation(SouthWestCardinalRelation(), ["Berlin", "Freiburg"], 1)
        relation2 = StoredRelation(NorthWestCardinalRelation(), ["Berlin", "Freiburg"], 1)
        relation3 = StoredRelation(SouthEastCardinalRelation(), ["Berlin", "Freiburg"], 1)

        opposite_relation1 = working_memory.create_opposite(relation1)
        opposite_relation2 = working_memory.create_opposite(relation2)
        opposite_relation3 = working_memory.create_opposite(relation3)

        self.assertEquals(opposite_relation1.relation.name.value, "NorthEast")
        self.assertEquals(opposite_relation1.objects[0], "Freiburg")
        self.assertEquals(opposite_relation1.objects[1], "Berlin")
        
        self.assertEquals(opposite_relation2.relation.name.value, "SouthEast")
        self.assertEquals(opposite_relation2.objects[0], "Freiburg")
        self.assertEquals(opposite_relation2.objects[1], "Berlin")

        self.assertEquals(opposite_relation3.relation.name.value, "NorthWest")
        self.assertEquals(opposite_relation3.objects[0], "Freiburg")
        self.assertEquals(opposite_relation3.objects[1], "Berlin")

    def test_create_smm_for_complete_cardinal_relation(self):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(NorthCardinalRelation(), ["Hamburg", "Freiburg"], 1)

        working_memory.create_new_smm(relation)
        actual_smm_list = working_memory.stored_spatial_mental_models

        self.assertEquals(len(actual_smm_list), 1)
        self.assertEqual(actual_smm_list[0].north, "Hamburg")
        self.assertEqual(actual_smm_list[0].middle, "Freiburg")
        self.assertEqual(actual_smm_list[0].south, None)

    def test_create_smm_for_complete_intercardinal_relation(self):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(SouthWestCardinalRelation(), ["Freiburg", "Prague"], 1)

        working_memory.create_new_smm(relation)
        actual_smm_list = working_memory.stored_spatial_mental_models

        self.assertEquals(len(actual_smm_list), 1)
        self.assertEqual(actual_smm_list[0].south_west, "Freiburg")
        self.assertEqual(actual_smm_list[0].middle, "Prague")
        self.assertEqual(actual_smm_list[0].south, None)

    def test_create_smm_for_incomplete_relation_first_object(self):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(NorthEastCardinalRelation(), ["Freiburg", "Prague"], 1)
        relation.objects_received[0] = False

        working_memory.create_new_smm(relation)
        actual_smm_list = working_memory.stored_spatial_mental_models

        self.assertEquals(len(actual_smm_list), 1)
        self.assertEqual(actual_smm_list[0].south_west, None)
        self.assertEqual(actual_smm_list[0].middle, "Prague")
        self.assertEqual(actual_smm_list[0].south, None)

    def test_create_smm_for_incomplete_relation_second_object(self):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(NorthEastCardinalRelation(), ["Freiburg", "Prague"], 1)
        relation.objects_received[1] = False

        working_memory.create_new_smm(relation)
        actual_smm_list = working_memory.stored_spatial_mental_models

        self.assertEquals(len(actual_smm_list), 1)
        self.assertEqual(actual_smm_list[0].north_east, "Freiburg")
        self.assertEqual(actual_smm_list[0].middle, None)
        self.assertEqual(actual_smm_list[0].south, None)

    def test_use_relation_for_smm_if_suitable_smm_exists_in_wm_and_relation_is_complete(self):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(NorthCardinalRelation(), ["London", "Paris"], 1)

        smm1 = SpatialMentalModel()
        smm1.east = "Berlin"
        smm1.middle = "Paris"
        smm2 = SpatialMentalModel()
        smm2.south = "Freiburg"
        smm2.middle = "Hamburg"
        working_memory.stored_spatial_mental_models = [smm1, smm2]
        working_memory.use_relation_for_smm(relation)
        actual_smm_list = working_memory.stored_spatial_mental_models

        self.assertEquals(len(actual_smm_list), 2)
        self.assertEqual(actual_smm_list[0].east, "Berlin")
        self.assertEqual(actual_smm_list[0].middle, "Paris")
        self.assertEqual(actual_smm_list[0].north, "London")
        self.assertEqual(actual_smm_list[1].north, None)
        self.assertEqual(actual_smm_list[1].middle, "Hamburg")
        self.assertEqual(actual_smm_list[1].south, "Freiburg")
    
    def test_multiple_use_relation_for_smm_if_suitable_smm_exists_in_wm_and_relation_is_complete(self):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(NorthCardinalRelation(), ["London", "Paris"], 1)
        relation2 = StoredRelation(SouthWestCardinalRelation(), ["Madrid", "Paris"], 1)


        smm = SpatialMentalModel()
        smm.east = "Berlin"
        smm.middle = "Paris"
        working_memory.stored_spatial_mental_models = [smm]
        working_memory.use_relation_for_smm(relation)
        working_memory.use_relation_for_smm(relation2)
        actual_smm_list = working_memory.stored_spatial_mental_models

        self.assertEquals(len(actual_smm_list), 1)
        self.assertEqual(actual_smm_list[0].east, "Berlin")
        self.assertEqual(actual_smm_list[0].south_west, "Madrid")
        self.assertEqual(actual_smm_list[0].middle, "Paris")
        self.assertEqual(actual_smm_list[0].north, "London")
        
    def test_use_relation_for_smm_if_suitable_smm_exists_in_wm_and_relation_is_incomplete_for_second_object(self):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(NorthCardinalRelation(), ["London", "Paris"], 1)
        relation.objects_received[1] = False

        smm1 = SpatialMentalModel()
        smm1.east = "Berlin"
        smm1.middle = "Paris"
        smm2 = SpatialMentalModel()
        smm2.south = "Freiburg"
        smm2.middle = "Paris"
        working_memory.stored_spatial_mental_models = [smm1, smm2]
        working_memory.use_relation_for_smm(relation)
        actual_smm_list = working_memory.stored_spatial_mental_models

        self.assertEquals(len(actual_smm_list), 3)
        self.assertEqual(actual_smm_list[0].east, "Berlin")
        self.assertEqual(actual_smm_list[0].middle, "Paris")
        self.assertEqual(actual_smm_list[0].north, None)
        self.assertEqual(actual_smm_list[1].north, None)
        self.assertEqual(actual_smm_list[1].middle, "Paris")
        self.assertEqual(actual_smm_list[1].south, "Freiburg")
        self.assertEqual(actual_smm_list[2].north, "London")
        self.assertEqual(actual_smm_list[2].middle, None)
        self.assertEqual(actual_smm_list[2].south, None)

    def test_use_relation_for_smm_if_suitable_smm_exists_in_wm_and_relation_is_incomplete_for_first_object(self):
        working_memory = WorkingMemoryService()
        relation = StoredRelation(NorthCardinalRelation(), ["London", "Paris"], 1)
        relation.objects_received[0] = False

        smm1 = SpatialMentalModel()
        smm1.east = "Berlin"
        smm1.middle = "Paris"
        smm2 = SpatialMentalModel()
        smm2.south = "Freiburg"
        smm2.middle = "Paris"
        working_memory.stored_spatial_mental_models = [smm1, smm2]
        working_memory.use_relation_for_smm(relation)
        actual_smm_list = working_memory.stored_spatial_mental_models

        self.assertEquals(len(actual_smm_list), 3)
        self.assertEqual(actual_smm_list[0].east, "Berlin")
        self.assertEqual(actual_smm_list[0].middle, "Paris")
        self.assertEqual(actual_smm_list[0].north, None)
        self.assertEqual(actual_smm_list[1].north, None)
        self.assertEqual(actual_smm_list[1].middle, "Paris")
        self.assertEqual(actual_smm_list[1].south, "Freiburg")
        self.assertEqual(actual_smm_list[2].north, None)
        self.assertEqual(actual_smm_list[2].middle, "Paris")
        self.assertEqual(actual_smm_list[2].south, None)

    def test_add_main_cardinal_to_smm(self):
        working_memory = WorkingMemoryService()
        spatial_mental_model = SpatialMentalModel()
        spatial_mental_model.middle = "A"
        spatial_mental_model.north = "B"
        relation = StoredRelation(SouthCardinalRelation, [CityObject("C"), CityObject("A")], 0)
        working_memory.add_to_smm(spatial_mental_model, relation)
        self.assertEquals(spatial_mental_model.south.name, "C")

    def test_add_inter_cardinal_to_smm(self):
        working_memory = WorkingMemoryService()
        spatial_mental_model = SpatialMentalModel()
        spatial_mental_model.middle = "A"
        spatial_mental_model.north_east = "B"
        relation = StoredRelation(NorthWestCardinalRelation, [CityObject("C"), CityObject("A")], 0)
        working_memory.add_to_smm(spatial_mental_model, relation)
        self.assertEquals(spatial_mental_model.north_west.name, "C")
