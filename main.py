#!/usr/bin/env python3 

from GUI.dashboard import Dashboard
from zerg.drones.drone import Drone
from zerg.drones.scout import ScoutDrone
from zerg.drones.miner import MinerDrone
from GUI.map import *
from tkinter import *
root = Tk()

example = Map(root, "Potato")
cocopebbles = ScoutDrone()
cocopebbles1 = Drone()
cocopebbles2 = MinerDrone()
Dict = {id(cocopebbles): cocopebbles, 
        id(cocopebbles1): cocopebbles1,
          id(cocopebbles2): cocopebbles2}



Map_dict =  {1: "Waffle House", 
        2: "IHOP",
          3: "Denny's"}


example.prepare_map()
#example.add_drone_to_tree(cocopebbles)
#example.fill_map_table(Map_dict)
#example.update_drone_table(Dict)


mainloop()
