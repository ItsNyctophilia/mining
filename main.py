#!/usr/bin/env python3

from tkinter import Tk, mainloop

from GUI.map import Map
from zerg import Overlord
from zerg.drones import Drone, MinerDrone, ScoutDrone

root = Tk()

example = Map(root, "Potato")
ticks = 50
refined_minerals = 1000
fruity_pebbles = Overlord(ticks, refined_minerals)
coco_pebbles = ScoutDrone(fruity_pebbles)
coco_pebbles1 = Drone(fruity_pebbles)
coco_pebbles2 = MinerDrone(fruity_pebbles)
Dict = {
    id(coco_pebbles): coco_pebbles,
    id(coco_pebbles1): coco_pebbles1,
    id(coco_pebbles2): coco_pebbles2,
}


Map_dict = {1: "Waffle House", 2: "IHOP", 3: "Denny's"}


example.prepare_map()
# example.add_drone_to_tree(coco_pebbles)
# example.fill_map_table(Map_dict)
# example.update_drone_table(Dict)


mainloop()
