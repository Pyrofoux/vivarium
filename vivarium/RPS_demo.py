import time
import json
import pandas as pd
import cv2
import numpy as np

from simple_playgrounds.game_engine import Engine
from simple_playgrounds.entities.agents.basic_agents import *
from simple_playgrounds.entities.agents.parts import *
from behavior import *
from braitenberg_rooms import *
import pygame

from logger import *
from tqdm import tqdm,trange


#Map Characteristics
map_size = 300
initial_spawn = PositionAreaSampler(area_shape='circle', center=[map_size/2, map_size/2], theta_range = [0,6.28], radius=map_size/2)
#Number of subrooms - default is (1,1)
n_rooms=(1, 1)

#Shared characteristics across all species
class Species(Agent):

    def __init__(self,

    #Default charateristics for all agents
    radius = 6,
    max_linear_force = 1,
    max_angular_velocity = 0.4,
    color = [0, 150, 0],

    sensorsFoV = 300,
    sensorsAngle = 90,

    #specific position to put agent (eg: when splitting, must be placed near)
    specific_position=None,
    #if position not specified, will use initial_spawn agent
    initial_position=initial_spawn,

    **kwargs):

        #Morphological characteristics
        base_platform = PlatformWithAngle(
        radius = radius,
        can_absorb = True,
        max_linear_force = max_linear_force,
        max_angular_velocity = max_angular_velocity,
        texture= {'texture_type':'color','color':color}
        )

        if  not (specific_position is None):
            initial_position = PositionAreaSampler(area_shape='circle', center=[specific_position[0], specific_position[1]], theta_range = [0,6.28], radius=1)

        super(Species, self).__init__(base_platform = base_platform, initial_position = initial_position, **kwargs)

        #Behaviorial Characteristics : Chase mode
        self.behavior = MultiBraitenbergVehicle(self,
        #Chase Candy
        behaviors=[
        ("=","+","Basic",2), #Avoid obstacles
        ("=","+",self.predator,1),  #Avoid predator
        ("!","+",self.prey,3)  #Attracted to prey
        ],
        #Sensor parameters
        sensorsFoV = 200, sensorsAngle = 180
        )

        #Distance where agent can attack
        self.attack_distance = 15
        #Current life of agent
        self.life = 100
        #Thresold before splitting
        self.splitting_thresold = 180

        #Internal information
        self.alive = True
        self.splitting = False



    def step_event(self, me, others):


        my_position = Vec2d(me.position[0], me.position[1])

        #Updating life energy based on distance attacks
        for agent in others:
            name = type(agent).__name__

            #If near a prey - take energy from it
            if name == self.prey:
                distance = my_position.get_distance(agent.position)
                if distance < self.attack_distance:
                    agent.life -= 1 #Total life energy of simulation is fixed
                    self.life += 1

        #Update alive status
        if self.life <= 0:
            self.alive = 0

        #Update splitting status
        if self.life >= self.splitting_thresold:
            self.splitting = True

    def split(self):

        clone = None
        if self.species == 'A':
            clone = A(specific_position = [self.position[0], self.position[1]])
        elif self.species == 'B':
            clone = B(specific_position = [self.position[0], self.position[1]])
        elif self.species == 'C':
            clone = C(specific_position = [self.position[0], self.position[1]])

        #Clone has half the energy of the original
        clone.life = self.life/2
        self.life -= clone.life
        return clone



#Red
class A(Species):

    def __init__(self, name = None, **kwargs):

        #Predators & Preys
        self.predator = 'C'
        self.prey = 'B'
        self.species = 'A'

        super(A, self).__init__(name = name, color = [150, 0, 0], **kwargs)

#Green
class B(Species):

    def __init__(self, name = None, **kwargs):

        #Predators & Preys
        self.predator = 'A'
        self.prey = 'C'
        self.species = 'B'

        super(B, self).__init__(name = name, color = [0, 150, 0], **kwargs)

#Blue
class C(Species):

    def __init__(self, name = None, **kwargs):

        #Predators Preys
        self.predator = 'B'
        self.prey = 'A'
        self.species = 'C'

        super(C, self).__init__(name = name, color = [0, 0, 150], **kwargs)


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

def run(a = 1, b = 1, c = 1, steps = 100, display = False):


    #Playground -- Rooms
    pg = ConnectedRooms2D(size = [map_size, map_size],

    #Number of subrooms
    #Default is (1, 1)
    n_rooms=n_rooms)

    agents = []

    #Generating agents for each species
    for i in range(a):
            my_agent = A(name="A_"+str(i))
            agents.append(my_agent)
    for i in range(b):
            my_agent = B(name="B_"+str(i))
            agents.append(my_agent)
    for i in range(c):
            my_agent = C(name="C_"+str(i))
            agents.append(my_agent)

    #Adding agents
    for agent in agents:
        pg.add_agent(agent)

    game = Engine(playground=pg, time_limit = steps, screen=display)

    #Simulation loop

    for current_step in trange(steps):

        #Events happening each step
        dead_agents = []
        baby_agents = []

        for agent in game.agents:
            agent.step_event(agent, game.agents)

            #Create baby ?
            if agent.splitting == True:
                agent.splitting = False
                baby_agents.append(agent.split())

            #Dead agent ?
            if agent.alive == False:
                dead_agents.append(agent)

        #Removing dead agents
        for dead in dead_agents:
            pg.remove_agent(dead)

        #Adding baby agents
        for baby in baby_agents:
            pg.add_agent(baby)


        game.update_observations()
        actions = {}

        #Behavorial events
        for agent in game.agents:
            next_actions = agent.behavior.get_next_actions()
            actions[agent.name] = next_actions


        #Updating game steps and observations
        game.step(actions)


        #Visualisation
        if display:
            cv2.waitKey(1)
            game.display_full_scene()

        #Logging data
        log_data(game.agents)

    #Plotting Data
    Logger.plot()
    Logger.show()
    game.terminate()

#Choosing variables to log
def log_data(agents):

    species = {'A':0, 'B':0, 'C':0}
    for agent in agents:
        species[agent.species] += 1

    Logger.add(species['A'],'count_A')
    Logger.add(species['B'],'count_B')
    Logger.add(species['C'],'count_C')


run(a = 10, b = 10, c = 10, display = True, steps = 2000)
