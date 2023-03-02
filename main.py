#!/usr/bin/env python3 

from dashboard import Dashboard
from zerg.drones.drone import Drone
from zerg.drones.scout import ScoutDrone
from zerg.drones.miner import MinerDrone
from map import *
from tkinter import *
root = Tk()
example = Dashboard(root)
cocopebbles = ScoutDrone()
example.add_drone_to_tree(cocopebbles)

mainloop()
