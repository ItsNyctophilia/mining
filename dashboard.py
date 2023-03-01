"""
This serves to define the dashboard clas, defines the attributes it has along with 
the methods that it uses.

"""

# !/usr/local/bin/python

import random
import tkinter
from tkinter import ttk


class Dashboard(tkinter.Toplevel):
    """
    serves as blueprint for the dashboard class
    """

    def __init__(self, parent):
        """
        serves as the constructore for a dashboard object
        """
        super().__init__(parent)
        photo = tkinter.PhotoImage(file='icon.png')
        self.wm_iconphoto(False, photo)
        self.minsize(500, 300)
        self.title("Overlord's Dashboard")
        self.map_tree = self.make_tree("top", "Map", "Map ID")
        self.turn_tree = self.make_tree("bottom", "Tick", "Action")
        # self.map_tree.insert('', 'end', text='Listbox', values=('15KB', 'Yesterday'))

    # https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def make_tree(self, aligment, column1, column2):
        """
        Builds trees for the dasboard to use, dashboards typically serve spreadhsheets in the gui.
        """
        # Using treeview widget
        treev = ttk.Treeview(self, selectmode='browse')

        # Calling pack method w.r.to treeview
        treev.pack(side=aligment)

        # Defining number of columns
        treev["columns"] = ("1", "2")

        # Defining heading
        treev['show'] = 'headings'

        # Assigning the width and anchor to  the
        # respective columns
        treev.column("1", width=180, anchor='c')
        treev.column("2", width=180, anchor='se')

        # Assigning the heading names to the
        # respective columns
        treev.heading("1", text=column1)
        treev.heading("2", text=column2)
        return treev
    # https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
