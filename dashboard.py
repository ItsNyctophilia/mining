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
        self.photo = tkinter.PhotoImage(file='icon.png')

        self.wm_iconphoto(False, self.photo)
        self.title("Overlord's Dashboard")
        self.map_tree = self.make_tree("top", "Map", "Map ID")
        self.map_tree.grid(row=0, column=0)
        self.turn_tree = self.make_tree("top", "Tick", "Action")
        self.turn_tree.grid(row=0, column=1)
        self.turn_tree1 = self.make_fat_tree("top", "Tick", "Action")
        self.turn_tree1.grid(row=1,column = 0, columnspan = 2)
        # self.map_tree.insert('', 'end', text='Listbox', values=('15KB', 'Yesterday'))

    # https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def make_tree(self, aligment, column1, column2):
        """
        Builds trees for the dasboard to use, dashboards typically serve spreadhsheets in the gui.
        """

        s = ttk.Style()
        s.theme_use('clam')

        # Configure the style of Heading in Treeview widget
        s.configure('Treeview.Heading', background="green3")


        # Using treeview widget
        treev = ttk.Treeview(self, selectmode='browse')

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

        # https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def make_fat_tree(self, aligment, column1, column2):
        """
        Builds trees for the dasboard to use, dashboards typically serve spreadhsheets in the gui.
        """

        s = ttk.Style()
        s.theme_use('clam')

        # Configure the style of Heading in Treeview widget
        s.configure('Treeview.Heading', background="green3")


        # Using treeview widget
        treev = ttk.Treeview(self, selectmode='browse')

        # Defining number of columns
        treev["columns"] = ("1", "2", "3", "4")

        # Defining heading
        treev['show'] = 'headings'

        # Assigning the width and anchor to  the
        # respective columns
        treev.column("1", width=180, anchor='c')
        treev.column("2", width=180, anchor='se')
        treev.column("3", width=180, anchor='se')
        treev.column("4", width=180, anchor='se')

        # Assigning the heading names to the
        # respective columns
        treev.heading("1", text=column1)
        treev.heading("2", text=column2)
        treev.heading("3", text="a")
        treev.heading("4", text="b")
        return treev
    # https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
