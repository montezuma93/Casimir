from Relation import *
import csv
import requests
import json
import ccobra
import numpy as np

save_url = 'http://localhost:5000/save_knowledge_fragment'
receive_url = 'http://localhost:5000/create_mental_image'
reset_url = 'http://localhost:5000/reset_simulation'
update_settings_url = 'http://localhost:5000/update_settings'

def cast_relation(relation):
    dictionary = {'north': 'North', 'south':'South', 'west': 'West', 'east': 'East' ,
    'north-east': 'NorthEast', 'north-west': 'NorthWest', 'south-east': 'SouthEast', 'south-west': 'SouthWest'}
    return dictionary.get(relation,'Relation Not Found')

def cast_relation_back(relation):
    dictionary = {'northEast': 'north-east', 'northWest': 'north-west', 'southEast': 'south-east', 'southWest': 'south-west',
    'south': 'south', 'north': 'north', 'west': 'west', 'east': 'east'}
    return dictionary.get(relation,'')

def get_opposite(relation):
    dictionary = {'north': 'south', 'south':'north', 'west': 'east', 'east': 'west' ,
    'northEast': 'south-west', 'northWest': 'south-east', 'southEast': 'north-west', 'southWest': 'north-east'}
    return dictionary.get(relation,'Relation Not Found')

def get_relation(relation_key1, relation_key2):
    key1 = relation_key1.replace('outer_', '')
    key2 = relation_key2.replace('outer_', '')
    if(key1 == key2):
        if 'outer' in relation_key1:
            relation = cast_relation_back(key1)
            return relation
        else:
            return get_opposite(key2)
    key = key1 + " " + key2
    dictionary = {'north south': 'north', 'north west': 'north-east', 'north east': 'north-west', 'north middle': 'north',
    'north northEast': 'south-west', 'north northWest': 'south-east', 'north southEast': 'north', 'north southWest': 'north',

    'south north':'south', 'south west': 'south-east', 'south east': 'south-west', 'south middle': 'south',
    'south southEast': 'north-west', 'south southWest': 'north-east', 'south northEast': 'south', 'south northWest': 'south',

    'east west': 'east', 'east north': 'south-east', 'east south': 'north-east', 'east middle': 'east',
    'east northEast': 'south-west', 'east southEast': 'north-west', 'east northWest': 'east', 'east southWest': 'east',

    'west east': 'west', 'west north': 'south-west', 'west south': 'north-west', 'west middle': 'west',
    'west northWest': 'south-east', 'west southWest': 'north-east', 'west northEast': 'west', 'west southEast': 'west',

    'northEast southWest': 'north-east', 'northEast northWest': 'east', 'northEast southEast': 'north',
    'northEast middle': 'north-east', 'northEast north': 'north-east', 'northEast east': 'north-east', 'northEast west': 'east', 'northEast south': 'north',

    'northWest southWest': 'north', 'northWest northEast': 'west', 'northWest southEast': 'north-west',
    'northWest middle': 'north-west', 'northWest north': 'north-west', 'northWest west':'north-west', 'northWest east': 'west', 'northWest south': 'north',
    
    'southWest northWest': 'south', 'southWest northEast': 'south-west', 'southWest southEast': 'west',
    'southWest middle': 'south-west', 'southWest south': 'south-west', 'southWest west': 'south-west', 'southWest north': 'south', 'southWest east': 'west',

    'southEast northWest': 'south-east', 'southEast northEast': 'south', 'southEast southWest': 'east',
    'southEast middle': 'south-east', 'southEast south': 'south-east', 'southEast east': 'south-east', 'southEast north': 'south', 'southEast west': 'east',

    'middle north': 'south', 'middle south': 'north', 'middle west': 'east', 'middle east': 'west',
    'middle northWest': 'south-east', 'middle northEast': 'south-west', 'middle southWest': 'north-east', 'middle southEast': 'north-west',
    }
    return dictionary.get(key,'')

def get_relations_out_of_smm(smm, smm_string_list):
    keys = list(smm)
    for key1 in keys:
        for key2 in keys:
            if key1 != key2 and smm[key1] != None and smm[key2] != None:
                smm_relation = get_relation(key1, key2)
                if smm_relation != '':
                    smm_string = [smm_relation, smm[key1], smm[key2]]
                    if not smm_string_list.__contains__(smm_string):
                        smm_string_list.append(smm_string)

def run(item):
    tasks = item.task
    choices = item.choices
    for fragment_to_save in tasks:
        relation_in_fragment = fragment_to_save[0]
        object1_in_fragment = {"name": fragment_to_save[1], "type": "City" }
        object2_in_fragment = {"name": fragment_to_save[2], "type": "City" }
        fragment_to_save_data = {
            "relation": cast_relation(relation_in_fragment),
            "objects": [object1_in_fragment, object2_in_fragment]
        }
        fragment_to_save_json = json.dumps(fragment_to_save_data)
        response_of_call = requests.post(save_url, data=fragment_to_save_json, headers={"Content-Type": "application/json"})

    context_object1 = choices[0][0][1]
    context_object2 = choices[0][0][2]
    context = []
    question_data = {
            "context" : [
                {"category": "Object",
                "name": context_object1,
                "type": "City"},
                {"category": "Object",
                "name": context_object2,
                "type": "City"},
                {"category": "RelationCategory",
                "type": "Cardinal"
                }
            ],
            'base_activation_decay': -0.86,
            'fraction_of_activation': 0.6,
            'initial_activation_value': 5,
            'noise': 0.1,
            'dynamic_firing_threshold': True,
            'firing_threshold': 0.01667,
            'noise_on': False,
            'spread_full_activation': True,
            'use_only_complete_fragments': False,
            'max_amount_of_retries': 3
        }
    question_json = json.dumps(question_data)
    
    response_of_receive_call = requests.put(receive_url, data=question_json, headers={"Content-Type": "application/json", "Accept": "application/json"})
    response_in_json = response_of_receive_call.json()

    smm_list = response_in_json['smm']
    smm_string_list = []
    for smm in smm_list:
        get_relations_out_of_smm(smm, smm_string_list)
    simulation_response_of_task = ""
    for smm_string_in_list in smm_string_list:
        if smm_string_in_list[1] == context_object1 and smm_string_in_list[2] == context_object2:
            simulation_response_of_task = [smm_string_in_list]
    response_of_reset_call = requests.post(reset_url)
    return simulation_response_of_task

'''
Prefers dull triangles (will place object close to the border) as well as main cardinal directions
'''
class Model5(ccobra.CCobraModel):

    def __init__(self, name='Model5'):
        super(Model5, self).__init__(name, ['relational'], ['verify', 'single_choice'])

    def predict(self, item, **kwargs):
        return run(item)