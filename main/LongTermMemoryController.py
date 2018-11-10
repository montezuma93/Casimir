from LongTermMemoryService import LongTermMemoryService

class LongTermMemoryController:

    def __init__(self):
        self.long_term_memory_service = LongTermMemoryService()
    
    def save_knowledge_fragment(self, relation, objects):
        self.long_term_memory_service.save_knowledge_fragment(relation, objects)

    def receive_knowledge_fragments(self, context_array):
        return self.long_term_memory_service.receive_knowledge_fragments(context_array)

    def show_all_knowledge_fragments(self):
        return self.long_term_memory_service.show_all_knowledge_fragments()
