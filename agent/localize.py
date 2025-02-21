from agent.util import * 
import random
from datetime import datetime

class SelfLocalizer:
    def __init__(self, world_connector, tries=8, check_wait=10):
        self.start_time = None
        self.disc_soc = 0
        self.rect_soc = 0
        self.wc = world_connector
        self.tries = tries
        self.current_try = 0

        self.disc = None
        self.rect = None
        self.disc_vel_x = 0.0
        self.disc_vel_y = 0.0
        self.rect_vel_x = 0.0

        self.last_disc = None
        self.last_rect = None
        self.last_disc_vel_x = 0.0
        self.last_disc_vel_y = 0.0
        self.last_rect_vel_x = 0.0

        self.last_key = NO_ACT_KEY
        self.check_wait = check_wait
        self.wait_time = 0


    def _compute_velocities(self):
        self.disc_vel_x = self.disc["x"] - self.last_disc["x"]
        self.disc_vel_y = self.disc["y"] - self.last_disc["y"]
        self.rect_vel_x = self.rect["middle_x"] - self.last_rect["middle_x"]


    def _check_for_effect(self, agent_type):
        if agent_type == AgentType.DISC:
            if self.last_key == UP_KEY:
                self.disc_soc += int(self.disc["y"] > self.last_disc["y"])
            if self.last_key == DOWN_KEY:
                self.disc_soc += 1
            if self.last_key == LEFT_KEY:
                self.disc_soc += int(self.disc_vel_x > self.last_disc_vel_x)
            if self.last_key == RIGHT_KEY:
                self.disc_soc += int(self.disc_vel_x < self.last_disc_vel_x)
        if agent_type == AgentType.RECT:
            if self.last_key == UP_KEY:
                self.rect_soc += int(self.rect["width"] < self.last_rect["width"])
            if self.last_key == DOWN_KEY:
                self.rect_soc += int(self.rect["width"] > self.last_rect["width"])
            if self.last_key == LEFT_KEY:
                self.rect_soc += int(self.rect_vel_x > self.last_rect_vel_x)
            if self.last_key == RIGHT_KEY:
                self.rect_soc += int(self.rect_vel_x < self.last_rect_vel_x)

    def has_determined(self):
        return self.current_try >= self.tries
    
    def get_type(self):
        print(f"disc soc: {self.disc_soc}")
        print(f"rect soc: {self.rect_soc}")
        if self.disc_soc > self.rect_soc:
            return AgentType.DISC
        else: 
            return AgentType.RECT


    def handle_world(self, world_desc):
        if self.start_time is None:
            self.start_time = datetime.now()
        current_time = datetime.now()
        t_delta = current_time - self.start_time
        t_delta_ms = (t_delta.seconds * 1000) + (t_delta.microseconds / 1000)

        self.disc = self.wc.get_disc()
        self.rect = self.wc.get_rect()

        if t_delta_ms < 600:
            # wait for startup
            self.last_key == NO_ACT_KEY

        elif self.last_key == NO_ACT_KEY:
            self.last_key = random.choice(VALID_KEY_LIST)
        elif self.wait_time >= self.check_wait:
                self.wait_time = 0
                self._compute_velocities()
                self._check_for_effect(AgentType.DISC)
                self._check_for_effect(AgentType.RECT)
                self.last_key = random.choice(VALID_KEY_LIST)
                self.current_try = self.current_try + 1
        else:
            # wait until game reacts
            self.wait_time += 1
            return NO_ACT_KEY
        self.last_disc = self.disc
        self.last_rect = self.rect
        self.last_disc_vel_x = self.disc_vel_x
        self.last_disc_vel_y = self.disc_vel_y
        self.last_rect_vel_x = self.rect_vel_x
        
        return self.last_key


    