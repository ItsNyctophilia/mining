#!/usr/local/bin/python
"""
Defines Map class along with the methods and attributs that it uses.
"""
import random
import tkinter


class Map(tkinter.Toplevel):
    """
    Serves as a blueprint for a map object
    """

    def __init__(self, parent, title):
        super().__init__(parent)
        self.geometry("300x200+300+0")
        self.title(title)
        self.log = tkinter.Text(self, width=30, height=30)
        self.log.pack()

    def write_up(self, string, x, y):
        """
        This writes to the map in certain unicode characters
        """
        unicode_dict = {
            'wall': u'\u2589',
            'acid': u'\u2600',
            'minerals': u'\u2662',
            'drone': u'\u26DF',
            'deployment': u'\u25BD',
            'unknown': u'\u26F6'
        }
        unicode_character = unicode_dict[string]
        coordinates = f'{y}.{x}'
        self.log.insert(coordinates, unicode_character)
