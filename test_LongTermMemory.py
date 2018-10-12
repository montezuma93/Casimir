import unittest
from LongTermMemory import LongTermMemory, KnowledgeSubnet
from Relation import EastCardinalRelation, NorthCardinalRelation, SouthCardinalRelation, PartOfTopologicalRelation, CardinalRelation, RelationCategory, CardinalRelationName, RelationType, TopologicalRelationName
from Object import CityObject, CountryObject

class TestLongTermMemory(unittest.TestCase):
    
    def test_long_term_memory_can_save_one_relation_correctly(self):
        long_term_memory = LongTermMemory()
        paris_city_object = CityObject("Paris")
        london_city_object = CityObject("London")
        north_cardinal_relation = NorthCardinalRelation()

        long_term_memory.save_knowledge_fragment(north_cardinal_relation, [london_city_object, paris_city_object])

        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].relation.relation_type, RelationType.CardinalRelation)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].relation.name, CardinalRelationName.North)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].objects[0], "London")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].objects[1], "Paris")

    def test_long_term_memory_can_save_multiple_relation_correctly(self):
        long_term_memory = LongTermMemory()
        paris_city_object = CityObject("Paris")
        london_city_object = CityObject("London")
        north_cardinal_relation = NorthCardinalRelation()
        kairo_city_object = CityObject("Kairo")
        south_cardinal_relation = SouthCardinalRelation()

        long_term_memory.save_knowledge_fragment(north_cardinal_relation, [london_city_object, paris_city_object])
        long_term_memory.save_knowledge_fragment(south_cardinal_relation, [kairo_city_object, paris_city_object])

        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].relation.name, CardinalRelationName.North)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].objects[0], "London")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].objects[1], "Paris")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].relation.name, CardinalRelationName.South)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].objects[0], "Kairo")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].objects[1], "Paris")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].time_of_creation, 2)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].amount_of_usages, 1)
        self.assertEqual(long_term_memory.stored_objects["Paris"].time_of_creation, 1)
        self.assertEqual(long_term_memory.stored_objects["Paris"].amount_of_usages, 2)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[0], (RelationType.CardinalRelation, 0))
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[1], (RelationType.CardinalRelation, 1))


    def test_long_term_memory_can_save_multiple_relation_categories_correctly(self):
        long_term_memory = LongTermMemory()
        paris_city_object = CityObject("Paris")
        london_city_object = CityObject("London")
        north_cardinal_relation = NorthCardinalRelation()      
        france_country_object = CountryObject("France")
        part_of_topological_relation = PartOfTopologicalRelation()
        kairo_city_object = CityObject("Kairo")
        south_cardinal_relation = SouthCardinalRelation()

        long_term_memory.save_knowledge_fragment(north_cardinal_relation, [london_city_object, paris_city_object])
        long_term_memory.save_knowledge_fragment(part_of_topological_relation, [paris_city_object, france_country_object])
        long_term_memory.save_knowledge_fragment(south_cardinal_relation, [kairo_city_object, paris_city_object])

        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].objects[0], "London")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].objects[1], "Paris")
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].time_of_creation, 1)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].amount_of_usages, 1)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].time_of_creation, 2)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].amount_of_usages, 1)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[0][0], RelationType.CardinalRelation)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[0][1], 0)
        self.assertEqual(long_term_memory.stored_objects["Paris"].stored_object, paris_city_object)
        self.assertEqual(long_term_memory.stored_objects["Paris"].time_of_creation, 1)
        self.assertEqual(long_term_memory.stored_objects["Paris"].amount_of_usages, 3)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[1][0], RelationType.TopologicalRelation)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[1][1], 0)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[2][0], RelationType.CardinalRelation)
        self.assertEqual(long_term_memory.stored_objects["Paris"].relation_links[2][1], 1)
        self.assertEqual(long_term_memory.stored_objects["France"].stored_object, france_country_object)


        
    def test_save_and_spread_activation_based_on_papers_example_without_dynamic_firing_threshold(self):
        
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory.DYNAMIC_FIRING_THRESHOLD = False
        retrieved_fragments = long_term_memory.receive_knowledge_fragments([RelationType.CardinalRelation, long_term_memory.paris_city_object, long_term_memory.london_city_object])
        '''
        self.assertEqual(long_term_memory.stored_objects["France"].activation, 0.061599999999999995)
        self.assertEqual(long_term_memory.stored_objects["England"].activation, 0.05999999999999999)
        self.assertEqual(long_term_memory.stored_objects["Prague"].activation, 0.06999999999999999)
        self.assertEqual(long_term_memory.stored_objects["London"].activation, 0.4033333333333333)
        self.assertEqual(long_term_memory.stored_objects["Paris"].activation, 0.4533333333333333)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][0].activation, 0.12066666666666664)
        self.assertEqual(long_term_memory.stored_relations[RelationType.TopologicalRelation][1].activation, 0.142)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][0].activation, 0.18466666666666665)
        self.assertEqual(long_term_memory.stored_relations[RelationType.CardinalRelation][1].activation, 0.26666666666666666)
        
        '''

        self.assertEqual(len(retrieved_fragments.objects), 3)
        self.assertEqual(len(retrieved_fragments.relations[RelationType.CardinalRelation]), 2)

        self.assertFalse(retrieved_fragments.relations.__contains__(RelationType.TopologicalRelation))
        self.assertFalse(retrieved_fragments.objects.__contains__(long_term_memory.france_country_object))
        self.assertFalse(retrieved_fragments.objects.__contains__(long_term_memory.england_country_object))

        self.assertEqual(retrieved_fragments.relations[RelationType.CardinalRelation][0].relation, long_term_memory.south_cardinal_relation)
        self.assertEqual(retrieved_fragments.relations[RelationType.CardinalRelation][1].relation, long_term_memory.east_cardinal_relation)
        self.assertEqual(retrieved_fragments.objects["Paris"].stored_object, long_term_memory.paris_city_object)
        self.assertEqual(retrieved_fragments.objects["London"].stored_object, long_term_memory.london_city_object)
        self.assertEqual(retrieved_fragments.objects["Prague"].stored_object, long_term_memory.prague_city_object)
        

    
    def test_save_and_spread_activation_based_on_papers_example_with_dynamic_firing_threshold(self):
        
        long_term_memory = self.create_long_term_memory_based_on_papers_example()
        long_term_memory.DYNAMIC_FIRING_THRESHOLD = True

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