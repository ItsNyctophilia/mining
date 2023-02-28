#!/usr/local/bin/python

import random
import tkinter


class Dashboard(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("300x200+300+0")
        self.title("Overlord's Dashboard")
        self.log = tkinter.Text(self, height=10,  width=30)
        self.log.pack()