from __future__ import absolute_import
from __future__ import print_function

import constants
import gym
import numpy as np
from gym import spaces

import createRoute
from constants import *
import random as rn

import os
import sys

# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import traci
from traci.constants import *

# Setting the seeds to get reproducible results
os.environ['PYTHONHASHSEED'] = '0'
np.random.seed(42)
rn.seed(12345)


# The 90 is a magic variable which should  be changed when the road get's longer.
def detectCollision(traci_data, veh_travelled_distance):
    return VEH_ID not in traci_data and veh_travelled_distance <= 90


def speedReward(speed):
    return -1 * (1 / (MAX_LANE_SPEED / (4 / 5))) * speed ** 5 + speed ** 4


def getReward(traci_data):
    speed = traci_data[VEH_ID][VAR_SPEED]
    reward = speedReward(speed)
    reward *= 10/speedReward(MAX_LANE_SPEED)
    # minus the time it costs
    reward -= traci.simulation.getCurrentTime()/10000
    return reward


class SumoEnv(gym.Env):

    def __init__(self):
        # Speeds in meter per second
        self.maxSpeed = 20
        self.minSpeed = 0

        high = np.append([
                self.maxSpeed
            ],
            np.ones(shape=(11, 11))
        )
        low = np.append([
                self.minSpeed
            ],
            np.zeros(shape=(11, 11))
        )

        # Observation space of the environment
        self.observation_space = spaces.Box(low, high)
        self.action_space = spaces.Discrete(3)

        self.viewer = None
        self.state = None
        self.log = False
        self.result = []
        self.run = []
        self.test = False

        # This variable automatically get's updated after traci.simulationStep()
        # self.traci_data

        self.config_path = "../data/{}.sumocfg".format(PREFIX)

    # check if it is possible to subscribe the next vehicle
    def subscribe_vehicles(self):
        # is the next id legit?
        if self.next_id_to_subscribe < len(self.created_cars):
            prev_car = self.created_cars[self.next_id_to_subscribe - 1]
            # check if the previous car is already in the simulation so that SUMO has read car 'next_id_to_subscribe
            if prev_car in self.traci_data and self.traci_data[prev_car][VAR_POSITION] > (0, 0):
                try:
                    traci.vehicle.subscribe(str(self.next_id_to_subscribe), [VAR_SPEED, VAR_DISTANCE, VAR_POSITION])
                    self.next_id_to_subscribe += 1
                except Exception:
                    pass

    # Sets the state to the currently known values
    def set_state(self):
        speed = self.traci_data[VEH_ID][VAR_SPEED]

        position_grid = np.zeros(shape=(11, 11))
        car_position = self.traci_data[VEH_ID][VAR_POSITION]
        for x, y in [x[VAR_POSITION] for x in self.traci_data.values()]:
            relative_x = x - car_position[0]
            relative_y = y - car_position[1]
            x_index = 5 + int(relative_x/5)
            y_index = 5 + int(relative_y/5)
            if -5 <= x_index <= 5 and -5 <= y_index <= 5:
                position_grid[x_index][y_index] = 1

        self.state = np.reshape(np.append([speed], position_grid), (1, self.observation_space.shape[0]))

    def _step(self, action):
        self.subscribe_vehicles()

        pos = self.traci_data[VEH_ID][VAR_DISTANCE]
        if VEH_ID in self.traci_data:
            # apply the given action
            if action == 0:
                traci.vehicle.setSpeed(VEH_ID, self.traci_data[VEH_ID][VAR_SPEED] + 0.25)
            if action == 2:
                traci.vehicle.setSpeed(VEH_ID, self.traci_data[VEH_ID][VAR_SPEED] - 0.25)

        # Run a step of the simulation
        traci.simulationStep()

        if detectCollision(self.traci_data, pos):
            print("collision detected")
            return np.array(self.state), -10000, True, {}

        # Check the result of this step and assign a reward
        if VEH_ID in self.traci_data:
            reward = getReward(self.traci_data)

            self.set_state()

            if self.log:
                print("{:.2f} {:d} {:.2f}".format(self.traci_data[VEH_ID][VAR_SPEED], action, reward))
            if self.test:
                self.run.append(self.traci_data[VEH_ID][VAR_SPEED])
            return np.array(self.state), reward, False, {}
        return np.array(self.state), 0, True, {}

    def _reset(self):
        if self.test and len(self.run) != 0:
            self.result.append(list(self.run))
            self.run.clear()

        # generate new traffic situation
        self.created_cars = createRoute.generate_routefile('../data/junction.rou.xml')

        traci.load(["-c", self.config_path])
        traci.simulationStep()

        # Setup environment
        traci.vehicle.setSpeedMode(VEH_ID, 0)
        traci.vehicle.setSpeed(VEH_ID, rn.randint(1, 8))

        traci.simulationStep()
        traci.vehicle.subscribe(VEH_ID, [VAR_SPEED, VAR_DISTANCE, VAR_POSITION])
        self.next_id_to_subscribe = 1

        self.set_state()
        return self.state

    def start(self, gui=False):
        sumoBinary = checkBinary('sumo-gui') if gui else checkBinary('sumo')
        traci.start([sumoBinary, "-n", "../data/{}.net.xml".format(PREFIX)])
        self.traci_data = traci.vehicle.getSubscriptionResults()

    def close(self):
        traci.close()
