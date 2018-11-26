from Relation import *
import csv
import requests
import json

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
            clean_smm = clean_empty(smm)
            keys = list(clean_smm)
            keys.remove('middle')
            smm_string = keys[0] + " " + clean_smm[keys[0]] + " " + clean_smm['middle']
            smm_string_list.append(smm_string)
            print(smm_string, "\n")


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
        