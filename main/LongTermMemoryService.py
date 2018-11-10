from collections import OrderedDict
from Relation import RelationType
from numpy import log, sqrt, power, random, pi
import copy
import json

class LongTermMemoryService:

    BASE_ACTIVATION_DECAY = -0.5
    FRACTION_OF_ACTIVATION =  0.6
    INITIAL_ACTIVATION_VALUE = 1
    NOISE = 0.1
    #false
    DYNAMIC_FIRING_THRESHOLD = True
    FIRING_THRESHOLD = 0.01667
    #True
    NOISE_ON = False
    #RECEIVE_ONLY_COMPLETE_KNOWLEDGE_FRAGMENTS = True
    #BASE_ACTIVATION_DECAY = -0.86
    #INITIAL_ACTIVATION_VALUE = 1.8

    def __init__(self):
        self.activation_spreading_in_progress = False
        self.receive_knowledge_fragments_in_progress = False
        self.time_since_initialization = 0
        self.stored_relations = OrderedDict()
        self.stored_objects = OrderedDict()

    def save_knowledge_fragment(self, relation, objects):
        self.time_since_initialization += 1
        self._save_relation(relation, objects)
        relation_reference_number = len(self.stored_relations[relation.relation_type]) -1
        self._save_objects_for_relation(objects, relation.relation_type, relation_reference_number)
   
    def _save_relation(self, relation, objects):
        relation_to_store = StoredRelation(relation, [concrete_object.name for concrete_object in objects], self.time_since_initialization)
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
        if not knowledge_subnets:
            print("none know")
            return None
        most_activated_knowledge_fragment = self.get_most_activated_knowledge_subnet(knowledge_subnets)       
        return most_activated_knowledge_fragment
    
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
            self._spread_activation_for_entity()
            self._update_activation_values()

    def _set_initial_activation_for_entity(self, entity, initial_activation_value):
        self._clean_up_activation_value_for_entities()
        for relation_type, stored_relations in self.stored_relations.items():
            for stored_relation in stored_relations:
                if (relation_type == entity):
                    stored_relation.activation_to_update = initial_activation_value * self.FRACTION_OF_ACTIVATION / len(stored_relations)
                    #stored_relation.activation_to_update = initial_activation_value
                    stored_relation.is_active = True
        for object_name, stored_objects in self.stored_objects.items():
            if (object_name == entity.name):
                stored_objects.activation_to_update = initial_activation_value
                stored_objects.is_active = True

    def _clean_up_activation_value_for_entities(self):
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                stored_relation.activation_to_update = 0
                stored_relation.is_active = False
        for stored_object in self.stored_objects.values():
            stored_object.activation_to_update = 0
            stored_object.is_active = False

    def _spread_activation_for_entity(self):
        self.activation_spreading_in_progress = True
        while(self.activation_spreading_in_progress):
            self._update_linked_activation_for_relation()
            self._update_linked_activation_for_object()

    def _update_linked_activation_for_relation(self):
        objects_to_set_active = []
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                if(stored_relation.is_active):
                    objects_to_update = [self.stored_objects[object_name] for object_name in stored_relation.objects if self.stored_objects[object_name].is_active == False]
                    for object_to_update in objects_to_update:
                        activation_value_to_spread = stored_relation.activation_to_update * self.FRACTION_OF_ACTIVATION / len(objects_to_update)
                        if(activation_value_to_spread > self.FIRING_THRESHOLD):
                            object_to_update.activation_to_update += activation_value_to_spread
                            objects_to_set_active.append(object_to_update)
        self._set_nodes_active(objects_to_set_active)

    def _update_linked_activation_for_object(self):       
        relations_to_set_active = []
        for stored_object in self.stored_objects.values():
            relations_to_update = []
            for relation_link in stored_object.relation_links:
                if (stored_object.is_active and self.stored_relations[relation_link[0]][relation_link[1]].is_active == False):
                    relations_to_update.append(self.stored_relations[relation_link[0]][relation_link[1]])
            for relation_to_update in relations_to_update:
                activation_value_to_spread = stored_object.activation_to_update * self.FRACTION_OF_ACTIVATION / len(relations_to_update)
                if(activation_value_to_spread > self.FIRING_THRESHOLD):
                    relation_to_update.activation_to_update += activation_value_to_spread
                    relations_to_set_active.append(relation_to_update)
        self._set_nodes_active(relations_to_set_active)

    def _set_nodes_active(self, nodes_to_set_active):
        if(len(nodes_to_set_active) > 0):
            self.activation_spreading_in_progress = True
        else:
            self.activation_spreading_in_progress = False
        for node in nodes_to_set_active:
            node.is_active = True

    def _update_activation_values(self):
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                stored_relation.activation += stored_relation.activation_to_update
        for stored_object in self.stored_objects.values():
            stored_object.activation += stored_object.activation_to_update

    def calculate_base_activation(self):            
        for relations in self.stored_relations.values():
            for relation in relations:
                relation.activation += self._calculate_base_activation_for_node(relation)
        for concrete_object in self.stored_objects.values():
            concrete_object.activation += self._calculate_base_activation_for_node(concrete_object)

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
        if amount_of_nodes == 0:
            return None
        return (retrieval_threshold / amount_of_nodes)



    def get_knowledge_subnets(self, retrieval_threshold):
        knowledge_subnets = []
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                if(stored_relation.activation > retrieval_threshold and self._relation_not_yet_used_in_knowledge_subnet(knowledge_subnets, stored_relation)):
                    knowledge_subnets.append(self.create_knowledge_subnet_for_relation(stored_relation, retrieval_threshold))
        return knowledge_subnets
    
    def _relation_not_yet_used_in_knowledge_subnet(self, knowledge_subnets, stored_relation):
        for knowledge_subnet in knowledge_subnets:
            for relations in knowledge_subnet.relations.values():
                for relation in relations:
                    if relation.relation.name == stored_relation.relation.name and relation.objects == stored_relation.objects:
                      return False
        return True

    def create_knowledge_subnet_for_relation(self, stored_relation, retrieval_threshold):
        relation_to_store = StoredRelation(stored_relation.relation, stored_relation.objects, stored_relation.time_of_creation)
        knowledge_subnet = KnowledgeSubnet(relation_to_store)
        self.retrieve_activated_nodes_through_knowledge_subnet(knowledge_subnet, retrieval_threshold)
        return knowledge_subnet
    
    def retrieve_activated_nodes_through_knowledge_subnet(self, knowledge_subnet, retrieval_threshold):
        self.receive_knowledge_fragments_in_progress = True
        while(self.receive_knowledge_fragments_in_progress):
            self._check_objects_in_relations_can_be_added(knowledge_subnet, retrieval_threshold)
            self._check_relation_in_objects_can_be_added(knowledge_subnet, retrieval_threshold)

    def _check_objects_in_relations_can_be_added(self, knowledge_subnet, retrieval_threshold):
        self.receive_knowledge_fragments_in_progress = False
        for relation_type, stored_relations in knowledge_subnet.relations.items():
            for relation in stored_relations:
                for object_name in relation.objects:
                    if object_name != None:
                        object_to_add_eventually = self.stored_objects[object_name]
                        if (object_to_add_eventually.activation > retrieval_threshold):
                            self._add_object_to_knowledge_subnet(object_to_add_eventually, knowledge_subnet, (relation_type, stored_relations.index(relation)))
                        else:
                            index = relation.objects.index(object_name)
                            relation.objects[index] = None

    def _add_object_to_knowledge_subnet(self, object_to_add, knowledge_subnet, relation_link):
        if (knowledge_subnet.objects.__contains__(object_to_add.stored_object.name)):
            if(not knowledge_subnet.objects[object_to_add.stored_object.name].relation_links.__contains__(relation_link)):
                knowledge_subnet.objects[object_to_add.stored_object.name].relation_links.append(relation_link)
        else:
            object_to_store = StoredObject(object_to_add.stored_object, object_to_add.time_of_creation)
            object_to_store.activation = object_to_add.activation
            object_to_store.relation_links = [relation_link]
            knowledge_subnet.objects[object_to_add.stored_object.name] = object_to_store
            knowledge_subnet.activation_value += object_to_store.activation
            knowledge_subnet.amount_of_activated_nodes += 1
            self.receive_knowledge_fragments_in_progress = True

    def _check_relation_in_objects_can_be_added(self, knowledge_subnet, retrieval_threshold):
        self.receive_knowledge_fragments_in_progress = False
        for object_name in knowledge_subnet.objects.keys():
            for relation_link in self.stored_objects[object_name].relation_links:
                relation_to_add_eventually = self.stored_relations[relation_link[0]][relation_link[1]]
                if(relation_to_add_eventually.activation > retrieval_threshold):
                    self._add_relations_to_knowledge_subnet(relation_to_add_eventually, knowledge_subnet)

    def _add_relations_to_knowledge_subnet(self, relation, knowledge_subnet):
        relation_to_add = StoredRelation(relation.relation, relation.objects, relation.time_of_creation)
        relation_to_add.activation = relation.activation
        if (knowledge_subnet.relations.__contains__(relation_to_add.relation.relation_type)):
            if(not knowledge_subnet.relations[relation_to_add.relation.relation_type].__contains__(relation_to_add)):
                knowledge_subnet.relations.get(relation_to_add.relation.relation_type).append(relation_to_add)
                knowledge_subnet.amount_of_activated_nodes += 1
                knowledge_subnet.activation_value += relation_to_add.activation
                self.receive_knowledge_fragments_in_progress = True
        else:
            knowledge_subnet.relations[relation_to_add.relation.relation_type] = [relation_to_add]
            knowledge_subnet.amount_of_activated_nodes += 1
            knowledge_subnet.activation_value += relation_to_add.activation
            self.receive_knowledge_fragments_in_progress = True

    def get_most_activated_knowledge_subnet(self, knowledge_subnets):
        most_activated_knowledge_subnet_average_activation_value = 0
        most_activated_knowledge_subnet = None
        for knowledge_subnet in knowledge_subnets:
            average_activation_value = knowledge_subnet.activation_value / knowledge_subnet.amount_of_activated_nodes
            if(average_activation_value > most_activated_knowledge_subnet_average_activation_value):
                most_activated_knowledge_subnet = knowledge_subnet
                most_activated_knowledge_subnet_average_activation_value = average_activation_value
        return most_activated_knowledge_subnet

    def show_all_knowledge_fragments(self):
        object_list = []
        relation_list = []
        for concrete_object in self.stored_objects.values():
            object_for_list = {"name":concrete_object.stored_object.name,
             "activation": concrete_object.activation}
            object_list.append(object_for_list)
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                relation_for_list = {"category": stored_relation.relation.relation_type.value, 
                "name": stored_relation.relation.name.value, 
                "activation": stored_relation.activation, 
                "objects": None}
                object_of_relation_list = []
                for concrete_object in stored_relation.objects:
                    object_for_relation_list = {"name":concrete_object}
                    object_of_relation_list.append(object_for_relation_list)
                relation_for_list["objects"] = object_of_relation_list
                relation_list.append(relation_for_list)    
        return{
            "retrival-threshold": self._calculate_retrieval_threshold(),
            "objects": object_list,
            "relations": relation_list
        }


