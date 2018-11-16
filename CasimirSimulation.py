from LongTermMemoryController import LongTermMemoryController
from WorkingMemoryController import WorkingMemoryController
import json
from Relation import *
from Object import CityObject, ObjectType, CountryObject, ContinentObject
from flask import Flask, request, json, jsonify
from flask_restplus import Resource, Api, reqparse, Swagger,fields

app = Flask(__name__)
class CasimirSimulation(Resource):

    def __init__(self, app):
        self.long_term_memory_controller = LongTermMemoryController()
        self.working_memory_controller = WorkingMemoryController()

    def save_knowledge_fragment(self, relation, objects):
        self.long_term_memory_controller.save_knowledge_fragment(relation, objects)

    def show_all_knowledge_fragments(self):
        return self.long_term_memory_controller.show_all_knowledge_fragments()

    def create_mental_image(self, context_array):
        knowledge_subnet = self.long_term_memory_controller.receive_knowledge_fragments(context_array)
        return self.working_memory_controller.construction(knowledge_subnet, context_array)

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

@app.route("/show_all_knowledge_fragments", methods=['GET'])
def show_all_knowledge_fragments():
    all_fragments = casimirSimulation.long_term_memory_controller.show_all_knowledge_fragments()
    return jsonify(all_fragments)

@app.route("/create_mental_image" , methods=['PUT'])   
def create_mental_image():
    req_data = request.get_json()
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

casimirSimulation = CasimirSimulation(app)

if __name__ == '__main__':
    app.run()
