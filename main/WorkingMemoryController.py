from WorkingMemoryService import WorkingMemoryService

class WorkingMemoryController:

    def __init__(self):
        self.working_memory_service = WorkingMemoryService()

    def create_smm(self, knowledge_fragments):
        return self.working_memory_service.create_smm(knowledge_fragments)


