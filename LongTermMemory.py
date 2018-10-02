from collections import OrderedDict

class LongTermMemory:

    def __init__(self):
        self.stored_relations = OrderedDict()

    def save(self, relation_object):
        if (self.stored_relations.__contains__(relation_object.relation.category_name)):
            self.stored_relations.get(relation_object.relation.category_name).append(relation_object)
        else:
            self.stored_relations[relation_object.relation.category_name] = [relation_object]


