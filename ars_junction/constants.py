# -*- coding: utf-8 -*-
"""
@file    constants.py
@author  Michael Behrisch
@author  Daniel Krajzewicz
@date    2008-07-21
@version $Id: constants.py 22608 2017-01-17 06:28:54Z behrisch $

Defining constants for the CityMobil parking lot.

SUMO, Simulation of Urban MObility; see http://sumo.dlr.de/
Copyright (C) 2008-2017 DLR (http://www.dlr.de/) and contributors

This file is part of SUMO.
SUMO is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""
from __future__ import absolute_import
import os
import sys

PREFIX = "junction"
TIME_STEPS = 50
VEH_ID = 'AUTO'
MAX_LANE_SPEED = 10
DEPART_TIME = 5

# INFINITY = 1e400
# DOUBLE_ROWS = 8
# ROW_DIST = 35
# STOP_POS = ROW_DIST - 12
# SLOTS_PER_ROW = 10
# SLOT_WIDTH = 5
# SLOT_LENGTH = 9
# SLOT_FOOT_LENGTH = 5
# CAR_CAPACITY = 3
# CYBER_CAPACITY = 20
# BUS_CAPACITY = 30
# TOTAL_CAPACITY = 60
# CYBER_SPEED = 5
# CYBER_LENGTH = 9
# WAIT_PER_PERSON = 5
# OCCUPATION_PROBABILITY = 0.5
# BREAK_DELAY = 1200
#
# PORT = 8883
# SUMO_HOME = os.path.realpath(os.environ.get(
#     "SUMO_HOME", os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))
# sys.path.append(os.path.join(SUMO_HOME, "tools"))
# try:
#     from sumolib import checkBinary
# except ImportError:
#     def checkBinary(name):
#         return name
# NETCONVERT = 'netconvert'
# SUMO = checkBinary("sumo")
# SUMOGUI = checkBinary("sumo-gui")
