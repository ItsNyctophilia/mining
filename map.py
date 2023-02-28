#!/usr/local/bin/python

import random
import tkinter


class Map(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("300x200+300+0")
        self.title("Map")
        self.log = tkinter.Text(self, height=50,  width=50)
        self.log.pack()
        