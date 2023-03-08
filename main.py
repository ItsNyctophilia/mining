#!/usr/bin/env python3
"""Test main."""
from tkinter import Tk, mainloop

from mining.GUI.dashboard import Dashboard
from mining.utils.map import Map
root = Tk()

example = Dashboard(root)

map_dict = {
        1 : "Map one",
        2 : "Map two",
        3 : "Map three",
        }
cocopebbles = Map()
example.fill_map_table(map_dict)
example.create_map_gui(cocopebbles)
mainloop()
