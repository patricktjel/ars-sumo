#!/usr/bin/env python
"""
Script to generate the rou.xml file in the data folder.
"""
from __future__ import absolute_import
from __future__ import print_function
import model.VehicleType as VehicleType
import model.Vehicle as Vehicle

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
    vtype = VehicleType.VehicleType("self_car")
    vehicle = Vehicle.Vehicle(VEH_ID, route="4to2", color="1,0,0")
    with open("data/%s.rou.xml" % PREFIX, "w") as routes:
        print("""<routes>
        """, vtype.printXML(), """"
        
        <route id="4to2" edges="4to1 1to2" />
        <route id="5to3" edges="5to1 1to3" />
        """, vehicle.printXML(), """
    
        """, file=routes)

        for i in range(TIME_STEPS):
            vehicle = Vehicle.Vehicle(i, route="5to3")
            print(vehicle.printXML(), file=routes)

        print("</routes>", file=routes)


# this is the main entry point of this script
if __name__ == "__main__":
    generate_routefile()
