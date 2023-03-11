#!/usr/bin/env python3
"""Test main."""
from tkinter import Tk, mainloop

from mining.GUI.dashboard import Dashboard
from mining.utils.map import Map
from mining.zerg_units.overlord import Overlord
from mining.utils.tile import Tile
from mining.utils.coordinate import Coordinate
from mining.utils.icon import Icon
from mining.zerg_units.drones.scout import ScoutDrone

def file_read(file_name):
    new_map = Map()
    Tile_dict = {}
    fp = open(file_name, "r")
    linecounter = 1
    for line in fp:
        lettercounter = 0 
        for letter in line:
            if letter == '\n':
                letter = ' '
            elif letter.isnumeric():
                letter = '*'
            Coordinate = (lettercounter, linecounter)
            tile = Tile(Coordinate, Icon(letter))
            Tile_dict[Coordinate] = tile
            lettercounter += 1
        linecounter += 1
    new_map._stored_tiles_ = Tile_dict
    return new_map
    


root = Tk()

example = Dashboard(root)

new_overlord = Overlord(example, 5, 10)

new_drone = ScoutDrone(new_overlord)
example.add_drone_to_tree(new_drone)
mainloop()
