#!/usr/bin/env python3 

from dashboard import Dashboard
from map import *
from tkinter import *
root = Tk()
example = Map(root)
example.log.insert('1.0', "Cocopebbles\n")
example.log.insert('2.0', "Cocopebbles\n")
example.log.insert('3.0', "Cocopebbles\n")
example.log.insert('3.5', "Cocopebbles\n")
example.write_up('unknown', 1, 2)

mainloop()
