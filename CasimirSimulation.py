from LongTermMemoryController import LongTermMemoryController
from LongTermMemoryService import StoredObject
from WorkingMemoryController import WorkingMemoryController
from Object import CityObject, CountryObject, ContinentObject, ObjectType
from Object import  MiscellaneousObject
import json
from Relation import *
from flask import Flask, request, json, jsonify
from flask_restplus import Resource, Api, reqparse, Swagger,fields

app = Flask(__name__)
class CasimirSimulation(Resource):

    MAX_AMOUNT_OF_RETRIES = 3

    """
    Initialize Casimir Simulation, with LongTermMemory and WorkingMemory
    Parameters
    """  
    def __init__(self, app):   

        self.long_term_memory_controller = LongTermMemoryController()
        self.working_memory_controller = WorkingMemoryController()

    """
    Update setting used in LTM and WM
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
    param9 : boolean
        false if complete and incomplete knowledge_fragments can be received, false otherwise
    """
    def update_settings(self, base_activation_decay, fraction_of_activation, initial_activation_value, noise,
         dynamic_firing_threshold, firing_threshold, noise_on, spread_full_activation, use_only_complete_fragments, max_amount_of_retries):
        self.MAX_AMOUNT_OF_RETRIES = max_amount_of_retries
        self.long_term_memory_controller.update_settings(base_activation_decay, fraction_of_activation, initial_activation_value, noise,
         dynamic_firing_threshold, firing_threshold, noise_on, spread_full_activation)
        self.working_memory_controller.update_settings(use_only_complete_fragments)

    """
    Reset simulation, clearing LongTermMemory and WorkingMemory
    """
    def reset_simulation(self):
        self.working_memory_controller.reset_simulation()
        self.long_term_memory_controller.reset_simulation()

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
        self.long_term_memory_controller.save_knowledge_fragment(relation, objects)
    
    """
    Create Spatial Mental Images and checks whether all from the contex wanted data, was received.
    If not try again, with a new call to the LTM

    Parameters
    ----------
    param1 : Array of Relations and Objects
        Relation and Objects which should get received from LTM and create Spatial Mental Images

    Returns
    --------
    SpatialMentalImages
        Array of Json Formatted Spatial Mental Images
    """
    def create_mental_image(self, context_array):
        object_to_receive_name_list = self._get_all_objects_names_in_context_array(context_array)
        knowledge_subnet = []
        received_object_list = []
        context_added = True
        retries = 0
        while(not self._received_all_necessary_nodes(object_to_receive_name_list, knowledge_subnet) and (context_added or retries < self.MAX_AMOUNT_OF_RETRIES )):
            retries = retries + 1
            context_added = False
            knowledge_subnet = self.long_term_memory_controller.receive_knowledge_fragments(context_array)
            for object_name, concrete_object in knowledge_subnet.objects.items():
                if (not received_object_list.__contains__(object_name)):
                    context_added = True
                    received_object_list.append(object_name)
                    context_array.append(cast_object(concrete_object.stored_object.object_type.value, object_name))
        return self.working_memory_controller.construction(knowledge_subnet, context_array)

    """
    Get all objects from context_array and returns them in an array

    Parameters
    ----------
    param1 : Array of Relations and Objects
        Relation and Objects

    Returns
    --------
    List
        List of the names of all objects in context array
    """
    def _get_all_objects_names_in_context_array(self, context_array):
        object_name_list = []
        for node in context_array:
            if type(node) is CityObject or type(node) is CountryObject or type(node) is ContinentObject or type(node) is MiscellaneousObject:
                object_name_list.append(node.name)
        return object_name_list

    """
    Checks if all data, was received based on the context array

    Parameters
    ----------
    param1 : Array of Relations and Objects
        Relation and Objects which should get received from LTM
    param2 : KnowledgeSubnet
        The knowledge subnet received from the LTM

    Returns
    --------
    boolean
        True if all nodes were received, false otherwise
    """
    def _received_all_necessary_nodes(self, object_names_to_receive, knowledge_subnet):
        if knowledge_subnet:
            for object_name in object_names_to_receive:
                if not knowledge_subnet.objects.__contains__(object_name):
                    return False
            return True
        else:
            return False

@app.route("/save_knowledge_fragment", methods=['POST'])
def save_knowledge_fragment():     
    req_data = request.get_json()
    relation = req_data['relation']
    objects = req_data['objects']
    casted_relation = cast_relation(relation)
    casted_objects = []
    for concrete_object in objects:
        casted_objects.append(cast_object(concrete_object["type"], concrete_object["name"]))

    casimirSimulation.save_knowledge_fragment(casted_relation, casted_objects)
    return 'saved'

@app.route("/reset_simulation", methods=['POST'])
def reset_simulation():
    casimirSimulation.reset_simulation()
    return 'Simulation reseted'

@app.route("/create_mental_image" , methods=['PUT'])
def create_mental_image():
    req_data = request.get_json()
    base_activation_decay = float(req_data['base_activation_decay'])
    fraction_of_activation = float(req_data['fraction_of_activation'])
    initial_activation_value = float(req_data['initial_activation_value'])
    noise = float(req_data['noise'])
    dynamic_firing_threshold = req_data['dynamic_firing_threshold']
    firing_threshold = float(req_data['firing_threshold'])
    noise_on = req_data['noise_on']
    spread_full_activation = req_data['spread_full_activation']
    use_only_complete_fragments = req_data['use_only_complete_fragments']
    max_amount_of_retries = req_data['max_amount_of_retries']

    casimirSimulation.update_settings(base_activation_decay, fraction_of_activation, initial_activation_value, noise,
     dynamic_firing_threshold, firing_threshold, noise_on, spread_full_activation, use_only_complete_fragments, max_amount_of_retries)

    context_array = req_data['context']
    casted_context_array = []
    for context in context_array:
        if context["category"] == "RelationCategory":
            casted_context_array.append(cast_relation_category(context["type"]))
        elif context["category"] == "Object":
            casted_context_array.append(cast_object(context["type"], context["name"]))
    mental_image = casimirSimulation.create_mental_image(casted_context_array)
    return jsonify(mental_image)

def cast_relation(relation):
    dictionary = {'North':NorthCardinalRelation(), 'South':SouthCardinalRelation(), 'West':WestCardinalRelation(), 'East': EastCardinalRelation(),
        "PartOf": PartOfTopologicalRelation(), 'NorthEast': NorthEastCardinalRelation(), 'NorthWest': NorthWestCardinalRelation(), 
        'SouthEast': SouthEastCardinalRelation(), 'SouthWest': SouthWestCardinalRelation(), 'Far': FarDistanceRelation(), 'Close': CloseDistanceRelation()}
    return dictionary.get(relation,'Relation Not Found')

def cast_relation_category(relation_category):
    dictionary = {'Cardinal':RelationType.CardinalRelation, 'Topological':RelationType.TopologicalRelation, 'Distance':RelationType.DistanceRelation}
    return dictionary.get(relation_category,'Relation Category Not Found')

def cast_object(object_type, name):
    if object_type == "City":
        return CityObject(name)
    elif object_type == "Country":
        return CountryObject(name)
    elif object_type == "Continent":
        return ContinentObject(name)
    elif object_type == "Miscellaneous":
        return MiscellaneousObject(name)

casimirSimulation = CasimirSimulation(app)

if __name__ == '__main__':
    app.run()
