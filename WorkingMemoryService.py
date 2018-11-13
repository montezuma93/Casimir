import json
import copy
from Relation import CardinalRelationName

class WorkingMemoryService:

    RECEIVE_ONLINE_COMPLETE_FRAGMENTS = True
    def __init__(self):
        self.stored_smm = []
        pass

    def create_smm_json(self):
        print("create json")
        relation_list = []
        print(len(self.stored_smm))

        for smm in self.stored_smm:
            print(smm.inner_west)
            relation_for_list = {"innerNorth": smm.inner_north, "innerSouth": smm.inner_south, "innerWest": smm.inner_west, "innerEast": smm.inner_east, 
            "outerNorth": smm.outer_north, "outerSouth": smm.outer_south, "outerWest": smm.outer_west, "outerEast": smm.outer_east,
            "middle": smm.middle, "innerPart": smm.inner_part, "outerPart": smm.outer_part }
            print(relation_for_list['innerWest'])
            relation_list.append(relation_for_list)
        return{
            "smm": relation_list
        }
    
    def add_opposite_knowledge(self, knowledge_subnet):
        new_knowledge_subnet = copy.deepcopy(knowledge_subnet)
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

    def create_opposite(self, relation):
        if not relation.relation.name.value == "PartOf":
            opposite_relation = copy.deepcopy(relation)
            opposite_relation.objects[0] = relation.objects[1]
            opposite_relation.objects[1] = relation.objects[0]
            if(relation.relation.name.value == "North"):
                opposite_relation.relation.name = CardinalRelationName.South
            elif(relation.relation.name.value == "South"):
                opposite_relation.relation.name = CardinalRelationName.North
            elif(relation.relation.name.value == "West"):
                opposite_relation.relation.name = CardinalRelationName.East
            elif(relation.relation.name.value == "East"):
                opposite_relation.relation.name = CardinalRelationName.West
            return opposite_relation
        else:
            return None


    # TODO: Sort
    def construction(self, knowledge_subnet):
        print("construction")
        if knowledge_subnet:
            #knowledge_subnet = self.add_opposite_knowledge(knowledge_subnet)
            for relations in knowledge_subnet.relations.values():
                for relation in relations:
                    self.create_smm(relation)
                    opposite_smm = self.create_opposite(relation)
                    if opposite_smm:
                        self.create_smm(opposite_smm)
        return self.create_smm_json()

    def create_smm(self, relation):
        print("create_smm")
        for smm in self.stored_smm:
            if smm.middle == relation.objects[1] and not relation.relation.name.value == "PartOf":
                self.add_to_stored_smm(smm, relation)
                return
        self.add_new_smm(relation)

    def add_new_smm(self, relation):
        print("addnew")
        print(relation.objects[0])
        print(relation.objects[1])
        smm_to_add = SMM()
        if(relation.relation.name.value == "North"):
            smm_to_add.inner_north = relation.objects[0]
            smm_to_add.middle = relation.objects[1]
        elif(relation.relation.name.value == "South"):
            smm_to_add.inner_south = relation.objects[0]
            smm_to_add.middle = relation.objects[1]
        elif(relation.relation.name.value == "West"):
            smm_to_add.inner_west = relation.objects[0]
            smm_to_add.middle = relation.objects[1]
        elif(relation.relation.name.value == "East"):
            smm_to_add.inner_east = relation.objects[0]
            smm_to_add.middle = relation.objects[1]
        self.stored_smm.append(smm_to_add)

    def add_to_stored_smm(self, smm, relation):
        updated_smm = False
        print("add_to_stored")
        if(relation.relation.name.value == "North" and smm.inner_north == ""):
            smm.inner_north = relation.objects[0]
            updated_smm = True
        elif(relation.relation.name.value == "South" and smm.inner_south == ""):
            smm.inner_south = relation.objects[0]
            updated_smm = True
        elif(relation.relation.name.value == "West" and smm.inner_west == ""):
            smm.inner_west = relation.objects[0]
            updated_smm = True
        elif(relation.relation.name.value == "East" and smm.inner_east == ""):
            smm.inner_east = relation.objects[0]
            updated_smm = True
        if(updated_smm == False):
            self.add_new_smm(relation)

class SMM():
    def __init__(self):
        self.inner_north = ""
        self.inner_south = ""
        self.inner_west = ""
        self.inner_east = ""
        self.outer_north = ""
        self.outer_south = ""
        self.outer_west = ""
        self.outer_east = ""
        self.middle = ""
        self.outer_part = ""
        self.inner_part = ""

        