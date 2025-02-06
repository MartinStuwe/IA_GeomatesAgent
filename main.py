
import agent.world as world
import os
from agent.util import AgentType, NO_ACT_KEY
from agent.telnet import TelnetClient

class GeomatesAgent:
    def __init__(self):
        self.world_connector = world.WorldConnector()
        self.agent_type = AgentType.UNKNOWN

    def handle_message(self, message):
        """Handles a message by forwarding it to WorldConnector."""
        self.world_connector.handle_world_msg(message)
        self.agent_type = self.world_connector.agent_type
        
        if self.agent_type is not AgentType.UNKNOWN:
            pass


if __name__ == "__main__":
    client = TelnetClient("localhost", 45678)
    agent = GeomatesAgent()
    client.connect()
    try:
        client.send(NO_ACT_KEY)
        while True:
            received_msg = client.receive()
            if received_msg:
                response = agent.handle_message(received_msg)
                client.send(response)
    finally:
        client.close()