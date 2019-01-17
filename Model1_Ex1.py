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

def clean_empty(d):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (clean_empty(v) for v in d) if v]
    return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v}

def cast_relation(relation):
    dictionary = {'north': 'North', 'south':'South', 'west': 'West', 'east': 'East' ,
    'north-east': 'NorthEast', 'north-west': 'NorthWest', 'south-east': 'SouthEast', 'south-west': 'SouthWest'}
    return dictionary.get(relation,'Relation Not Found')

def get_opposite(relation):
    dictionary = {'north': 'south', 'south':'north', 'west': 'east', 'east': 'west' ,
    'north-east': 'south-west', 'north-west': 'south-east', 'south-east': 'north-west', 'south-west': 'north-east'}
    return dictionary.get(relation,'Relation Not Found')

def get_relation(relation_key1, relation_key2):
    key1 = relation_key1.replace('outer-', '')
    key2 = relation_key2.replace('outer-', '')
    if(key1 == key2):
        if 'outer' in relation_key1:
            return relation_key1.replace('outer-', '')
        else:
            return get_opposite(relation_key2.replace('outer-', ''))

    key = key1 + " " + key2
    dictionary = {'north south': 'north', 'north west': 'north-west', 'north east': 'north-east', 'north middle': 'north',
    'north north-east': 'west', 'north north-west': 'east', 'north south-east': 'north', 'north south-west': 'north',

    'south north':'south', 'south west': 'south-east', 'south east': 'south-east', 'south middle': 'south',
    'south south-east': 'west', 'south south-west': 'east', 'south north-east': 'south', 'south north-west': 'south',

    'east west': 'east', 'east north': 'south-east', 'east south': 'north-east', 'east middle': 'east',
    'east north-east': 'south', 'east south-east': 'north', 'east north-west': 'east', 'east south-west': 'east',

    'west east': 'west', 'west north': 'south-west', 'west south': 'north-west', 'west middle': 'west',
    'west north-west': 'south', 'west south-west': 'north', 'west north-east': 'west', 'west south-east': 'west',

    'north-east south-west': 'north-east', 'north-east north-west': 'east', 'north-east south-east': 'north',
    'north-east middle': 'north-east', 'north-east north': 'east', 'north-east east': 'north', 'north-east west': 'east', 'north-east south': 'north',

    'north-west south-west': 'north', 'north-west north-east': 'west', 'north-west south-east': 'north-west',
    'north-west middle': 'north-west', 'north-west north': 'west', 'north-west west':'north', 'north-west east': 'west', 'north-west south': 'north',
    
    'south-west north-west': 'south', 'south-west north-east': 'south-west', 'south-west south-east': 'west',
    'south-west middle': 'south-west', 'south-west south': 'west', 'south-west west': 'south', 'south-west north': 'south', 'south-west east': 'west',

    'south-east north-west': 'south-east', 'south-east north-east': 'south', 'south-east south-west': 'east',
    'south-east middle': 'south-east', 'south-east south': 'east', 'south-east east': 'south', 'south-east north': 'south', 'south-east west': 'east',

    'middle north': 'south', 'middle south': 'north', 'middle west': 'east', 'middle east': 'west',
    'middle north-west': 'south-east', 'middle north-east': 'south-west', 'middle south-west': 'north-east', 'middle south-east': 'north-west',
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
        relation = None
        
        fragment_to_save_data = {
            "relation": cast_relation(relation_in_fragment),
            "objects": [object1_in_fragment, object2_in_fragment]
        }
        fragment_to_save_json = json.dumps(fragment_to_save_data)

        response_of_call = requests.post(save_url, data=fragment_to_save_json, headers={"Content-Type": "application/json"})

        #print("save_fragment", fragment_to_save_json, "\n")
    
    context_object1 = choices[0][0][1]
    context_object2 = choices[0][0][2]
    #print("question is: ", context_object1, context_object2, "\n")
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
            'base_activation_decay': -0.5,
            'fraction_of_activation': 0.6,
            'initial_activation_value': 1,
            'noise': 0.1,
            'dynamic_firing_threshold': True,
            'firing_threshold': 0.01667,
            'noise_on': False,
            'spread_full_activation': False,
            'use_only_complete_fragments': False,
            'max_amount_of_retries': 3
        }
    question_json = json.dumps(question_data)
    
    response_of_receive_call = requests.put(receive_url, data=question_json, headers={"Content-Type": "application/json", "Accept": "application/json"})
    response_in_json = response_of_receive_call.json()
    smm_list = response_in_json['smm']

    print("simulation answer", "\n")
    smm_string_list = []
    for smm in smm_list:
        print(smm, "\n")
        get_relations_out_of_smm(smm, smm_string_list)

    simulation_response_of_task = ""
    for smm_string_in_list in smm_string_list:
        #print(smm_string_in_list)
        if smm_string_in_list[1] == context_object1 and smm_string_in_list[2] == context_object2:
            simulation_response_of_task = [smm_string_in_list]

    #print("Last answer")
    #print(simulation_response_of_task[0][0])
    #print(simulation_response_of_task[0][1])
    #print(simulation_response_of_task[0][2])
    #print("reset simulation -> next task", "\n")
    response_of_reset_call = requests.post(reset_url)
    print(simulation_response_of_task)
    return(simulation_response_of_task)



'''
Prefers perfect traingles as well as main cardinal directions
'''
class Model1(ccobra.CCobraModel):

    def __init__(self, name='Model1'):
        super(Model1, self).__init__(name, ['relational'], ['verify', 'single_choice'])

    def predict(self, item, **kwargs):
        #print("task")
        return run(item)