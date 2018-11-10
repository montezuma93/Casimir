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

    def create_smm(self, knowledge_fragements):
        return casimirSimulation.working_memory_controller.create_smm(knowledge_fragements)

  
        
casimirSimulation = CasimirSimulation(app)

@app.route("/post", methods=['POST'])
def post():      
    req_data = request.get_json()
    relation = req_data['relation']
    casted_relation = cast_relation(relation)
    casted_objects = []
    objects = req_data['objects']
    for concrete_object in objects:
        casted_objects.append(cast_object(concrete_object["type"], concrete_object["name"]))
    casimirSimulation.long_term_memory_controller.save_knowledge_fragment(casted_relation, casted_objects)
    return 'saved'

@app.route("/get", methods=['GET'])
def get():
    print("getall")
    all_fragments = casimirSimulation.long_term_memory_controller.show_all_knowledge_fragments()
    return jsonify(all_fragments)

@app.route("/put" , methods=['PUT'])   
def put():
    req_data = request.get_json()
    casted_context_array = []
    context_array = req_data['context']
    for context in context_array:
        if context["category"] == "RelationCategory":
            casted_context_array.append(cast_relation_category(context["type"]))
        elif context["category"] == "Object":
            casted_context_array.append(cast_object(context["type"], context["name"]))
    knowledge_fragements = casimirSimulation.long_term_memory_controller.receive_knowledge_fragments(casted_context_array)

    smm = casimirSimulation.create_smm(knowledge_fragements)
    return jsonify(smm)
    #return knowledge_fragements.toJson()

def cast_relation(relation):
    dictionary = {'North':NorthCardinalRelation(), 'South':SouthCardinalRelation(), 'West':WestCardinalRelation(), 'East': EastCardinalRelation(),
        "PartOf": PartOfTopologicalRelation()}
    return dictionary.get(relation,'Not Found')

def cast_relation_category(relation_category):
    dictionary = {'Cardinal':RelationType.CardinalRelation, 'Topological':RelationType.TopologicalRelation, 'Distance':RelationType.DistanceRelation}
    return dictionary.get(relation_category,'Not Found')

def cast_object(object_type, name):
    if object_type == "City":
        return create_city(name)
    elif object_type == "Country":
        return create_country(name)
    elif object_type == "Continent":
        return create_continent(name)

def create_city(name):
    return CityObject(name)

def create_country(name):
    return CountryObject(name)

def create_continent(name):
    return ContinentObject(name)

if __name__ == '__main__':
    app.run()
