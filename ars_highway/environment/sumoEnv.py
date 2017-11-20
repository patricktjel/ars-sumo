from __future__ import absolute_import
from __future__ import print_function

import logging


import constants
import gym
import numpy as np
from gym import spaces
from gym.utils import seeding
from constants import *

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

logger = logging.getLogger(__name__)


class SumoEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 50
    }

    def __init__(self):
        self._seed()

        # Speeds in meter per second
        self.maxSpeed = 70
        self.minSpeed = 0

        # distances
        self.minDistance = 0
        self.maxDistance = 500

        high = np.array([
            self.maxSpeed,
            self.maxDistance
        ])
        low = np.array([
            self.minSpeed,
            self.maxDistance
        ])

        self.observation_space = spaces.Box(low, high)
        self.action_space = spaces.Discrete(3)

        self._seed()
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

        self.started = False


    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]


    def _step(self, action):
        reward = 0

        #if traci.simulation.getCurrentTime() % 10000 == 0:
            # print(traci.vehicle.getSpeed(VEH_ID))
            # lane = traci.vehicle.getLaneID(VEH_ID);
            # print(traci.lane.getMaxSpeed(lane))
        if action == 0:
            traci.vehicle.setSpeed(VEH_ID, traci.vehicle.getSpeed(VEH_ID) + 2)
        if action == 1:
            traci.vehicle.setSpeed(VEH_ID, traci.vehicle.getSpeed(VEH_ID) - 2)

        traci.simulationStep()

        if VEH_ID in traci.vehicle.getIDList():
            lane = traci.vehicle.getLaneID(VEH_ID)
            if traci.vehicle.getSpeed(VEH_ID) > traci.lane.getMaxSpeed(lane):
                reward = -10
            else:
                reward = traci.vehicle.getSpeed(VEH_ID)/traci.lane.getMaxSpeed(lane)

            self.state = (traci.vehicle.getSpeed(VEH_ID), traci.vehicle.getDistance(VEH_ID))
            return np.array(self.state), reward, False, {}
        return np.array(self.state), 0, True, {}

    def _reset(self):
        sumoBinary = checkBinary('sumo-gui')

        if self.started:
            traci.close()
        traci.start([sumoBinary, "-c", "data/highway.sumocfg",
                     "--tripinfo-output", "tripinfo.xml"])
        traci.simulationStep()
        traci.vehicle.setSpeed(VEH_ID, 0)
        self.started = True

        self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(2,))
        self.steps_beyond_done = None
        return np.array(self.state)
