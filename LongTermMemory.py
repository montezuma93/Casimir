from collections import OrderedDict

class LongTermMemory:

    def __init__(self):
        self.stored_relations = OrderedDict()
        self.stored_objects = OrderedDict()

    def save_relation_object_mapping(self, relation_to_objects_mapping):
        self._save_relation(relation_to_objects_mapping)
        self._save_object(relation_to_objects_mapping)
   
    def _save_relation(self, relation_to_objects_mapping):
        if (self.stored_relations.__contains__(relation_to_objects_mapping.relation.relation_type)):
            self.stored_relations.get(relation_to_objects_mapping.relation.relation_type).append(relation_to_objects_mapping)
        else:
            self.stored_relations[relation_to_objects_mapping.relation.relation_type] = [relation_to_objects_mapping]

    def _save_object(self, relation_to_objects_mapping):
        relation_reference_number = len(self.stored_relations[relation_to_objects_mapping.relation.relation_type]) -1
        relation_type = relation_to_objects_mapping.relation.relation_type
        for concrete_object in relation_to_objects_mapping.object_list:
            object_to_store = ObjectToRelationMapping(concrete_object, relation_type, relation_reference_number)
            if (self.stored_objects.__contains__(concrete_object.name)):
                self.stored_objects[concrete_object.name].append(object_to_store)
            else:
                self.stored_objects[concrete_object.name] = [object_to_store]

    def receive_knowledge_fragments(self, relation_category, object1, object2):
        attention_rate = 1
        threshold = 0.5
        while(attention_rate > threshold):
            self.stored_relations[relation_category.category_name]

class RelationToObjectsMapping:
    def __init__(self, relation, object_list):
        self.relation = relation
        self.object_list = object_list

class ObjectToRelationMapping:
    def __init__(self, stored_object, relation_type, relation_reference_number):
        self.stored_object = stored_object
        self.relation_type = relation_type
        self.reference_number = relation_reference_number