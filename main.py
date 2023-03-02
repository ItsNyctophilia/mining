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
cocopebbles1 = Drone()
cocopebbles2 = MinerDrone()
Dict = {id(cocopebbles): cocopebbles, 
        id(cocopebbles1): cocopebbles1,
          id(cocopebbles2): cocopebbles2}






example.add_drone_to_tree(cocopebbles)
example.update_drone_table(Dict)


mainloop()
