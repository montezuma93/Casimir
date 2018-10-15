from collections import OrderedDict
from Relation import RelationType
from numpy import log, sqrt, power, random, pi
import copy

class LongTermMemory:

    BASE_ACTIVATION_DECAY = -0.5
    FRACTION_OF_ACTIVATION =  0.6
    INITIAL_ACTIVATION_VALUE = 1
    NOISE = 0.1
    DYNAMIC_FIRING_THRESHOLD = False
    FIRING_THRESHOLD = 0.01667
    NOISE_ON = True

    def __init__(self):
        self.activation_spreading_in_progress = False
        self.time_since_initialization = 0
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
                self.stored_objects[concrete_object.name].usages.append(self.time_since_initialization)
                self.stored_objects[concrete_object.name].relation_links.append((relation_type, relation_reference_number))
            else:
                object_to_store = StoredObject(concrete_object, self.time_since_initialization)
                object_to_store.relation_links.append((relation_type, relation_reference_number))
                self.stored_objects[concrete_object.name] = object_to_store
                
    def receive_knowledge_fragments(self, context_array):
        self.time_since_initialization += 1
        self.calculate_activation(context_array)
        retrieval_threshold = self._calculate_retrieval_threshold()
        knowledge_subnets = self.get_knowledge_subnets(retrieval_threshold)
        return self.get_most_activated_knowledge_subnet(knowledge_subnets)        
    
    def calculate_activation(self, context_array):
        self.spread_activation(context_array)
        self.calculate_base_activation()
        if(self.NOISE_ON):
            self.add_noise_to_activation()

    def spread_activation(self, context_array):
        if(self.DYNAMIC_FIRING_THRESHOLD):
            self.FIRING_THRESHOLD = len(context_array) * 0.0001
        initial_activation_value = self.INITIAL_ACTIVATION_VALUE / len(context_array)
        for entity in context_array:
            self._set_initial_activation_for_entity(entity, initial_activation_value)
            self._spread_activation_for_entity(entity)
            self._update_activation_values()

    def _set_initial_activation_for_entity(self, entity, initial_activation_value):
        entity.activation_to_update = 0
        for relation_type, stored_relations in self.stored_relations.items():
            for stored_relation in stored_relations:
                if (relation_type == entity):
                    stored_relation.activation_to_update = initial_activation_value * self.FRACTION_OF_ACTIVATION / len(stored_relations)
                    stored_relation.is_active = True
        for object_name, stored_objects in self.stored_objects.items():
            if (object_name == entity.name):
                stored_objects.activation_to_update = initial_activation_value
                stored_objects.is_active = True

    def _spread_activation_for_entity(self, entity):
        self.activation_spreading_in_progress = True
        while(self.activation_spreading_in_progress):
            self._update_linked_activation_for_relation()
            self._update_linked_activation_for_object()

    def _update_linked_activation_for_relation(self):
        self.activation_spreading_in_progress = False
        objects_to_set_active = []
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                if (stored_relation.is_active):
                    objects_to_update = [object_name for object_name in stored_relation.objects if self.stored_objects[object_name].is_active == False]
                    for object_name in objects_to_update:
                        activation_value_to_spread = stored_relation.activation_to_update * self.FRACTION_OF_ACTIVATION / len(objects_to_update)
                        if(activation_value_to_spread > self.FIRING_THRESHOLD):
                            self.activation_spreading_in_progress = True
                            objects_to_set_active.append(object_name) if object_name not in objects_to_set_active else None
                            self.stored_objects[object_name].activation_to_update += activation_value_to_spread
        for object_name in objects_to_set_active:
            self.stored_objects[object_name].is_active = True

    def _update_linked_activation_for_object(self):
        self.activation_spreading_in_progress = False
        relations_to_set_active = []
        for stored_object in self.stored_objects.values():
            if(stored_object.is_active):
                relations_to_update = []
                for relation_link in stored_object.relation_links:
                    if (self.stored_relations[relation_link[0]][relation_link[1]].is_active == False):
                        relations_to_update.append(self.stored_relations[relation_link[0]][relation_link[1]])
                if(len(relations_to_update)==0):
                    return
                activation_value_to_spread = stored_object.activation_to_update * self.FRACTION_OF_ACTIVATION / len(relations_to_update)
                if(activation_value_to_spread > self.FIRING_THRESHOLD):
                    for relation_to_update in relations_to_update:
                        relation_to_update.activation_to_update += activation_value_to_spread
                        relations_to_set_active.append(relation_to_update) if relation_to_update not in relations_to_set_active else None
                        relation_to_update.is_active = True
                        self.activation_spreading_in_progress = True
        for relation in relations_to_set_active:
            relation.is_active = True


    def _update_activation_values(self):
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                stored_relation.activation += stored_relation.activation_to_update
        for stored_object in self.stored_objects.values():
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
            retrieval_threshold += stored_object.activation
        print(retrieval_threshold / amount_of_nodes)
        return (retrieval_threshold / amount_of_nodes)

    def calculate_base_activation(self):            
        for relations in self.stored_relations.values():
            for relation in relations:
                print(relation.relation.name)
                print("SPREAD_ACTIVATION_VALUE")
                print(relation.activation)
                relation.activation += self._calculate_base_activation_for_node(relation)
                print("SPREAD_ACTIVATION_VALUE_WITH_BASE_ACTIVATION")
                print(relation.activation)
        for concrete_object in self.stored_objects.values():
            print(concrete_object.stored_object.name)
            print("SPREAD_ACTIVATION_VALUE")
            print(concrete_object.activation)
            concrete_object.activation += self._calculate_base_activation_for_node(concrete_object)
            print("SPREAD_ACTIVATION_VALUE_WITH_BASE_ACTIVATION")
            print(concrete_object.activation)

    def _calculate_base_activation_for_node(self, node):
        sum_over_usages = 0
        for usage in node.usages:
            sum_over_usages += power((self.time_since_initialization - usage), self.BASE_ACTIVATION_DECAY)
        return log(sum_over_usages)

    def add_noise_to_activation(self):
        for relations in self.stored_relations.values():
            for relation in relations:
                relation.activation += self._calculate_noise_for_node(relation)
        for concrete_object in self.stored_objects.values():
            concrete_object.activation += self._calculate_noise_for_node(concrete_object)

    def _calculate_noise_for_node(self, node):
        loc = 0
        scale = power(pi, 2) / 3 * power(self.NOISE,2)
        noise = random.logistic(loc, scale)
        return noise

    def get_knowledge_subnets(self, retrieval_threshold):
        knowledge_subnets = []
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                if(stored_relation.activation > retrieval_threshold and self._relation_not_yet_used_in_knowledge_subnet(knowledge_subnets, stored_relation.relation)):
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

    def _add_active_objects_for_relation(self, knowledge_subnet, retrieval_threshold):
        something_got_added = False
        for relation_type, stored_relations in  knowledge_subnet.relations.items():
            for relation in stored_relations:
                for object_name in relation.objects:
                    stored_object = self.stored_objects[object_name]
                    if (stored_object.activation > retrieval_threshold):
                        if (knowledge_subnet.objects.__contains__(object_name)):
                            if(not knowledge_subnet.objects[object_name].relation_links.__contains__((relation_type, stored_relations.index(relation)))):
                                knowledge_subnet.objects[object_name].relation_links.append((relation_type, stored_relations.index(relation)))
                        else:
                            object_to_store = copy.copy(stored_object)
                            object_to_store.relation_links = [(relation_type, stored_relations.index(relation))]
                            knowledge_subnet.objects[object_name] = object_to_store
                            knowledge_subnet.activation_value += stored_object.activation
                            knowledge_subnet.amount_of_activated_nodes += 1
                            something_got_added = True
                    else:
                        relation.objects.remove(object_name)
        return something_got_added

    def _add_active_relations_for_object(self, knowledge_subnet, retrieval_threshold):
        something_got_added = False
        for object_name in knowledge_subnet.objects.keys():
            for relation_link in self.stored_objects[object_name].relation_links:
                stored_relation = self.stored_relations[relation_link[0]][relation_link[1]]
                if(stored_relation.activation > retrieval_threshold):
                    if (knowledge_subnet.relations.__contains__(stored_relation.relation.relation_type)):
                        if(not knowledge_subnet.relations[stored_relation.relation.relation_type].__contains__(stored_relation)):
                            knowledge_subnet.relations.get(stored_relation.relation.relation_type).append(stored_relation)
                            something_got_added = True
                            knowledge_subnet.amount_of_activated_nodes += 1
                            knowledge_subnet.activation_value += stored_relation.activation
                    else:
                        knowledge_subnet.relations[stored_relation.relation.relation_type] = [stored_relation]
                        something_got_added = True
                        knowledge_subnet.amount_of_activated_nodes += 1
                        knowledge_subnet.activation_value += stored_relation.activation
        return something_got_added

    def _relation_not_yet_used_in_knowledge_subnet(self, knowledge_subnets, relation):
        if (len(knowledge_subnets) == 0 or
            not len([knowledge_subnet for knowledge_subnet in knowledge_subnets if not knowledge_subnet.relations[relation.relation_type].__contains__(relation)]) > 0):
            return True
        else:
            return False

    def get_most_activated_knowledge_subnet(self, knowledge_subnets):
        most_activated_knowledge_subnet_average_activation_value = 0
        most_activated_knowledge_subnet = None
        for knowledge_subnet in knowledge_subnets:
            average_activation_value = knowledge_subnet.activation_value / knowledge_subnet.amount_of_activated_nodes
            if(average_activation_value > most_activated_knowledge_subnet_average_activation_value):
                most_activated_knowledge_subnet = knowledge_subnet
                most_activated_knowledge_subnet_average_activation_value = average_activation_value
        return most_activated_knowledge_subnet

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
        self.amount_of_usages = 1
        self.activation = 0
        self.activation_to_update = 0
        self.is_active = False
        self.usages = [time_of_creation]

class StoredObject:
    def __init__(self, stored_object, time_of_creation):
        self.relation_links = []
        self.stored_object = stored_object
        self.time_of_creation = time_of_creation
        self.amount_of_usages = 1
        self.is_active = False
        self.activation = 0
        self.activation_to_update = 0
        self.usages = [time_of_creation]
