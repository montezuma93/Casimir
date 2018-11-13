from WorkingMemoryService import WorkingMemoryService

class WorkingMemoryController:

    def __init__(self):
        self.working_memory_service = WorkingMemoryService()

    def construction(self, knowledge_fragments, context_array):
        return self.working_memory_service.construction(knowledge_fragments)



