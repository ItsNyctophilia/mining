#!/usr/local/bin/python

import random
import tkinter


class Map(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("300x200+300+0")
        self.title("Map")
        self.log = tkinter.Text(self, width=30,  height=30)
        self.log.pack()


    def write_up(self, string, x, y):
        unicode_dict = {
            'wall' : u'\u2589',
            'acid' : u'\u2600',
            'minerals' : u'\u2662',
            'drone' : u'\u26DF',
            'deployment' : u'\u25BD',
            'unknown' : u'\u26F6'
        }
        unicode_character = unicode_dict[string]
        coordinates = f'{y}.{x}'
        self.log.insert(coordinates, unicode_character)
        