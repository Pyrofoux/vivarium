from simple_playgrounds.entities.agents.sensors.semantic_sensors import *
from lidar import *
from simple_playgrounds.utils.definitions import ActionTypes, KeyTypes
import numpy as np

class Behavior():
    #Classe de base pour implémenter des comportements
    def __init__(self, agent, **parameters):

        #Stocker l'agent en entier, ou seulement ce que le Behavior veut récupérer ?
        self.agent = agent

        #Stocker les paramètres comme l'aggressivité de l'agent, etc
        self.parameters = parameters

        #Structures propres au comportement de l'IA, comme une mémoire
        self.memory = []

        pass

    def get_next_actions(self):

        #Entrée :
        observations = self.agent.observations

        #Format de la sortie :
        available_actions = self.agent.available_actions

        #Renvoie des valeurs transformées de available_actions
        pass

class BraitenbergVehicle(Behavior):

    def __init__(self, agent, sensorsAngle = 90, sensorsFoV = 200, connection = '=', activation = '+', target='Basic'):

        super(BraitenbergVehicle, self).__init__(agent)

        #Sensor parameters
        self.sensorsAngle = sensorsAngle
        self.sensorsFoV   = sensorsFoV

        self.connection = connection
        self.activation = activation

        self.target = target

        #Multiplicative coefficients for forward and rotational velocity
        self.forward_coeff = 0.25
        self.rotation_coeff = 1

        #Create lidar sensor for braitenberg behavior
        #2 Angle ranges : left and right
        #In this order, because of the direction of trigonometric angles

        self.lidar = LidarSensor(name= "lidar_braitenberg",anchor= agent.base_platform, invisible_body_parts= agent.parts, FoV = self.sensorsFoV, angle_ranges = [(0,self.sensorsAngle),(360-self.sensorsAngle,360)] ,fov=0)
        agent.add_sensor(self.lidar)


    def get_next_actions(self):


        #Calculating wheel activation
        right_activ, left_activ = self.calculate_stimulus(target_entity = self.target, connection = self.connection, activation = self.activation)

        #Conversion from wheel activation to longitudinal + angular velocity
        long_vel, ang_vel = self._lr_2_fwd_rot(left_activ, right_activ)

        actions = {}

        base_actions = {}

        base_actions[ActionTypes.LONGITUDINAL_FORCE] = long_vel

        #Positive = counter clock-wise, trigonometric
        base_actions[ActionTypes.ANGULAR_VELOCITY] = ang_vel

        actions[self.agent.base_platform.name] = base_actions


        return actions

    def calculate_stimulus(self, target_entity = "None", connection = "!", activation = "+"):

        #Right and left wheels connections to sensors

        #Parallel connections
        #if connection == "=":
        right_connect = 'right'
        left_connect  = 'left'

        #Opposite connections
        if connection != '=':
            right_connect = 'left'
            left_connect  = 'right'



        #Activation stimulus for each direction Closer = stronger
        stimulus = {}

        #Stimulus is 0 if target isn't found
        stimulus['left']  = self.lidar.observation[0].get(target_entity, 0)
        stimulus['right'] = self.lidar.observation[1].get(target_entity, 0)


        #Which wheel is the sensor connected to ? Activation or inhibition ?
        right_activ = self.calculate_activation(stimulus[right_connect], activation)
        left_activ = self.calculate_activation(stimulus[left_connect], activation)

        return left_activ, right_activ

    def calculate_activation(self, value, weight):

        if weight == '0':
            return 0
        elif weight == "+":
            return value
        elif weight == '-':
            return 1-value
        else:
            raise BaseException("Symbol '"+str(weight)+"' is not recognized as a valid activation symbol")


    def _lr_2_fwd_rot(self, left_spd, right_spd):
        fwd = self.forward_coeff * (left_spd + right_spd)
        rot = self.rotation_coeff * (left_spd - right_spd)
        return fwd, rot


class MultiBraitenbergVehicle(Behavior):

    def __init__(self, agent, sensorsAngle = 90, sensorsFoV = 200, behaviors = [('=','+','Basic',1)]):

        super(MultiBraitenbergVehicle, self).__init__(agent)
        #self.logger = logger

        #Sensor parameters
        self.sensorsAngle = sensorsAngle
        self.sensorsFoV   = sensorsFoV

        self.behaviors = behaviors

        #Multiplicative coefficients for forward and rotational velocity
        self.forward_coeff = 0.25
        self.rotation_coeff = 1

        #Create lidar sensor for braitenberg behavior
        #2 Angle ranges : left and right
        #In this order, because of the direction of trigonometric angles

        self.lidar = LidarSensor(name= "lidar_braitenberg",anchor= agent.base_platform, invisible_body_parts= agent.parts, FoV = self.sensorsFoV, angle_ranges = [(0,self.sensorsAngle),(360-self.sensorsAngle,360)] ,fov=0)
        agent.add_sensor(self.lidar)

    def get_next_actions(self):


        #Stores stimulus for every behavior
        right_stimuli = []
        left_stimuli  = []
        weights       = []

        for behavior in self.behaviors:

            connection = behavior[0]
            activation = behavior[1]
            target = behavior[2]
            weighted_coeff = behavior[3]

            #Calculating wheel activation for this behavior
            right_activ, left_activ = self.calculate_stimulus(target_entity = target, connection = connection, activation = activation)

            right_stimuli.append(right_activ)
            left_stimuli.append(left_activ)
            weights.append(weighted_coeff)

        right_activ = np.average(right_stimuli, weights=weights)
        left_activ = np.average(left_stimuli, weights=weights)

        #Conversion from wheel activation to longitudinal + angular velocity
        long_vel, ang_vel = self._lr_2_fwd_rot(left_activ, right_activ)

        actions = {}

        base_actions = {}

        base_actions[ActionTypes.LONGITUDINAL_FORCE] = long_vel

        #Positive = counter clock-wise, trigonometric
        base_actions[ActionTypes.ANGULAR_VELOCITY] = ang_vel

        actions[self.agent.base_platform.name] = base_actions


        return actions

    def calculate_stimulus(self, target_entity = "None", connection = "!", activation = "+"):

        #Right and left wheels connections to sensors

        #Parallel connections
        #if connection == "=":
        right_connect = 'right'
        left_connect  = 'left'

        #Opposite connections
        if connection != '=':
            right_connect = 'left'
            left_connect  = 'right'



        #Activation stimulus for each direction Closer = stronger
        stimulus = {}

        #Stimulus is 0 if target isn't found
        stimulus['left']  = self.lidar.observation[0].get(target_entity, 0)
        stimulus['right'] = self.lidar.observation[1].get(target_entity, 0)


        #Which wheel is the sensor connected to ? Activation or inhibition ?
        right_activ = self.calculate_activation(stimulus[right_connect], activation)
        left_activ = self.calculate_activation(stimulus[left_connect], activation)

        return left_activ, right_activ

    def calculate_activation(self, value, mode):

        if mode == '0':
            return 0
        elif mode == "+":
            return value
        elif mode == '-':
            return 1-value
        else:
            raise BaseException("Symbol '"+str(weight)+"' is not recognized as a valid activation symbol")

    def _lr_2_fwd_rot(self, left_spd, right_spd):
        fwd = self.forward_coeff * (left_spd + right_spd)
        rot = self.rotation_coeff * (left_spd - right_spd)
        return fwd, rot
