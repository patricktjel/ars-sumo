#!/usr/bin/env python
"""
Script to generate the rou.xml file in the data folder.
"""
from __future__ import absolute_import
from __future__ import print_function
from VehicleType import VehicleType

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
    vtype = VehicleType("car")
    with open("data/%s.rou.xml" % PREFIX, "w") as routes:
        print("""<routes>
        """,vtype.printXML(),""""
        <route id="start" edges="4to1" />
        <route id="4to2" edges="4to1 1to2" />
        <route id="3to5" edges="3to1 1to5" />
    <vehicle id="AUTO" type="car" route="4to2" depart="0" color="1,0,0"/>
        """, file=routes)

        vehNr = 0
        for i in range(TIME_STEPS):
            # from 4 to 2 cars every step
            print('    <vehicle id="right_%i" type="car" route="4to2" depart="%i" />' % (
                vehNr, i), file=routes)
            vehNr += 1

            # from 3 to 5 cars every step
            print('    <vehicle id="down_%i" type="car" route="3to5" depart="%i" />' % (
                vehNr, i), file=routes)
            vehNr += 1

        print("</routes>", file=routes)


# this is the main entry point of this script
#if __name__ == "__main__":
generate_routefile()
