from LongTermMemoryService import LongTermMemoryService

class LongTermMemoryController:

    def __init__(self):
        self.long_term_memory_service = LongTermMemoryService()

    def reset_simulation(self):
        self.long_term_memory_service.reset_simulation()

    def update_settings(self, base_activation_decay, fraction_of_activation, initial_activation_value, noise,
     dynamic_firing_threshold, firing_threshold, noise_on, spread_full_activation):
        self.long_term_memory_service.update_settings(base_activation_decay, fraction_of_activation, initial_activation_value, noise,
         dynamic_firing_threshold, firing_threshold, noise_on, spread_full_activation)
        
    def save_knowledge_fragment(self, relation, objects):
        self.long_term_memory_service.save_knowledge_fragment(relation, objects)

    def receive_knowledge_fragments(self, context_array):
        return self.long_term_memory_service.receive_knowledge_fragments(context_array)
