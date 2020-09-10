import time
import json
import pandas as pd
import cv2

from simple_playgrounds.game_engine import Engine
from simple_playgrounds.entities.agents.basic_agents import *
from simple_playgrounds.entities.agents.parts import *
from behavior import *
from braitenberg_rooms import *
import pygame

#Demo map to test/debug agent behaviour in presence of collectible items
#Useful for testing Braitenberg behavior

#Map Characteristics
map_size = 300
candy_number = 5


class ChaserAgent(Agent):

    def __init__(self, initial_position, **kwargs):

        agent_base = PlatformWithAngle(
        radius = 6,
        can_absorb = True, #Important if you want the agent to be able to eat!
        max_angular_velocity = 1,
        max_linear_force = 1,
        texture= {'texture_type':'color','color':[0, 150, 150]})


        super(ChaserAgent, self).__init__(initial_position=initial_position, base_platform=agent_base, **kwargs)

        #Behavior Initialisation : Chase mode
        self.behavior = MultiBraitenbergVehicle(self,
        #Chase Candy
        behaviors=[
        ("=","+","Basic",1), #Avoid walls
        ("!","+","Candy",3)  #Attracted to candy
        ],
        #Sensor parameters
        sensorsFoV = 200, sensorsAngle = 180
        )



## Edited platform to show the direction the agent is looking at
## (white line)
class PlatformWithAngle(ForwardPlatform):

    def __init__(self, **kwargs):
        super(PlatformWithAngle,self).__init__(**kwargs)

    def _create_mask(self, is_interactive=False):

        mask = Part._create_mask(self)

        pos_y = self.radius + (self.radius-2) * (math.cos(self.pm_body.angle))
        pos_x = self.radius + (self.radius-2) * (math.sin(self.pm_body.angle))
        pygame.draw.line(mask, pygame.color.THECOLORS["white"],
                         (self.radius, self.radius), (pos_x, pos_y), 2)

        return mask

def run(nbAgents = 1, steps = 100, display = False):

    pg = CandyRoom(size = [map_size, map_size], candy_number = candy_number, deviation = 0, deltaAngle = -1/4)

    agents = []

    initial_position = PositionAreaSampler(area_shape='circle', center=[150, 150], theta_range = [0,0], radius=0)

    #Generating agents
    for i in range(nbAgents):

        my_agent = ChaserAgent(initial_position =initial_position, max_angular_velocity=10, name="")
        pg.add_agent(my_agent)

    game = Engine(playground=pg, time_limit = steps, screen=display)

    while game.game_on:

        game.update_observations()

        actions = {}
        for agent in game.agents:
            actions[agent.name] = agent.behavior.get_next_actions()

        #Updating game steps and observations
        game.step(actions)


        #Visualisation

        if display:
            cv2.waitKey(15)
            game.display_full_scene()

    game.terminate()

run(nbAgents = 1, display = True, steps = 2000)
