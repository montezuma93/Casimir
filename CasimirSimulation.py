from LongTermMemoryController import LongTermMemoryController
import json
from Relation import *
from Object import CityObject, ObjectType, CountryObject, ContinentObject
from flask import Flask, request, json, jsonify
from flask_restplus import Resource, Api, reqparse, Swagger,fields

app = Flask(__name__)
api = Api(app)

class CasimirSimulation(Resource):

    def __init__(self, app):
        self.long_term_memory_controller = LongTermMemoryController()

    def post(self):
        print("here")
        
        req_data = request.get_json()
        relation = req_data['relation']
        casted_relation = self.cast_relation(relation)
        casted_objects = []
        objects = req_data['objects']
        for concrete_object in objects:
            casted_objects.append(self.cast_object(concrete_object["type"], concrete_object["name"]))
        casimirSimulation.long_term_memory_controller.save_knowledge_fragment(casted_relation, casted_objects)

    def put(self):
        print("lala")
        req_data = request.get_json()
        casted_context_array = []
        context_array = req_data['context']
        for context in context_array:
            if context["category"] == "RelationCategory":
                casted_context_array.append(self.cast_relation_category(context["type"]))
            elif context["category"] == "Object":
                casted_context_array.append(self.cast_object(context["type"], context["name"]))
        knowledge_fragements = casimirSimulation.long_term_memory_controller.receive_knowledge_fragments(casted_context_array)
        print(len(knowledge_fragements.relations))
        return knowledge_fragements.toJson()

    def cast_relation(self, relation):
        dictionary = {'North':NorthCardinalRelation(), 'South':SouthCardinalRelation(), 'West':WestCardinalRelation(), 'East': EastCardinalRelation(),
         "PartOf": PartOfTopologicalRelation()}
        return dictionary.get(relation,'Not Found')
    
    def cast_relation_category(self, relation_category):
        dictionary = {'Cardinal':RelationType.CardinalRelation, 'Topological':RelationType.TopologicalRelation, 'Distance':RelationType.DistanceRelation}
        return dictionary.get(relation_category,'Not Found')
    
    def cast_object(self, object_type, name):
        if object_type == "City":
            return self.create_city(name)
        elif object_type == "Country":
            return self.create_country(name)
        elif object_type == "Continent":
            return self.create_continent(name)

    def create_city(self, name):
        return CityObject(name)
    
    def create_country(self, name):
        return CountryObject(name)

    def create_continent(self, name):
        return ContinentObject(name)
        
casimirSimulation = CasimirSimulation(app)

api.add_resource(CasimirSimulation, "/")

if __name__ == '__main__':
    app.run()
