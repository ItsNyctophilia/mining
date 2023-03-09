#!/usr/bin/env python3
"""Test main."""
from tkinter import Tk, mainloop

from mining.GUI.dashboard import Dashboard
from mining.utils.map import Map
from mining.utils.tile import Tile
from mining.utils.coordinate import Coordinate
from mining.utils.icon import Icon
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


cocopebbles = file_read("map03.txt")
cocopebbles2 = file_read("map02.txt")
example.create_map_gui(cocopebbles2)
example.create_map_gui(cocopebbles)
example.update_maps()
mainloop()
