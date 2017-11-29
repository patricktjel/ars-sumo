from __future__ import absolute_import
from __future__ import print_function

import logging

import constants
import gym
import numpy as np
from gym import spaces
from constants import *
import random as rn

import os
import sys

# Setting the seeds to get reproducible results
os.environ['PYTHONHASHSEED'] = '0'
np.random.seed(42)
rn.seed(12345)

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

logger = logging.getLogger(__name__)

gui = False
if gui:
    sumoBinary = checkBinary('sumo-gui')
else:
    sumoBinary = checkBinary('sumo')
config_path = "../data/highway.sumocfg"


class SumoEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 50
    }

    def __init__(self):
        self._seed()

        # Speeds in meter per second
        self.maxSpeed = 20
        self.minSpeed = 0

        high = np.array([
            self.maxSpeed
        ])
        low = np.array([
            self.minSpeed
        ])

        # Observation space of the environment
        self.observation_space = spaces.Box(low, high)
        self.action_space = spaces.Discrete(3)

        self.viewer = None
        self.state = None
        self.log = False
        self.result = []
        self.run = []
        self.test = False

    def _step(self, action):
        if VEH_ID in traci.vehicle.getIDList():
            # apply the given action
            if action == 0:
                traci.vehicle.setSpeed(VEH_ID, traci.vehicle.getSpeed(VEH_ID) + 0.25)
            if action == 2:
                traci.vehicle.setSpeed(VEH_ID, traci.vehicle.getSpeed(VEH_ID) - 0.25)

        # Run a step of the simulation
        traci.simulationStep()

        # Check the result of this step and assign a reward
        if VEH_ID in traci.vehicle.getIDList():
            lane = traci.vehicle.getLaneID(VEH_ID)
            maxLaneSpeed = traci.lane.getMaxSpeed(lane)
            speed = traci.vehicle.getSpeed(VEH_ID)

            if speed > maxLaneSpeed:
                reward = -10 * (speed - maxLaneSpeed)
            else:
                reward = speed ** 2

            self.state = speed

            if self.log:
                print("%d %.2f %d %.2f" % (traci.simulation.getCurrentTime() / 100, speed, action, reward))
                if self.test:
                    self.run.append(speed)
            return np.array(self.state), reward, False, {}
        return np.array(self.state), 0, True, {}

    def _reset(self):
        if self.test and len(self.run) != 0:
            self.result.append(list(self.run))
            self.run.clear()

        traci.load(["-c", config_path])
        traci.simulationStep()

        # Setup environment
        speed = rn.randint(1, 8)
        traci.vehicle.setSpeedMode(VEH_ID, 0)
        traci.vehicle.setSpeed(VEH_ID, speed)

        traci.simulationStep()

        self.state = speed
        return np.array(self.state)

    def close(self):
        traci.close()


traci.start([sumoBinary, "-c", config_path])
