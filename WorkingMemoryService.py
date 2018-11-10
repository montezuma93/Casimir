import json

class WorkingMemoryService:

    RECEIVE_ONLINE_COMPLETE_FRAGMENTS = True
    def __init__(self):
        pass

    def create_smm(self, knowledge_fragment):
        print(knowledge_fragment)
        relation_list = []
        if knowledge_fragment:
            for stored_relations in knowledge_fragment.relations.values():
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
        return{
            "smm": relation_list
        }