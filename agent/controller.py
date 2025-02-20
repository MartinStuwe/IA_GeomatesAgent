from agent.util import *
from agent.localize import SelfLocalizer

class AgentController:

    def __init__(self, world_connector):
        self.agent_type = AgentType.UNKNOWN
        self.wc = world_connector
        self.localizer = SelfLocalizer(self.wc)



    def handle_world(self, world_desc):
        if self.agent_type == AgentType.UNKNOWN:
            new_key = self.localizer.handle_world(world_desc)
            if self.localizer.has_determined():
                self.agent_type = self.localizer.get_type()
                print(f"determined {self.agent_type}")
            return new_key
        else:
            return NO_ACT_KEY
            