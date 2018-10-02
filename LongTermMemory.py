from collections import OrderedDict
from Relation import RelationCategory, RelationObject

class LongTermMemory:

    def __init__(self):
        self.storedRelations = OrderedDict()

    def save(self, relationObject):
        if (self.storedRelations.__contains__(relationObject.relation.category_name)):
            self.storedRelations.get(relationObject.relation.category_name).append(relationObject)
        else:
            self.storedRelations[relationObject.relation.category_name] = [relationObject]


