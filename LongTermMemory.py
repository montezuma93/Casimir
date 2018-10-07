from collections import OrderedDict
from Relation import RelationType

class LongTermMemory:

    FRACTION_OF_ACTIVATION =  0.6
    INITIAL_ACTIVATION_VALUE = 1
    RETRIEVAL_ACTIVATION_THRESHOLD = 0.7
    NOISE = 0.1


    def __init__(self):
        self.activation_spreading_in_progress = True
        self.time_since_initialization = 0
        self.firing_threshold = 0.01667
        self.stored_relations = OrderedDict()
        self.stored_objects = OrderedDict()

    def save_relation_object_mapping(self, relation_to_objects_mapping):
        self.time_since_initialization += 1
        self._save_relation(relation_to_objects_mapping)
        self._save_object(relation_to_objects_mapping)
   
    def _save_relation(self, relation_to_objects_mapping):
        relation_to_objects_mapping.time_of_initialization = self.time_since_initialization
        relation_to_objects_mapping.amout_of_usages = 1
        relation_to_objects_mapping.activation = 0
        relation_to_objects_mapping.activation_to_update = 0
        relation_to_objects_mapping.is_active = False
        if (self.stored_relations.__contains__(relation_to_objects_mapping.relation.relation_type)):
            self.stored_relations.get(relation_to_objects_mapping.relation.relation_type).append(relation_to_objects_mapping)
        else:
            self.stored_relations[relation_to_objects_mapping.relation.relation_type] = [relation_to_objects_mapping]

    def _save_object(self, relation_to_objects_mapping):
        relation_reference_number = len(self.stored_relations[relation_to_objects_mapping.relation.relation_type]) -1
        relation_type = relation_to_objects_mapping.relation.relation_type
        for concrete_object in relation_to_objects_mapping.object_list:
            concrete_object.is_active = False
            concrete_object.activation = 0
            concrete_object.activation_to_update = 0
            if (self.stored_objects.__contains__(concrete_object.name)):
                self.stored_objects[concrete_object.name].amount_of_usages += 1
                self.stored_objects[concrete_object.name].relation_links.append((relation_type, relation_reference_number))
            else:
                object_to_store = ObjectToRelationMapping(concrete_object, self.time_since_initialization)
                object_to_store.relation_links.append((relation_type, relation_reference_number))
                self.stored_objects[concrete_object.name] = object_to_store

    def receive_knowledge_fragments(self, context_array):
        self.time_since_initialization += 1
        initial_activation_value = self.INITIAL_ACTIVATION_VALUE / len(context_array)
        for entity in context_array:
            print("##########################")
            self._spread_activation(entity, initial_activation_value)
            self._update_activation_values()
        return self._get_most_activated_fragments()
    
    def _spread_activation(self, entity, initial_activation_value):
        self._set_initial_activation(entity, initial_activation_value)
        self.activation_spreading_in_progress = True
        while(self.activation_spreading_in_progress):
            self._update_linked_activation_for_relation()
            for concrete_object in self.stored_objects.values():
                if(concrete_object.stored_object.is_active):
                    self._update_linked_activation_for_object(concrete_object)

    def _set_initial_activation(self, entity, initial_activation_value):
        if(type(entity) is RelationType):
            for relation_type, relation_to_objects_mappings in self.stored_relations.items():
                for relation_to_objects_mapping in relation_to_objects_mappings:
                    if (relation_type == entity):
                        relation_to_objects_mapping.activation_to_update = initial_activation_value * self.FRACTION_OF_ACTIVATION / len(relation_to_objects_mappings)
                        relation_to_objects_mapping.is_active = True
                    else:
                        relation_to_objects_mapping.activation_to_update = 0
                        relation_to_objects_mapping.is_active = False
            for object_name, object_to_relation_mapping in self.stored_objects.items():
                object_to_relation_mapping.stored_object.is_active = False
                object_to_relation_mapping.stored_object.activation_to_update = 0
        else:
            for object_name, object_to_relation_mapping in self.stored_objects.items():
                if (object_name == entity.name):
                    object_to_relation_mapping.stored_object.activation_to_update = initial_activation_value
                    object_to_relation_mapping.stored_object.is_active = True
                else:
                    object_to_relation_mapping.stored_object.is_active = False
                    object_to_relation_mapping.stored_object.activation_to_update = 0
            for relation_to_objects_mappings in self.stored_relations.values():
                for relation_to_objects_mapping in relation_to_objects_mappings:
                    relation_to_objects_mapping.activation_to_update = 0
                    relation_to_objects_mapping.is_active = False

    
    def _update_linked_activation_for_relation(self):
        self.activation_spreading_in_progress = False
        objects_to_set_active = []
        for relation_to_objects_mappings in self.stored_relations.values():
            for relation_to_objects_mapping in relation_to_objects_mappings:
                if (relation_to_objects_mapping.is_active):
                    objects_to_update = [object_to_update for object_to_update in relation_to_objects_mapping.object_list if object_to_update.is_active == False]
                    if(len(objects_to_update) == 0):
                        continue
                    activation_value_to_spread = relation_to_objects_mapping.activation_to_update * self.FRACTION_OF_ACTIVATION / len(objects_to_update)
                    if(activation_value_to_spread > self.firing_threshold):
                        for object_to_update in objects_to_update:
                            self.activation_spreading_in_progress = True
                            if(not objects_to_set_active.__contains__(object_to_update)):
                                objects_to_set_active.append(object_to_update)
                            object_to_update.activation_to_update += activation_value_to_spread
        for concrete_object in objects_to_set_active:
            concrete_object.is_active = True

    def _update_linked_activation_for_object(self, concrete_object):
        self.activation_spreading_in_progress = False
        relations_to_update = []
        for relation_link in concrete_object.relation_links:
            if (self.stored_relations[relation_link[0]][relation_link[1]].is_active == False):
                relations_to_update.append(self.stored_relations[relation_link[0]][relation_link[1]])
        if(len(relations_to_update)==0):
            return
        activation_value_to_spread = concrete_object.stored_object.activation_to_update * self.FRACTION_OF_ACTIVATION / len(relations_to_update)
        if(activation_value_to_spread > self.firing_threshold):
            for relation_to_update in relations_to_update:
                relation_to_update.activation_to_update += activation_value_to_spread
                relation_to_update.is_active = True
                self.activation_spreading_in_progress = True

    def _update_activation_values(self):
        for relation_to_objects_mappings in self.stored_relations.values():
            for relation_to_objects_mapping in relation_to_objects_mappings:
                print("relation")
                print(relation_to_objects_mapping.relation.relation_type.value)
                print(relation_to_objects_mapping.object_list[0].name)
                print(relation_to_objects_mapping.object_list[1].name)
                print(relation_to_objects_mapping.activation)
                print(relation_to_objects_mapping.activation_to_update)
                relation_to_objects_mapping.activation += relation_to_objects_mapping.activation_to_update
        for concrete_object in self.stored_objects.values():
            print("object")
            print(concrete_object.stored_object.name)
            print(concrete_object.stored_object.activation)
            print(concrete_object.stored_object.activation_to_update)
            concrete_object.stored_object.activation += concrete_object.stored_object.activation_to_update

    def _get_most_activated_fragments(self):
        fragment_list = []
        for relation_to_objects_mappings in self.stored_relations.values():
            for relation_to_objects_mapping in relation_to_objects_mappings:
                if(relation_to_objects_mapping.activation >= 0.5):
                    fragment_list.append(relation_to_objects_mapping)
        fragment_list.sort(key=lambda fragment: fragment.activation, reverse=False)
        return fragment_list




class RelationToObjectsMapping:
    def __init__(self, relation, object_list):
        self.relation = relation
        self.object_list = object_list

class ObjectToRelationMapping:
    def __init__(self, stored_object, time_of_initialization):
        self.relation_links = []
        self.stored_object = stored_object
        self.time_of_initialization = time_of_initialization
        self.amount_of_usages = 1