class KnowledgeSubnet():
    def __init__(self, node_to_store):
        if(type(node_to_store) is StoredRelation):
            self.objects = OrderedDict()
            self.relations = OrderedDict()
            self.relations[node_to_store.relation.relation_type] = [node_to_store]
        else: 
            self.objects = OrderedDict()
            self.objects[node_to_store.stored_object.name] = node_to_store
            self.relations = OrderedDict()
        self.activation_value = node_to_store.activation
        self.amount_of_activated_nodes = 1

class StoredRelation():
    def __init__(self, relation, objects, time_of_creation):
        self.relation = relation
        self.objects = objects
        self.time_of_creation = time_of_creation
        self.amount_of_usages = 1
        self.activation = 0
        self.activation_to_update = 0
        self.is_active = False
        self.usages = [time_of_creation]
        self.is_complete = None

    def __eq__(self, other):
        if self.relation.name == other.relation.name and self.objects == other.objects:
            return True
        else:
            return False

class StoredObject():
    def __init__(self, stored_object, time_of_creation):
        self.relation_links = []
        self.stored_object = stored_object
        self.time_of_creation = time_of_creation
        self.amount_of_usages = 1
        self.is_active = False
        self.activation = 0
        self.activation_to_update = 0
        self.usages = [time_of_creation]

