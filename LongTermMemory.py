from collections import OrderedDict

class LongTermMemory:

    DECAY =  0.9
    RELATION_OBJECT_LINK_WEIGHT = 0.75
    OBJECT_RELATION_LINK_WEIGHT = 0.25
    FIRING_THRESHOLD = 0.5
    INITIAL_ACTIVATION_ON = 1
    INITIAL_ACTIVATION_OFF = 0


    def __init__(self):
        self.stored_relations = OrderedDict()
        self.stored_objects = OrderedDict()

    def save_relation_object_mapping(self, relation_to_objects_mapping):
        self._save_relation(relation_to_objects_mapping)
        self._save_object(relation_to_objects_mapping)
   
    def _save_relation(self, relation_to_objects_mapping):
        if (self.stored_relations.__contains__(relation_to_objects_mapping.relation.relation_type)):
            self.stored_relations.get(relation_to_objects_mapping.relation.relation_type).append(relation_to_objects_mapping)
        else:
            self.stored_relations[relation_to_objects_mapping.relation.relation_type] = [relation_to_objects_mapping]

    def _save_object(self, relation_to_objects_mapping):
        relation_reference_number = len(self.stored_relations[relation_to_objects_mapping.relation.relation_type]) -1
        relation_type = relation_to_objects_mapping.relation.relation_type
        for concrete_object in relation_to_objects_mapping.object_list:
            object_to_store = ObjectToRelationMapping(concrete_object, relation_type, relation_reference_number)
            if (self.stored_objects.__contains__(concrete_object.name)):
                self.stored_objects[concrete_object.name].append(object_to_store)
            else:
                self.stored_objects[concrete_object.name] = [object_to_store]

    def receive_knowledge_fragments(self, relation_type, object1, object2):
        self._spread_activation(relation_type, object1, object2)
        self._get_most_activated_fragments()
        
    
    def _spread_activation(self, intial_relation_type, initial_object1, initial_object2):
        self._set_initial_activation(intial_relation_type, initial_object1, initial_object2)
        while(self._firing_node_exists()):
            return "true"

    def _set_initial_activation(self, intial_relation_type, initial_object1, initial_object2):
        for relation_type, relation_to_objects_mappings in self.stored_relations.items():
            for relation_to_objects_mapping in relation_to_objects_mappings:
                if (relation_type == intial_relation_type):
                    relation_to_objects_mapping.activation = self.INITIAL_ACTIVATION_ON
                else:
                    relation_to_objects_mapping.activation = self.INITIAL_ACTIVATION_OFF
        for object_name, object_to_relation_mappings in self.stored_objects.items():
            for object_to_relation_mapping in object_to_relation_mappings:
                if(object_name == initial_object1.name or object_name == initial_object2.name):
                    object_to_relation_mapping.activation = self.INITIAL_ACTIVATION_ON
                else:
                    object_to_relation_mapping.activation = self.INITIAL_ACTIVATION_OFF
    
    def _firing_node_exists(self):
        return "true"
    
    def _get_most_activated_fragments(self):
        return "true"




class RelationToObjectsMapping:
    def __init__(self, relation, object_list):
        self.relation = relation
        self.object_list = object_list

class ObjectToRelationMapping:
    def __init__(self, stored_object, relation_type, relation_reference_number):
        self.stored_object = stored_object
        self.relation_type = relation_type
        self.reference_number = relation_reference_number