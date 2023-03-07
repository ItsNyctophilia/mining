#!/usr/bin/env python3
"""Test main."""
from tkinter import Tk, mainloop

from mining.GUI.dashboard import Dashboard

root = Tk()

example = Dashboard(root)

mainloop()
