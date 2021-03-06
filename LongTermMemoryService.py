from collections import OrderedDict
from Relation import RelationType
from numpy import log, sqrt, power, random, pi
import copy
import json
import logging

class LongTermMemoryService:

    #Should be default values
    BASE_ACTIVATION_DECAY = -0.5
    FRACTION_OF_ACTIVATION =  0.6
    INITIAL_ACTIVATION_VALUE = 1
    NOISE = 0.1
    DYNAMIC_FIRING_THRESHOLD = True
    FIRING_THRESHOLD = 0.01667
    NOISE_ON = False
    SPREAD_FULL_ACTIVATION = False
    EPSILON = 0.01

    """
    Initialize a empty LongTermMemory
    """
    def __init__(self):
        self.logger = logging.getLogger('LongTermMemory')
        self.logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        self.logger.addHandler(stream_handler)

        self.activation_spreading_in_progress = False
        self.receive_knowledge_fragments_in_progress = False
        self.time_since_initialization = 0
        self.stored_relations = OrderedDict()
        self.stored_objects = OrderedDict()

    """
    Reset and clean up simulation
    """
    def reset_simulation(self):
        self.activation_spreading_in_progress = False
        self.receive_knowledge_fragments_in_progress = False
        self.time_since_initialization = 0
        self.stored_relations = OrderedDict()
        self.stored_objects = OrderedDict()

    """
    Update setting used in LTM calculations

    Parameters
    ----------
    param1 : float
        should be between 0 and -1, used to calculate the forgetting process
    param2 : float
        should be between 0 and 1, used to calculate how much of the previous activation value is spread to the next nodes
    param3 : float
        should be positive, the activation value that is spread in the beginning of an activation spreading process
    param4 : float
        value is used to calculated the noise activation value that is added to the nodes
    param5 : boolean
        true if the firing_threshold should be calculated dynamically or it should use a fix value
    param6 : float
        should be a small value below 1, is just used if DYNAMIC_FIRING_THRESHOLD is set to false
    param7 : boolean
        true if noise activation should be calculated and added to a nodes activation
    param8 : boolean
        true if the initial activation value should be added to the concrete categories instead of splitting the value among them, by going through
        the relation category
    """
    def update_settings(self, base_activation_decay, fraction_of_activation, initial_activation_value, noise,
     dynamic_firing_threshold, firing_threshold, noise_on, spread_full_activation):
        if(base_activation_decay != ''):
            self.BASE_ACTIVATION_DECAY = base_activation_decay
        if(fraction_of_activation != ''):
            self.FRACTION_OF_ACTIVATION = fraction_of_activation
        if(initial_activation_value != ''):
            self.INITIAL_ACTIVATION_VALUE = initial_activation_value
        if(noise != ''):
            self.NOISE = noise
        if(dynamic_firing_threshold != ''):
            self.DYNAMIC_FIRING_THRESHOLD = dynamic_firing_threshold
        if(firing_threshold != ''):
            self.FIRING_THRESHOLD = firing_threshold
        if(noise_on != ''):
            self.NOISE_ON = noise_on
        if(spread_full_activation != ''):
            self.SPREAD_FULL_ACTIVATION = spread_full_activation

    """
    Stores knowledge_fragments in the LTM

    Parameters
    ----------
    param1 : StoredRelation
        StoredRelation, that should be saved
    param2 : List of StoredObjects
        StoredObjects, that should be saved
    """
    def save_knowledge_fragment(self, relation, objects):
        self.logger.info('Got save request')
        self.time_since_initialization += 1
        self._save_relation(relation, objects)
        relation_reference_number = len(self.stored_relations[relation.relation_type]) -1
        self._save_objects_for_relation(objects, relation.relation_type, relation_reference_number)
   
    """
    Stores relations in the LTM

    Parameters
    ----------
    param1 : StoredRelation
        StoredRelation, that should be saved
    param2 : List of StoredObjects
        StoredObjects, that should be saved
    """
    def _save_relation(self, relation, objects):
        self.logger.info('Save relation for type: %s, and name: %s', relation.relation_type, relation.name)
        relation_to_store = StoredRelation(relation, [concrete_object.name for concrete_object in objects], self.time_since_initialization)
        if (self.stored_relations.__contains__(relation.relation_type)):
            self.stored_relations.get(relation.relation_type).append(relation_to_store)
        else:
            self.stored_relations[relation.relation_type] = [relation_to_store]

    """
    Stores Objects in the LTM

    Parameters
    ----------
    param1 : List of StoredObjects
        StoredRelation, that should be saved
    param2 : RelationType (Enum) 
        RelationType of the relation, to which the objects belong to
    param3 : int
        Index of the relation in the stored_relation list of the LTM
    """
    def _save_objects_for_relation(self, objects, relation_type, relation_reference_number):
        for concrete_object in objects:
            self.logger.info('Save object with name: %s', concrete_object.name)
            if (self.stored_objects.__contains__(concrete_object.name)):
                self.stored_objects[concrete_object.name].amount_of_usages += 1
                self.stored_objects[concrete_object.name].usages.append(self.time_since_initialization)
                self.stored_objects[concrete_object.name].relation_links.append((relation_type, relation_reference_number))
            else:
                object_to_store = StoredObject(concrete_object, self.time_since_initialization)
                object_to_store.relation_links.append((relation_type, relation_reference_number))
                self.stored_objects[concrete_object.name] = object_to_store

    """
    Receives most activated knowledge subnet
    Calculates activation, base activation and noise before

    Parameters
    ----------
    param1 : List of entities
        List of Relations or Object to receive knowledge_subnet for and spread activation before
    """        
    def receive_knowledge_fragments(self, context_array):
        self.logger.info('Receive Knowledge Fragments request for context array: %s', context_array)
        self.time_since_initialization += 1
        self.calculate_activation(context_array)
        retrieval_threshold = self._calculate_retrieval_threshold()
        knowledge_subnets = self.get_knowledge_subnets(retrieval_threshold)
        if not knowledge_subnets:
            return None
        most_activated_knowledge_fragment = self.get_most_activated_knowledge_subnet(knowledge_subnets)
        self.mark_received_nodes_for_activated_knowledge_fragment(most_activated_knowledge_fragment)
        self.add_usage_for_activated_knowledge_fragments(most_activated_knowledge_fragment)
        return most_activated_knowledge_fragment
    
    """
    Calculate activation values for all entities

    Parameters
    ----------
    param1 : List of entities
        List of Relations or Objects to spread activation
    """    
    def calculate_activation(self, context_array):
        self.spread_activation(context_array)
        self.calculate_base_activation()
        if(self.NOISE_ON):
            self.add_noise_to_activation()

    """
    Spread activation for context array entities

    Parameters
    ----------
    param1 : List of entities
        List of Relations or Object to spread activation
    """    
    def spread_activation(self, context_array):
        self.logger.info('Spread activation for context array: %s', context_array)
        if(self.DYNAMIC_FIRING_THRESHOLD):
            self.FIRING_THRESHOLD = len(context_array) * 0.0001
        initial_activation_value = self.INITIAL_ACTIVATION_VALUE / len(context_array)
        for entity in context_array:
            self._set_initial_activation_for_entity(entity, initial_activation_value)
            self._spread_activation_for_entity()
            self._update_activation_values()

    """
    Set initial activation value for context entities and set it to active

    Parameters
    ----------
    param1 : entity, can be object or relation
        entity, that will receive the initial activation value and will be set to active
    param2 : float
        initial activation value, that the entity will receive
    """   
    def _set_initial_activation_for_entity(self, entity, initial_activation_value):
        self._clean_up_activation_values()
        for relation_type, stored_relations in self.stored_relations.items():
            for stored_relation in stored_relations:
                if (relation_type == entity):
                    if self.SPREAD_FULL_ACTIVATION:
                        stored_relation.activation_to_update = initial_activation_value
                    else:
                        stored_relation.activation_to_update = initial_activation_value * self.FRACTION_OF_ACTIVATION / len(stored_relations)
                    stored_relation.is_active = True
        for object_name, stored_objects in self.stored_objects.items():
            if (object_name == entity.name):
                stored_objects.activation_to_update = initial_activation_value
                stored_objects.is_active = True

    """
    Clean up all activation values and set all entities to not active
    """   
    def _clean_up_activation_values(self):
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                stored_relation.activation_to_update = 0
                stored_relation.is_active = False
        for stored_object in self.stored_objects.values():
            stored_object.activation_to_update = 0
            stored_object.is_active = False

    """
    Spread activation for an entity as long as activation spreading is in progress.
    Activation spreading is in progress as long as the activation value that will be spread
    to the next entity via its connections is higher that the spreading threshold
    """   
    def _spread_activation_for_entity(self):
        self.activation_spreading_in_progress = True
        while(self.activation_spreading_in_progress):
            self._update_linked_activation_for_relation()
            self._update_linked_activation_for_object()

    """
    Spread activation for all activated relations and sets objects which are not yet active to active as
    well as set their activation value, that should be added
    """   
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

    """
    Spread activation for all activated objects and sets relation which are not yet active to active as
    well as increase their activation value
    """  
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

    """
    Sets nodes to be active, if their is at least one node to set active,
    activation spreading will be in progress

    Parameters
    ----------
    param1 : List of entities, can be objects and relations
        entities to set active
    """  
    def _set_nodes_active(self, nodes_to_set_active):
        if(len(nodes_to_set_active) > 0):
            self.activation_spreading_in_progress = True
        else:
            self.activation_spreading_in_progress = False
        for node in nodes_to_set_active:
            node.is_active = True

    """
    For all nodes add the activation value that should be added to the
    activation value of the node
    """  
    def _update_activation_values(self):
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                stored_relation.activation += stored_relation.activation_to_update
        for stored_object in self.stored_objects.values():
            stored_object.activation += stored_object.activation_to_update


    """
    Calculate the base activation value for all nodes
    and add it to the activation value
    """  
    def calculate_base_activation(self):            
        for relations in self.stored_relations.values():
            for relation in relations:
                relation.activation += self._calculate_base_activation_for_node(relation)
        for concrete_object in self.stored_objects.values():
            concrete_object.activation += self._calculate_base_activation_for_node(concrete_object)

    """
    Calculate the base activation value for a node

    Parameters
    ----------
    param1 : Entity
        entity, for which the base activation value should be calculated for

    Returns
    --------
    float
        base activation value that will be added to the node
    """  
    def _calculate_base_activation_for_node(self, node):
        sum_over_usages = 0
        for usage in node.usages:
            sum_over_usages += power((self.time_since_initialization - usage), self.BASE_ACTIVATION_DECAY)
        return log(sum_over_usages)

    """
    Calculate the base activation value for all nodes and add it
    """  
    def add_noise_to_activation(self):
        for relations in self.stored_relations.values():
            for relation in relations:
                relation.activation += self._calculate_noise_for_node(relation)
        for concrete_object in self.stored_objects.values():
            concrete_object.activation += self._calculate_noise_for_node(concrete_object)

    """
    Calculate the noise activation value for a node to be added

    Parameters
    ----------
    param1 : Entity
        entity, for which the base activation value should be calculated for

    Returns
    --------
    float
        noise activation value that will be added to the node
    """  
    def _calculate_noise_for_node(self, node):
        loc = 0
        scale = power(pi, 2) / 3 * power(self.NOISE,2)
        noise = random.logistic(loc, scale)
        return noise
    
    """
    Calculate the noise retrieval threshold value for nodes
    Done by averaging all nodes activation value
    """  
    def _calculate_retrieval_threshold(self):
        amount_of_nodes = 0
        retrieval_threshold = 0
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                self.logger.info('Activation value of relation for type: %s, and name: %s is %s',
                 stored_relation.relation.relation_type, stored_relation.relation.name, stored_relation.activation)
                if not stored_relation.is_received:
                    amount_of_nodes += 1
                    retrieval_threshold += stored_relation.activation
        for object_name, stored_object in self.stored_objects.items():
            self.logger.info('Activation value of object with name: %s is %s',
                 object_name, stored_object.activation)
            if not stored_object.is_received:
                amount_of_nodes += 1
                retrieval_threshold += stored_object.activation
        if amount_of_nodes == 0:
            return None
        threshold = (retrieval_threshold / amount_of_nodes)
        self.logger.info('Retrieval Threshold is: %s', threshold)
        return threshold


    """
    Get all knowledge_subnets in the LTM

    Parameters
    ------------
    param1: float
        Retrieval_Threshold value, which determines if an entity can be received or not

    Returns
    ----------
    List of KnowledgeSubnet, can be empty
    """
    def get_knowledge_subnets(self, retrieval_threshold):
        knowledge_subnets = []
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                if(stored_relation.activation + self.EPSILON >= retrieval_threshold and self._relation_not_yet_used_in_knowledge_subnet(knowledge_subnets, stored_relation)):
                    self._clean_up_retrieved_mark()
                    knowledge_subnets.append(self.create_knowledge_subnet_for_relation(stored_relation, retrieval_threshold))
        self.logger.info('Found %s knowledge subnets', len(knowledge_subnets))
        return knowledge_subnets
    
    """
    Clean up all retrieved marks for all nodes
    """
    def _clean_up_retrieved_mark(self):
        for stored_relations in self.stored_relations.values():
            for stored_relation in stored_relations:
                for index in enumerate(stored_relation.objects_received):
                    stored_relation.objects_received[index[0]] = True
    """
    Check if relation not yet used in a created knowledge subnet

    Parameters
    ------------
    param1: List of KnownledgeSubnet
        List of KnowledgeSubnet to go through
    param2: StoredRelation
        StoredRelation to check, whether it is in the list of KnowledgeSubnet or not

    Returns
    ----------
    bool
        True if not in any Knowledge Subnet
    """
    def _relation_not_yet_used_in_knowledge_subnet(self, knowledge_subnets, stored_relation):
        for knowledge_subnet in knowledge_subnets:
            for relations in knowledge_subnet.relations.values():
                if relations.__contains__(stored_relation):
                    return False
        return True

    
    """
    Create KnowledgeSubnet for StoredRelation

    Parameters
    ------------
    param1: StoredRelation
        Relation, which is used to create KnowledgeSubnet
    param2: int
        Retrieval Threeshold, that decides whether nodes can be added to KnowledgeSubnet or not

    Returns
    ----------
    KnowledgeSubnet
        Returns full KnowledgeSubnet
    """
    def create_knowledge_subnet_for_relation(self, stored_relation, retrieval_threshold):
        relation_to_store = stored_relation
        knowledge_subnet = KnowledgeSubnet(relation_to_store)
        self.retrieve_activated_nodes_through_knowledge_subnet(knowledge_subnet, retrieval_threshold)
        return knowledge_subnet
    
    """
    Retrieve all nodes in an KnowledgeSubnet based on their links

    Parameters
    ------------
    param1: KnowledgeSubnet
        KnowledgeSubnet, to go through to add all activated nodes
    param2: int
        Retrieval Threeshold, that decides whether nodes can be added to KnowledgeSubnet or not
    """
    def retrieve_activated_nodes_through_knowledge_subnet(self, knowledge_subnet, retrieval_threshold):
        self.receive_knowledge_fragments_in_progress = True
        while(self.receive_knowledge_fragments_in_progress):
            self._check_objects_in_relations_can_be_added(knowledge_subnet, retrieval_threshold)
            self._check_relation_in_objects_can_be_added(knowledge_subnet, retrieval_threshold)

    """
    Check if an object can be added based on the retrieval_threshold

    Parameters
    ------------
    param1: KnowledgeSubnet
        KnowledgeSubnet, to go through to add all activated objects
    param2: int
        Retrieval Threeshold, that decides whether nodes can be added to KnowledgeSubnet or not
    """
    def _check_objects_in_relations_can_be_added(self, knowledge_subnet, retrieval_threshold):
        self.receive_knowledge_fragments_in_progress = False
        for relation_type, stored_relations in knowledge_subnet.relations.items():
            for relation in stored_relations:
                for index, object_name in enumerate(relation.objects):
                    if relation.objects_received[index] == True:
                        object_to_add_eventually = self.stored_objects[object_name]
                        if (object_to_add_eventually.activation + self.EPSILON >= retrieval_threshold):
                            self._add_object_to_knowledge_subnet(object_to_add_eventually, knowledge_subnet, (relation_type, stored_relations.index(relation)))
                        else:
                            relation.objects_received[index] = False

    """
    Add object to knowledge subnet

    Parameters
    ------------
    param1: object
        object that will be added to  knowledge subnet if it not yet is in the subnet
    param1: knowledge
        KnowledgeSubnet, to which the object will be added if it is not yet in it
    param2: tuple of (relation_category, relation_reference_number)
        relation_link that will be added to the object in order to know to which relation in the subnet it is linked
    """
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

    """
    Check if an relation can be added based on the retrieval_threshold

    Parameters
    ------------
    param1: KnowledgeSubnet
        KnowledgeSubnet, to go through to add all activated relations
    param2: int
        Retrieval Threeshold, that decides whether nodes can be added to KnowledgeSubnet or not
    """
    def _check_relation_in_objects_can_be_added(self, knowledge_subnet, retrieval_threshold):
        self.receive_knowledge_fragments_in_progress = False
        for object_name in knowledge_subnet.objects.keys():
            for relation_link in self.stored_objects[object_name].relation_links:
                relation_to_add_eventually = self.stored_relations[relation_link[0]][relation_link[1]]
                if(relation_to_add_eventually.activation + self.EPSILON >= retrieval_threshold):
                    self._add_relations_to_knowledge_subnet(relation_to_add_eventually, knowledge_subnet)

    """
    Add relation to knowledge subnet

    Parameters
    ------------
    param1: relation
        relation that will be added to knowledge subnet if it not yet is in the subnet
    param1: knowledge
        KnowledgeSubnet, to which the relation will be added if it is not yet in it
    """
    def _add_relations_to_knowledge_subnet(self, relation_to_add, knowledge_subnet):
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

    """
    Get the most activated knowledge subnet

    Parameters
    ------------
    param1: List of knowledge subnets
        all knowledge subnets that will be compared and will be evaluated, based on the activation values
        of their members (relations and objects that each subnet contains)

    Returns
    ------------
    KnowledgeSubnet
        returns the most activated knowledge subnet
    """
    def get_most_activated_knowledge_subnet(self, knowledge_subnets):
        most_activated_knowledge_subnet_average_activation_value = 0
        most_activated_knowledge_subnet = None
        for knowledge_subnet in knowledge_subnets:
            average_activation_value = knowledge_subnet.activation_value / knowledge_subnet.amount_of_activated_nodes
            if(average_activation_value > most_activated_knowledge_subnet_average_activation_value):
                most_activated_knowledge_subnet = knowledge_subnet
                most_activated_knowledge_subnet_average_activation_value = average_activation_value
        self.logger.info('Found most activated knowledge subnets')
        return most_activated_knowledge_subnet
    

    """
    Add usage for all nodes in the most activated knowledge subnet
    (If a node was received by an LTM call it will add this time to its usages array)

    Parameters
    ------------
    param1: KnowledgeSubnet
        Relations and Objects stored in the KnowledgeSubnet will get an new entry
        in their usages list
    """
    def add_usage_for_activated_knowledge_fragments(self, knowledge_subnet):
        if not knowledge_subnet:
            return
        for relations in knowledge_subnet.relations.values():
            for relation in relations:
                relation.usages.append(self.time_since_initialization)           
        for object_name in knowledge_subnet.objects.keys():
            self.stored_objects[object_name].usages.append(self.time_since_initialization)

    """
    Mark all nodes in knowledge_subnets as recieved

    Parameters
    ------------
    param1: KnowledgeSubnet
        KnowldegeSubnet, for which all objects and relations will be set as received
    """
    def mark_received_nodes_for_activated_knowledge_fragment(self, knowledge_subnet):
        if not knowledge_subnet:
            return
        for relations in knowledge_subnet.relations.values():
            for relation in relations:
                relation.is_received = True        
        for object_name in knowledge_subnet.objects.keys():
            self.stored_objects[object_name].is_received = True

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
        self.objects_received = [True for concrete_object in objects]
        self.time_of_creation = time_of_creation
        self.amount_of_usages = 1
        self.activation = 0
        self.activation_to_update = 0
        self.is_active = False
        self.usages = [time_of_creation]
        self.is_complete = None
        self.is_received = False

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
        self.is_received = False

