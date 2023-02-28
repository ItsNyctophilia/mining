#!/usr/local/bin/python

import random
import tkinter 
from tkinter import ttk


class Dashboard(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Overlord's Dashboard")
        self.map_tree = self.make_tree("bottom", "Map", "Map ID")
        
    #https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def make_tree(self, aligment, column1, column2):
        # Using treeview widget
        treev = ttk.Treeview(self, selectmode ='browse')

                # Calling pack method w.r.to treeview
        treev.pack(side = aligment)
        
        # Defining number of columns
        treev["columns"] = ("1", "2")
        
        # Defining heading
        treev['show'] = 'headings'
        
        # Assigning the width and anchor to  the
        # respective columns
        treev.column("1", width = 180, anchor ='c')
        treev.column("2", width = 180, anchor ='se')
        
        # Assigning the heading names to the
        # respective columns
        treev.heading("1", text = column1)
        treev.heading("2", text = column2)
        return treev
    #https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
