from WorkingMemoryService import WorkingMemoryService

class WorkingMemoryController:

    def __init__(self):
        self.working_memory_service = WorkingMemoryService()

    def reset_simulation(self):
        self.working_memory_service.reset_simulation()

    def update_settings(self, use_only_complete_fragments):
        self.working_memory_service.update_settings(use_only_complete_fragments)

    def construction(self, knowledge_fragments, context_array):
        return self.working_memory_service.construction(knowledge_fragments)



