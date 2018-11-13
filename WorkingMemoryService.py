import json
import copy
from Relation import CardinalRelationName

class WorkingMemoryService:

    RECEIVE_ONLINE_COMPLETE_FRAGMENTS = True
 
    def __init__(self):
        self.stored_smm = []
        pass

    def create_smm(self, knowledge_subnet):
        relation_list = []
        if knowledge_subnet:
            knowledge_subnet = self.add_opposite_knowledge(knowledge_subnet)
            for stored_relations in knowledge_subnet.relations.values():
                for stored_relation in stored_relations:
                    print(stored_relation.relation.name.value)
                    if(stored_relation.relation.name.value == "North"):
                        relation_for_list = {"innerNorth": stored_relation.objects[0], "middle": stored_relation.objects[1] }
                        relation_list.append(relation_for_list)  
                    elif(stored_relation.relation.name.value == "South"):
                        relation_for_list = {"innerSouth": stored_relation.objects[0], "middle": stored_relation.objects[1] }
                        relation_list.append(relation_for_list)  
                    elif(stored_relation.relation.name.value == "West"):
                        relation_for_list = {"innerWest": stored_relation.objects[0], "middle": stored_relation.objects[1] }
                        relation_list.append(relation_for_list)  
                    elif(stored_relation.relation.name.value == "East"):
                        relation_for_list = {"innerEast": stored_relation.objects[0], "middle": stored_relation.objects[1] }
                        relation_list.append(relation_for_list) 
                    elif(stored_relation.relation.name.value == "PartOf"):
                        relation_for_list = {"innerPart": stored_relation.objects[0], "outerPart": stored_relation.objects[1] }
                        relation_list.append(relation_for_list)
        return{
            "smm": relation_list
        }
    
    def add_opposite_knowledge(self, knowledge_subnet):
        new_knowledge_subnet = copy.deepcopy(knowledge_subnet)
        if knowledge_subnet:
            for relation_type, stored_relations in knowledge_subnet.relations.items():
                for stored_relation in stored_relations:
                    if not stored_relation.relation.name.value == "PartOf":
                        opposite_relation = copy.deepcopy(stored_relation)
                        opposite_relation.objects[0] = stored_relation.objects[1]
                        opposite_relation.objects[1] = stored_relation.objects[0]
                        if(stored_relation.relation.name.value == "North"):
                            opposite_relation.relation.name = CardinalRelationName.South
                        elif(stored_relation.relation.name.value == "South"):
                            opposite_relation.relation.name = CardinalRelationName.North
                        elif(stored_relation.relation.name.value == "West"):
                            opposite_relation.relation.name = CardinalRelationName.East
                        elif(stored_relation.relation.name.value == "East"):
                            opposite_relation.relation.name = CardinalRelationName.West
                        new_knowledge_subnet.relations[relation_type].append(opposite_relation)
            return new_knowledge_subnet
