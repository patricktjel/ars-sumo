#!/usr/bin/env python
"""
Script to generate the rou.xml file in the data folder.
"""
from __future__ import absolute_import
from __future__ import print_function

import random
from constants import *

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


# method to generate routes file.
def generate_routefile():
    random.seed(42)  # make tests reproducible

    # demand per second from different directions
    fourToTwo = 1. / 11
    fourToThree = 1. / 10
    fourToFive = 1. / 30
    with open("data/%s.rou.xml" % PREFIX, "w") as routes:
        print("""<routes>
        <vType id="car" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" guiShape="passenger"/>

        <route id="4to2" edges="4to1 1to2" />
        <route id="4to3" edges="4to1 1to3" />
        <route id="4to5" edges="4to1 1to5" />
        
        <route id="2to3" edges="2to1 1to3" />
        <route id="2to4" edges="2to1 1to4" />
        <route id="2to5" edges="2to1 1to5" />""", file=routes)
        vehNr = 0
        for i in range(TIME_STEPS):
            random_number = random.uniform(0, 1)
            if random_number < fourToTwo:
                print('    <vehicle id="down_%i" type="car" route="4to2" depart="%i" color="1,0,0"/>' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random_number < fourToThree:
                print('    <vehicle id="left_%i" type="car" route="4to3" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random_number < fourToFive:
                print('    <vehicle id="right_%i" type="car" route="4to5" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1

            if random_number < fourToTwo:
                print('    <vehicle id="down_%i" type="car" route="2to4" depart="%i" color="1,0,0"/>' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random_number < fourToThree:
                print('    <vehicle id="left_%i" type="car" route="2to3" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random_number < fourToFive:
                print('    <vehicle id="right_%i" type="car" route="2to5" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1

        print("</routes>", file=routes)


# this is the main entry point of this script
if __name__ == "__main__":
    generate_routefile()
