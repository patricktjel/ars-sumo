import logging

import gym
from gym import spaces
from gym.utils import seeding

logger = logging.getLogger(__name__)


class SumoEnv(gym.Env):
    def __init__(self):
        self._seed()

def _seed(self, seed=None):
    self.np_random, seed = seeding.np_random(seed)
    self.action_space = spaces.Discrete(2)
    return [seed]


def _step(self, action):
    return

def _reset(self):
    return