import json
import copy
from Relation import CardinalRelationName
import logging

class WorkingMemoryService:

    USE_ONLY_COMPLETE_FRAGMENTS = False

    def __init__(self):
        self.logger = logging.getLogger('LongTermMemory')
        self.logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        self.logger.addHandler(stream_handler)
        self.stored_smm = []

    """
    Reset all stored smm
    """
    def reset_simulation(self):
        self.stored_smm = []

    """
    Update setting used in LTM calculations

    Parameters
    ----------
    param1 : boolean
        true if just knowledge_fragments should be used, in that all objects were received
    """
    def update_settings(self, use_only_complete_fragments):
        if use_only_complete_fragments != '':
            self.USE_ONLY_COMPLETE_FRAGMENTS = use_only_complete_fragments

    """
    Construct SMM for received knowledge_subnet

    Parameters
    ------------
    param1: KnowledgeSubnet
        knowledgeSubnet, for which a smm gets created

    Returns
    ------------
    JsonObject
        returns a created smm based on the received knowledge_subnet
    """
    def construction(self, knowledge_subnet):
        self.stored_smm = []
        self.logger.info('Construction request')
        if knowledge_subnet:
            for relations in knowledge_subnet.relations.values():
                for relation in relations:
                    if self.USE_ONLY_COMPLETE_FRAGMENTS:
                        if self._relation_is_complete(relation):
                            self.add_relation_and_opposite_to_smm(relation)
                    else:
                        self.add_relation_and_opposite_to_smm(relation)            
        return self.create_smm_json()

    """
    Check if all objects in a relation are received

    Parameters
    ------------
    param1: StoredRelation
        storedRelation, for which gets checked if all objects are received from the LTM

    Returns
    ------------
    Boolean
        returns true if all objects in an relation have the received flag, false otherwise
    """
    def _relation_is_complete(self, relation):
        for object_is_received in relation.objects_received:
            if object_is_received == False:
                return False
        return True 

    """
    Use relation and its opposite to create or update smm 

    Parameters
    ------------
    param1: StoredRelation
        storedRelation, which gets used to create or update smm
    """
    def add_relation_and_opposite_to_smm(self, relation):
        self.use_relation_for_smm(relation)
        opposite_smm = self.create_opposite(relation)
        if opposite_smm is not None:
            self.use_relation_for_smm(opposite_smm)

    """
    Create Opposite of a given relation

    Parameters
    ------------
    param1: StoredRelation
        storedRelation, for which an opposite relation gets created
    
    Returns
    ------------
    StoredRelation
        returns the opposite relation, or None if there is no opposite relation
        i.e. partOf topological relation
    """
    def create_opposite(self, relation):
        if not relation.relation.name.value == "PartOf":
            opposite_relation = copy.deepcopy(relation)
            opposite_relation.objects[0] = relation.objects[1]
            opposite_relation.objects_received[0] = relation.objects_received[1]
            opposite_relation.objects[1] = relation.objects[0]
            opposite_relation.objects_received[1] = relation.objects_received[0]
            if(relation.relation.name.value == "North"):
                opposite_relation.relation.name = CardinalRelationName.South
            elif(relation.relation.name.value == "South"):
                opposite_relation.relation.name = CardinalRelationName.North
            elif(relation.relation.name.value == "West"):
                opposite_relation.relation.name = CardinalRelationName.East
            elif(relation.relation.name.value == "East"):
                opposite_relation.relation.name = CardinalRelationName.West
            elif(relation.relation.name.value == "NorthWest"):
                opposite_relation.relation.name = CardinalRelationName.SouthEast
            elif(relation.relation.name.value == "NorthEast"):
                opposite_relation.relation.name = CardinalRelationName.SouthWest
            elif(relation.relation.name.value == "SouthWest"):
                opposite_relation.relation.name = CardinalRelationName.NorthEast
            elif(relation.relation.name.value == "SouthEast"):
                opposite_relation.relation.name = CardinalRelationName.NorthWest
            return opposite_relation
        else:
            return None
    
    """
    Create Opposite of a given relation

    Parameters
    ------------
    param1: StoredRelation
        storedRelation, for which an opposite relation gets created
    
    Returns
    ------------
    StoredRelation
        returns the opposite relation, or None if there is no opposite relation
        i.e. partOf topological relation
    """
    def use_relation_for_smm(self, relation):
        for smm in self.stored_smm:
            if smm.middle == relation.objects[1] and relation.objects_received[1] == True and not relation.relation.name.value == "PartOf":
                self.add_to_smm(smm, relation)
                return
        self.create_new_smm(relation)

    """
    Create new smm for given relation

    Parameters
    ------------
    param1: StoredRelation
        storedRelation, for which a smm gets created and stored in WM
    """
    def create_new_smm(self, relation):
        import pprint
        pprint.pprint(relation)
        smm_to_add = SMM()
        if(relation.relation.name.value == "North"):
            if(relation.objects_received[0] == True):
                smm_to_add.north = relation.objects[0]
            if(relation.objects_received[1] == True):
                smm_to_add.middle = relation.objects[1]
        elif(relation.relation.name.value == "South"):
            if(relation.objects_received[0] == True):
                smm_to_add.south = relation.objects[0]
            if(relation.objects_received[1] == True):
                smm_to_add.middle = relation.objects[1]
        elif(relation.relation.name.value == "West"):
            if(relation.objects_received[0] == True):
                smm_to_add.west = relation.objects[0]
            if(relation.objects_received[1] == True):
                smm_to_add.middle = relation.objects[1]
        elif(relation.relation.name.value == "East"):
            if(relation.objects_received[0] == True):
                smm_to_add.east = relation.objects[0]
            if(relation.objects_received[1] == True):
                smm_to_add.middle = relation.objects[1]
        elif(relation.relation.name.value == "NorthWest"):
            if(relation.objects_received[0] == True):
                smm_to_add.north_west = relation.objects[0]
            if(relation.objects_received[1] == True):
                smm_to_add.middle = relation.objects[1]
        elif(relation.relation.name.value == "NorthEast"):
            if(relation.objects_received[0] == True):
                smm_to_add.north_east = relation.objects[0]
            if(relation.objects_received[1] == True):
                smm_to_add.middle = relation.objects[1]
        elif(relation.relation.name.value == "SouthWest"):
            if(relation.objects_received[0] == True):
                smm_to_add.south_west = relation.objects[0]
            if(relation.objects_received[1] == True):
                smm_to_add.middle = relation.objects[1]
        elif(relation.relation.name.value == "SouthEast"):
            if(relation.objects_received[0] == True):
                smm_to_add.south_east = relation.objects[0]
            if(relation.objects_received[1] == True):
                smm_to_add.middle = relation.objects[1]
        elif(relation.relation.name.value == "PartOf"):
            if(relation.objects_received[0] == True):
                smm_to_add.inner_part = relation.objects[0]
            if(relation.objects_received[1] == True):
                smm_to_add.outer_part = relation.objects[1]
        self.stored_smm.append(smm_to_add)

    """
    Add given relation to smm if possible otherwise create new

    Parameters
    ------------
    param1: SMM
        smm, to which relation should get added
    param2: StoredRelation
        storedRelation, which should get added to smm
    """
    def add_to_smm(self, smm, relation):
        updated_smm = False
        if(relation.relation.name.value == "North" and smm.north is None):
            if(relation.objects_received[0] == True):
                smm.north = relation.objects[0]
                updated_smm = True
        elif(relation.relation.name.value == "North" and smm.north is not None and smm.outer_north is None):
            if(relation.objects_received[0] == True):
                smm.outer_north = relation.objects[0]
                updated_smm = True
        elif(relation.relation.name.value == "South" and smm.south is None):
            if(relation.objects_received[0] == True):
                smm.south = relation.objects[0]
                updated_smm = True
        elif(relation.relation.name.value == "South" and smm.south is not None and smm.outer_south is None):
            if(relation.objects_received[0] == True):
                smm.outer_south = relation.objects[0]
                updated_smm = True
        elif(relation.relation.name.value == "West" and smm.west is None):
            if(relation.objects_received[0] == True):
                smm.west = relation.objects[0]
                updated_smm = True
        elif(relation.relation.name.value == "West" and smm.west is not None and smm.outer_west is None):
            if(relation.objects_received[0] == True):
                smm.outer_west = relation.objects[0]
                updated_smm = True
        elif(relation.relation.name.value == "East" and smm.east is None):
            if(relation.objects_received[0] == True):
                smm.east = relation.objects[0]
                updated_smm = True
        elif(relation.relation.name.value == "East" and smm.east is not None and smm.outer_east is None):
            if(relation.objects_received[0] == True):
                smm.outer_east = relation.objects[0]
                updated_smm = True
        elif(relation.relation.name.value == "NorthWest" and smm.north_west == None):
            if(relation.objects_received[0] == True):
                smm.north_west = relation.objects[0]
                updated_smm = True
        elif(relation.relation.name.value == "NorthWest" and smm.north_west is not None and smm.outer_north_west is None):
            if(relation.objects_received[0] == True):
                smm.outer_north_west = relation.objects[0]
                updated_smm = True
        elif(relation.relation.name.value == "NorthEast" and smm.north_east ==None):
            if(relation.objects_received[0] == True):
                smm.north_east = relation.objects[0]
                updated_smm = True
        elif(relation.relation.name.value == "NorthEast" and smm.north_east is not None and smm.outer_north_east is None):
            if(relation.objects_received[0] == True):
                smm.outer_north_east = relation.objects[0]
                updated_smm = True
        elif(relation.relation.name.value == "SouthWest" and smm.south_west == None):
            if(relation.objects_received[0] == True):
                smm.south_west = relation.objects[0]
                updated_smm = True
        elif(relation.relation.name.value == "SouthWest" and smm.south_west is not None and smm.outer_south_west is None):
            if(relation.objects_received[0] == True):
                smm.outer_south_west = relation.objects[0]
                updated_smm = True
        elif(relation.relation.name.value == "SouthEast" and smm.south_east == None):
            if(relation.objects_received[0] == True):
                smm.south_east = relation.objects[0]
                updated_smm = True
        elif(relation.relation.name.value == "SouthEast" and smm.south_east is not None and smm.outer_south_east is None):
            if(relation.objects_received[0] == True):
                smm.outer_south_east = relation.objects[0]
                updated_smm = True
        if(updated_smm == False):
            self.create_new_smm(relation)

    """
    Create Json Object for stored smm in WM
    
    Returns
    ------------
    JsonObject
        returns the json object containing all stored smm in current WM
        i.e
    """
    def create_smm_json(self):
        self.logger.info("create json for stored smm")
        relation_list = []
        for smm in self.stored_smm:
            relation_for_list = {"north": smm.north, "south": smm.south, "west": smm.west, "east": smm.east, 
            "north-west": smm.north_west, "north-east": smm.north_east, "south-west": smm.south_west, "south-east": smm.south_east,
            "middle": smm.middle, "innerPart": smm.inner_part, "outerPart": smm.outer_part,
            "outer-north": smm.outer_north, "outer-south": smm.outer_south, "outer-west": smm.outer_west, "outer-east": smm.outer_east,
            "outer-north-west": smm.outer_north_west, "outer-north-east": smm.outer_north_east, 
            "outer-south-west": smm.outer_south_west, "outer-south-east": smm.outer_south_east }
            relation_list.append(relation_for_list)
        return{
            "smm": relation_list
        }

class SMM():
    def __init__(self):
        self.north = None
        self.outer_north = None
        self.south = None
        self.outer_south = None
        self.west = None
        self.outer_west = None
        self.east = None
        self.outer_east = None
        self.north_west = None
        self.outer_north_west = None
        self.north_east = None
        self.outer_north_east = None
        self.south_west = None
        self.outer_south_west = None
        self.south_east = None
        self.outer_south_east = None
        self.middle = None
        self.outer_part = None
        self.inner_part = None

        