import math

from simple_playgrounds.game_engine import Engine
from simple_playgrounds.playgrounds import *
from simple_playgrounds.utils import *
from simple_playgrounds.entities import *
from simple_playgrounds.entities.scene_elements.collection.contact import *



class CandyRoom(SingleRoom):

    def __init__(self, size = (300, 300), radius = 1/3, candy_number = 0, deviation = 0, deltaAngle = -1/4, **playground_params):

        super(CandyRoom, self).__init__(size = size, **playground_params)

        pi = math.pi

        #Number of targets
        number = candy_number

        #Circle parameters - adapted to the room size
        radius = min(size[0],size[1])*radius
        center = (size[0]/2,size[1]/2)

        #At which angle the repartition should start
        deltaAngle *= pi

        #Deviation from calculated position
        deviation




        for i in range(number):

            x = center[0]+radius*math.cos(2*pi*i/number + deltaAngle)
            y = center[1]+radius*math.sin(2*pi*i/number + deltaAngle)
            area = PositionAreaSampler(area_shape='circle', center=[x, y], radius=deviation)
            candy = Candy(area)
            self.add_scene_element(candy)
