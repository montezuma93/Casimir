from Relation import *
import csv
import requests
import json
import ccobra

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
    'north-west middle': 'north-west', 'north-west north': 'west', 'north-west west':'north', 'north-west east': 'west', 'north-west south': 'south',
    
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
                    smm_string = smm_relation + " " + smm[key1] + " " + smm[key2]
                    if not smm_string_list.__contains__(smm_string):
                        print(smm_string)
                        smm_string_list.append(smm_string)
    return smm_string_list  


with open('spatial1_cobra.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    counter = 0
    for row in reader:
        iD = row['id']
        task = row['task']
        question = row['question']
        response = row['response']
        fragments_to_save  = task.split('/')
        print(reader.line_num)
        for fragment_to_save in fragments_to_save:
            array_in_fragment = fragment_to_save.split(';')
            relation_in_fragment =array_in_fragment[0]
            object1_in_fragment = {"name": array_in_fragment[1], "type": "City" }
            object2_in_fragment = {"name": array_in_fragment[2], "type": "City" }
            relation = None
            
            fragment_to_save_data = {
                "relation": cast_relation(relation_in_fragment),
                "objects": [object1_in_fragment, object2_in_fragment]
            }
            fragment_to_save_json = json.dumps(fragment_to_save_data)

            response_of_call = requests.post(save_url, data=fragment_to_save_json, headers={"Content-Type": "application/json"})

            print("save_fragment", fragment_to_save_json, "\n")
        
        question_to_ask = question.split()
        context_object1 = question_to_ask[1]
        context_object2 = question_to_ask[6]
        context_object2 = context_object2.replace(".", "")
        print("question is: ", context_object1, context_object2, "\n")
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
                ]
            }
        question_json = json.dumps(question_data)

        response_of_receive_call = requests.put(receive_url, data=question_json, headers={"Content-Type": "application/json", "Accept": "application/json"})
        response_in_json = response_of_receive_call.json()
        smm_list = response_in_json['smm']
        print("simulation answer", "\n")
        smm_string_list = []
        for smm in smm_list:
            print(smm, "\n")
            list_to_add = get_relations_out_of_smm(smm, smm_string_list)


        response_array = response.split(";")
        relation_in_answer = response_array[0]
        object1_in_answer = response_array[1]
        object2_in_answer = response_array[2]
        response_string = relation_in_answer + " " + object1_in_answer + " " + object2_in_answer
        print("experiment answer", "\n")
        print(response_string, "\n")

    
        for smm_string_in_list in smm_string_list:
            if smm_string_in_list == response_string:
                print("Answer was found by simulation", "\n")
                counter = counter + 1

        print("reset simulation -> next task", "\n")
        response_of_reset_call = requests.post(reset_url)

    print("# right answers", counter, "\n")
        