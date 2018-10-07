from collections import OrderedDict
from Relation import RelationType

class LongTermMemory:

    FRACTION_OF_ACTIVATION =  0.6
    INITIAL_ACTIVATION_VALUE = 1
    NOISE = 0.1


    def __init__(self):
        self.activation_spreading_in_progress = True
        self.time_since_initialization = 0
        self.firing_threshold = 0.01667
        self.stored_relations = OrderedDict()
        self.stored_objects = OrderedDict()

    def save_knowledge_fragment(self, relation, objects):
        self.time_since_initialization += 1
        self._save_relation(relation, objects)
        relation_reference_number = len(self.stored_relations[relation.relation_type]) -1
        self._save_objects_for_relation(objects, relation.relation_type, relation_reference_number)
   
    def _save_relation(self, relation, objects):
        relation_to_store = StoredRelation(relation, objects, self.time_since_initialization)
        if (self.stored_relations.__contains__(relation.relation_type)):
            self.stored_relations.get(relation.relation_type).append(relation_to_store)
        else:
            self.stored_relations[relation.relation_type] = [relation_to_store]

    def _save_objects_for_relation(self, objects, relation_type, relation_reference_number):
        for concrete_object in objects:
            if (self.stored_objects.__contains__(concrete_object.name)):
                self.stored_objects[concrete_object.name].amount_of_usages += 1
                self.stored_objects[concrete_object.name].relation_links.append((relation_type, relation_reference_number))
            else:
                object_to_store = StoredObject(concrete_object, self.time_since_initialization)
                object_to_store.relation_links.append((relation_type, relation_reference_number))
                self.stored_objects[concrete_object.name]= object_to_store

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
            for stored_object in self.stored_objects.values():
                if(stored_object.is_active):
                    self._update_linked_activation_for_object(stored_object)

    def _set_initial_activation(self, entity, initial_activation_value):
        if(type(entity) is RelationType):
            for relation_type, stored_relations in self.stored_relations.items():
                for stored_relation in stored_relations:
                    if (relation_type == entity):
                        stored_relation.activation_to_update = initial_activation_value * self.FRACTION_OF_ACTIVATION / len(stored_relations)
                        stored_relation.is_active = True
                    else:
                        stored_relation.activation_to_update = 0
                        stored_relation.is_active = False
            for object_name, stored_objects in self.stored_objects.items():
                stored_objects.is_active = False
                stored_objects.activation_to_update = 0
        else:
            for object_name, stored_objects in self.stored_objects.items():
                if (object_name == entity.name):
                    stored_objects.activation_to_update = initial_activation_value
                    stored_objects.is_active = True
                else:
                    stored_objects.is_active = False
                    stored_objects.activation_to_update = 0
            for stored_relations in self.stored_relations.values():
                for stored_relation in stored_relations:
                    stored_relation.activation_to_update = 0
                    stored_relation.is_active = False

    
    def _update_linked_activation_for_relation(self):
        self.activation_spreading_in_progress = False
        objects_to_set_active = []
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                if (stored_relation.is_active):
                    objects_to_update = [object_name for object_name in stored_relation.objects if self.stored_objects[object_name].is_active == False]
                    if(len(objects_to_update) == 0):
                        continue
                    activation_value_to_spread = stored_relation.activation_to_update * self.FRACTION_OF_ACTIVATION / len(objects_to_update)
                    if(activation_value_to_spread > self.firing_threshold):
                        for object_name in objects_to_update:
                            self.activation_spreading_in_progress = True
                            if(not objects_to_set_active.__contains__(object_name)):
                                objects_to_set_active.append(object_name)
                            self.stored_objects[object_name].activation_to_update += activation_value_to_spread
        for object_name in objects_to_set_active:
            self.stored_objects[object_name].is_active = True

    def _update_linked_activation_for_object(self, stored_object):
        self.activation_spreading_in_progress = False
        relations_to_update = []
        for relation_link in stored_object.relation_links:
            if (self.stored_relations[relation_link[0]][relation_link[1]].is_active == False):
                relations_to_update.append(self.stored_relations[relation_link[0]][relation_link[1]])
        if(len(relations_to_update)==0):
            return
        activation_value_to_spread = stored_object.activation_to_update * self.FRACTION_OF_ACTIVATION / len(relations_to_update)
        if(activation_value_to_spread > self.firing_threshold):
            for relation_to_update in relations_to_update:
                relation_to_update.activation_to_update += activation_value_to_spread
                relation_to_update.is_active = True
                self.activation_spreading_in_progress = True

    def _update_activation_values(self):
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                print("relation")
                print(stored_relation.relation.relation_type.value)
                print(stored_relation.objects[0])
                print(stored_relation.objects[1])
                print(stored_relation.activation)
                print(stored_relation.activation_to_update)
                stored_relation.activation += stored_relation.activation_to_update
        for stored_object in self.stored_objects.values():
            print("object")
            print(stored_object.stored_object.name)
            print(stored_object.activation)
            print(stored_object.activation_to_update)
            stored_object.activation += stored_object.activation_to_update

    def _get_most_activated_fragments(self):
        fragment_list = []
        for relation_to_objects_mappings in self.stored_relations.values():
            for relation_to_objects_mapping in relation_to_objects_mappings:
                if(relation_to_objects_mapping.activation >= 0.5):
                    fragment_list.append(relation_to_objects_mapping)
        fragment_list.sort(key=lambda fragment: fragment.activation, reverse=False)
        return fragment_list




class StoredRelation:
    def __init__(self, relation, objects, time_of_creation):
        self.relation = relation
        self.objects = [concrete_object.name for concrete_object in objects]
        self.time_of_creation = time_of_creation
        self.amout_of_usages = 1
        self.activation = 0
        self.activation_to_update = 0
        self.is_active = False

class StoredObject:
    def __init__(self, stored_object, time_of_creation):
        self.relation_links = []
        self.stored_object = stored_object
        self.time_of_creation = time_of_creation
        self.amount_of_usages = 1
        self.is_active = False
        self.activation = 0
        self.activation_to_update = 0