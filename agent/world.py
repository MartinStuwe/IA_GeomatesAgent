import re

from agent.util import AgentType
from agent.util import NO_ACT_KEY


class WorldConnector:
    def __init__(self):
        self.agent_type = AgentType.UNKNOWN
        self.world_parser = WorldParser()
        self.handler = None  # List to store handler functions

    def _check_for_agent_hint(self, msg):
        return ":playing" in msg
    
    def _parse_agent_hint(self, msg):
        if "disc" in msg.lower():
            self.agent_type = AgentType.DISC
        elif "rect" in msg.lower():
            self.agent_type = AgentType.RECT
        else:
            self.agent_type = AgentType.UNKNOWN
    
    def register_handler(self, handler):
        """Register a new handler function for world messages."""
        self.handler = handler

    def handle_world_msg(self, message):
        handler_return = None
        """Handles the world message and calls the appropriate handler functions."""
        if self.agent_type == AgentType.UNKNOWN and self._check_for_agent_hint(message):
            self._parse_agent_hint(message)
            print(f"I am a {self.agent_type}")
        else:
            self.world_parser.parse_description(message)
            if self.handler is not None:
                handler_return = self.handler(message) # Call the handler with the message
            else: 
                handler_return = NO_ACT_KEY
        return handler_return
    
    # Additional methods to retrieve world data
    def get_disc(self):
        return self.world_parser.disc
    
    def get_rect(self):
        return self.world_parser.rect
    
    def get_platforms(self):
        return self.world_parser.platforms
    
    def get_diamonds(self):
        return self.world_parser.diamonds
    
    def get_grid(self):
        return self.world_parser.render_world()
    




class WorldParser:
    def __init__(self, x_dim=80, y_dim=40):
        self.rect = None
        self.disc = None
        self.diamonds = []
        self.platforms = []

        self.x_dim = x_dim
        self.y_dim = y_dim
        
    
    def parse_description(self, description: str):
        self.rect = None
        self.disc = None
        self.diamonds = []
        self.platforms = []
        
        pattern = re.compile(r"\(:(\w+) ([0-9\.\- ]+)\)")
        matches = pattern.findall(description)
        
        for obj_type, values in matches:
            values = list(map(float, values.split()))
            
            if obj_type == "RECT":
                # Changed to use middle_x, middle_y, height, width
                self.rect = {
                    "middle_x": values[0], "middle_y": values[1], "width": values[2], "height": values[3], 
                    "rotation": values[4], "id": int(values[5])
                }
            elif obj_type == "DISC":
                self.disc = {"x": values[0], "y": values[1], "radius": values[2], "id": int(values[3])}
            elif obj_type == "DIAMOND":
                self.diamonds.append({"x": int(values[0]), "y": int(values[1])})
            elif obj_type == "PLATFORM":
                self.platforms.append({
                    "x_start": int(values[0]), "y_start": int(values[1]), "x_end": int(values[2]), "y_end": int(values[3])
                })
    
    def render_world(self, include_rect=True, include_disc=True):
        grid = [[' ' for _ in range(self.x_dim)] for _ in range(self.y_dim)]
        if self.rect and include_rect:
            # Adjust for new rectangle position based on middle_x, middle_y
            rect_left = self.rect["middle_x"] - self.rect["width"] / 2
            rect_top = self.rect["middle_y"] - self.rect["height"] / 2

            for i in range(round(rect_top), min(round(rect_top + self.rect["height"]), 40)):
                for j in range(round(rect_left), min(round(rect_left + self.rect["width"]), self.x_dim)):
                    grid[self.y_dim - 1 - i][j] = 'R'
        
        if self.disc and include_disc:
            for i in range(max(0, round(self.disc["y"] - self.disc["radius"])), min(40, round(self.disc["y"] + self.disc["radius"]) + 1)):
                for j in range(max(0, round(self.disc["x"] - self.disc["radius"])), min(80, round(self.disc["x"] + self.disc["radius"]) + 1)):
                    grid[self.y_dim -1 - i][j] = 'D'
        
        for i, diamond in enumerate(self.diamonds):
            if 0 <= diamond["y"] < 40 and 0 <= diamond["x"] < self.x_dim:
                grid[self.y_dim - 1 - diamond["y"]][diamond["x"]] = str(i+1)
        
        for platform in self.platforms:
            for i in range(platform["y_start"], min(platform["y_end"], self.y_dim)):
                for j in range(platform["x_start"], min(platform["x_end"], self.x_dim)):
                    grid[self.y_dim - 1 - i][j] = 'P'
        return grid
    
    def get_display_grid(self):
        grid = self.render_world()
        grid_str = '\n'.join(''.join(row) for row in grid)
        return grid_str
    
    def get_dict(self):
        result = {}
        result["RECT"] = self.rect
        result["DISC"] = self.disc
        result["DIAMONDS"] = self.diamonds
        result["PLATFORMS"] = self.platforms
        return result

    
    def __repr__(self):
        return (f"WorldParser(\nRECT: {self.rect}\nDISC: {self.disc}\nDIAMONDS: {self.diamonds}\nPLATFORMS: {self.platforms}\n)")
