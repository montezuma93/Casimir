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
        self.spread_activation(context_array)
        retrieval_threshold = self._calculate_retrieval_threshold()
        return self._get_most_activated_knowledge_subnet(retrieval_threshold)
    
    def spread_activation(self, context_array):
        initial_activation_value = self.INITIAL_ACTIVATION_VALUE / len(context_array)
        for entity in context_array:
            print("##########################")
            self._set_initial_activation_for_entity(entity, initial_activation_value)
            self._spread_activation_for_entity(entity)
            self._update_activation_values()

    def _spread_activation_for_entity(self, entity):
        self.activation_spreading_in_progress = True
        while(self.activation_spreading_in_progress):
            self._update_linked_activation_for_relation()
            for stored_object in self.stored_objects.values():
                if(stored_object.is_active):
                    self._update_linked_activation_for_object(stored_object)

    def _set_initial_activation_for_entity(self, entity, initial_activation_value):
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

    def _calculate_retrieval_threshold(self):
        amount_of_nodes = 0
        retrieval_threshold = 0
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                amount_of_nodes += 1
                retrieval_threshold += stored_relation.activation
        for stored_object in self.stored_objects.values():
            amount_of_nodes += 1
            retrieval_threshold = stored_object.activation
        return retrieval_threshold / amount_of_nodes

    def _get_knowledge_subnets(self, retrieval_threshold):
        knowledge_subnets = []
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                if(stored_relation.activation > retrieval_threshold):
                    knowledge_subnet = KnowledgeSubnet(stored_relation)
                    knowledge_subnet.amount_of_activated_nodes += 1
                    knowledge_subnet.activation_value += stored_relation.activation
                    something_was_added = True
                    while(something_was_added):
                        object_was_added = self._add_active_objects_for_relation(knowledge_subnet, retrieval_threshold)
                        relation_was_added = self._add_active_relations_for_object(knowledge_subnet, retrieval_threshold)
                        if (object_was_added or relation_was_added):
                            something_was_added = True
                        else: 
                            something_was_added = False
                    knowledge_subnets.append(knowledge_subnet)  
        return knowledge_subnets

    def _add_active_objects_for_relation(self, knowledege_subnet, retrieval_threshold):
        something_got_added = False
        for relation_type, stored_relations in  knowledege_subnet.relations.items():
            for relation in stored_relations:
                for object_name in relation.objects:
                    stored_object = self.stored_objects[object_name]
                    if (stored_object.activation > retrieval_threshold):
                        if (knowledege_subnet.objects.__contains__(object_name)):
                            knowledege_subnet.objects[object_name].relation_links.append((relation_type, stored_relations.index(relation)))
                        else:
                            object_to_store = StoredObject(stored_object.stored_object, None)
                            object_to_store.relation_links.append((relation_type, stored_relations.index(relation)))
                            knowledege_subnet.objects[object_name] = object_to_store
                            knowledege_subnet.activation_value += stored_object.activation
                            knowledege_subnet.amount_of_activated_nodes += 1
                            something_got_added = True
                    else:
                        relation.objets.remove(object_name)
        return something_got_added

    def _add_active_relations_for_object(self, knowledege_subnet, retrieval_threshold):
        something_got_added = False
        for objects in knowledege_subnet.objects.values():
            for relation_link in objects.relation_links:
                stored_relation = self.stored_relations[relation_link[0]][relation_link[1]]
                if(stored_relation.activation > retrieval_threshold):
                    knowledege_subnet.amount_of_activated_nodes += 1
                    knowledege_subnet.activation_value += stored_relation.activation
                    if (knowledege_subnet.relations.__contains__(stored_relation.relation.relation_type)):
                        if(not knowledege_subnet.relations[stored_relation.relation.relation_type].__contains__(stored_relation)):
                            knowledege_subnet.relations.get(stored_relation.relation.relation_type).append(stored_relation)
                            something_got_added = True
                    else:
                        knowledege_subnet.relations[stored_relation.relation.relation_type] = [stored_relation]
                        something_got_added = True     
        return something_got_added

    def _get_most_activated_knowledge_subnet(self, retrieval_threshold):
        knowledge_subnets = self._get_knowledge_subnets(retrieval_threshold)
        most_actived_knowldege_subnet_average_activation_value = 0
        most_actived_knowldege_subnet = None
        for knowledge_subnet in knowledge_subnets:
            average_activation_value = knowledge_subnet.activation_value / knowledge_subnet.amount_of_activated_nodes
            if(average_activation_value > most_actived_knowldege_subnet_average_activation_value):
                most_actived_knowldege_subnet = knowledge_subnet
                most_actived_knowldege_subnet_average_activation_value = average_activation_value
        return most_actived_knowldege_subnet


class KnowledgeSubnet:
    def __init__(self, relation_to_store):
        self.relations = OrderedDict()
        self.relations[relation_to_store.relation.relation_type] = [relation_to_store]
        self.objects = OrderedDict()
        self.activation_value = 0
        self.amount_of_activated_nodes = 0

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