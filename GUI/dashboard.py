"""
This serves to define the dashboard clas, defines the attributes it has along with 
the methods that it uses.

"""
import random
import tkinter
from tkinter import ttk
from zerg.drones.drone import Drone
from zerg.drones.scout import ScoutDrone
from zerg.drones.miner import MinerDrone


class Dashboard(tkinter.Toplevel):
    """
    serves as blueprint for the dashboard class
    """

    def __init__(self, parent):
        """serves as the constructor for the Dashboard object

        Arguments:
            parent (tktinker.Toplevel): Takes in a tkinter top level window
        """
        super().__init__(parent)
        self.photo = tkinter.PhotoImage(file='icon.png')

        self.configure(bg='#2C292C')
        # Configure the style of Heading in Treeview widget
        self.wm_iconphoto(False, self.photo)
        self.title("Overlord's Dashboard")
        self.map_tree = self.make_tree("Window Title", "Map ID")
        self.map_tree.grid(row=0, column=0, padx=(20, 20), pady=(20, 20))
        self.turn_tree = self.make_tree("Tick", "Action")
        self.turn_tree.grid(row=0, column=1, padx=(20, 20), pady=(20, 20))
        self.drone_tree = self.make_drone_tree()
        self.drone_tree.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(20, 20))
        # 

    # https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def make_tree(self, column1, column2):
        """
        Builds trees for the dashboard to use, dashboards typically serve spreadsheets in the gui.
        Arguments:
            column1 (string) : the name for this first column in the table
            column2 (string) : the name for the second column in the table
        """

        s = ttk.Style()
        s.theme_use('clam')

        # Configure the style of Heading in Treeview widget
        s.configure('Treeview.Heading', background="#ad73ac")

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
    def make_drone_tree(self):
        """
        Builds drone tree for dashboard to best keep track of drones, This will ensure the user knows about each drone
        """

        s = ttk.Style()
        s.theme_use('clam')

        # Configure the style of Heading in Treeview widget
        s.configure('Treeview.Heading', background="#ad73ac")

        # Using treeview widget
        treev = ttk.Treeview(self, selectmode='browse')

        # Defining number of columns
        treev["columns"] = ("1", "2", "3", "4", "5")

        # Defining heading
        treev['show'] = 'headings'

        # Assigning the width and anchor to  the
        # respective columns
        treev.column("1", width=180, anchor='c')
        treev.column("2", width=180, anchor='se')
        treev.column("3", width=120, anchor='se')
        treev.column("4", width=120, anchor='se')
        treev.column("5", width=120, anchor='se')

        # Assigning the heading names to the
        # respective columns
        treev.heading("1", text="Drone ID")
        treev.heading("2", text="Drone Type")
        treev.heading("3", text="Health")
        treev.heading("4", text="Capacity")
        treev.heading("5", text="Moves")
        return treev

    # https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def add_drone_to_tree(self, new_drone):
        """
        Adds a drone to the drone tree in the gui
        Arguments:
            new_drone (drone) : this is the drone we are adding to the tree in the dashboard
        """
        typeofdrone = type(new_drone).__name__
        self.drone_tree.insert('', 'end', text='Listbox', values=(
        id(new_drone), typeofdrone, new_drone.health, new_drone.capacity, new_drone.moves))

    def clear_table(self, tree):
        """
        clears any of the tables in the GUI
        Arguments:
            tree (Tktinker.treeview): This is the tree we will be clearing.
        """
        for entry in tree.get_children():
            tree.delete(entry)

    def update_drone_table(self, drone_dict):
        """
        clears drone table and adds a new dictionary of drones to the table
        Arguments:
            drone_dict (dict) : This dictionary should contain all the drones that will be added to
            the drone table.
        """
        self.clear_table(self.drone_tree)
        for entry in drone_dict.values():
            self.add_drone_to_tree(entry)

    def fill_map_table(self, map_dict):
        """
        fills map table with new maps that come from a dictionary
        Arguments:
            map_dict (dict) : This dictionary should contain all the maps that will be added
            to the table
        """
        window_counter = 0
        self.clear_table(self.map_tree)
        for entry in map_dict.values():
            window_counter += 1
            self.map_tree.insert('', 'end', text='Listbox', values=(f'Map {window_counter}', entry))
