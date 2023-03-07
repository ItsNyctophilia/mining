#!/usr/bin/env python3 

from GUI.dashboard import Dashboard
from zerg.drones.drone import Drone
from zerg.drones.scout import ScoutDrone
from zerg.drones.miner import MinerDrone
from GUI.map import *
from tkinter import *
root = Tk()

example = Dashboard(root)


mainloop()
