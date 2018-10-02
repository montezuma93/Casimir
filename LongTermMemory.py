from collections import OrderedDict

class LongTermMemory:

    def __init__(self):
        self.stored_relations = OrderedDict()
        self.stored_objects = OrderedDict()

    def save_object_relation(self, relation_object):
        self._save_relation(relation_object)
        self._save_object(relation_object)
   
    def _save_relation(self, relation_object):
        if (self.stored_relations.__contains__(relation_object.relation.category_name)):
            self.stored_relations.get(relation_object.relation.category_name).append(relation_object)
        else:
            self.stored_relations[relation_object.relation.category_name] = [relation_object]

    def _save_object(self, relation_object):
        reference_number = len(self.stored_relations[relation_object.relation.category_name]) -1
        relation_category = relation_object.relation.category_name
        for concrete_object in relation_object.object_list:
            object_to_store = StoredObject(relation_category, reference_number)
            if (self.stored_objects.__contains__(concrete_object.name)):
                self.stored_objects[concrete_object.name].append(object_to_store)
            else:
                self.stored_objects[concrete_object.name] = [object_to_store]

    def receive_knowledge_fragments(self, relation_category, object1, object2):
        attention_rate = 1
        threshold = 0.5
        while(attention_rate > threshold):
            self.stored_relations[relation_category.category_name]



class StoredRelation:
    def __init__(self, relation, object_list):
        self.relation = relation
        self.object_list = object_list

class StoredObject:
    def __init__(self, relation_category, reference_number):
        self.relation_category = relation_category
        self.reference_number = reference_number