from WorkingMemoryService import WorkingMemoryService

class WorkingMemoryController:

    def __init__(self):
        self.working_memory_service = WorkingMemoryService()

    def create_smm(self, knowledge_fragments, context_array):
        return self.working_memory_service.create_smm(knowledge_fragments)



