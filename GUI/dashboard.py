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
        self.prep_dashboard_trees()
        self.title("Overlord's Dashboard")

    # https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def make_tree(self, column_dictionary: dict) -> None:
        """
        Builds trees for the dashboard to use, dashboards typically serve spreadsheets in the gui.
        Arguments:
            column_dictionary: Contains dictionaries and width values for 
            each column.
        """

        s = ttk.Style()
        s.theme_use('clam')

        # Configure the style of Heading in Treeview widget
        s.configure('Treeview.Heading', background="#ad73ac")

        # Using treeview widget
        treev = ttk.Treeview(self, selectmode='browse')

        # Defining number of columns
        treev["columns"] = tuple(column_dictionary)

        # Defining heading
        treev['show'] = 'headings'

        column_count = 0
        for column, width in column_dictionary.items():
            string_column = str(column_count)
            treev.column(string_column, width=width, anchor='se')
            treev.heading(string_column, text=column)
            column_count += 1

        return treev

    # https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def prep_dashboard_trees(self):
        """
        prepares the three treeviews in the dashboard
        """
        map_dict = {
                'Window Title': 180,
                'Map ID': 180
                }

        action_tree = {
                'Action' : 180,
                'Tick' : 180
                }

        drone_tree = {
                'Drone ID' : 180,
                'Drone Type' : 180,
                'Health' : 120,
                'Capacity' : 120,
                'Moves' : 120
                }
        padding = (20, 20)
        self.map_tree = self.make_tree(map_dict)
        self.map_tree.grid(row=0, column=0, padx= padding, pady=padding)
        self.turn_tree = self.make_tree(action_tree)
        self.turn_tree.grid(row=0, column=1, padx=padding, pady=padding)
        self.drone_tree = self.make_tree(drone_tree)
        self.drone_tree.grid(row=1, column=0, columnspan=2,padx=padding, pady=padding)

    def add_drone_to_tree(self, new_drone: Drone) -> None:
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

    def update_drone_table(self, drone_dict: dict) -> None:
        """
        clears drone table and adds a new dictionary of drones to the table
        Arguments:
            drone_dict (dict) : This dictionary should contain all the drones that will be added to
            the drone table.
        """
        self.clear_table(self.drone_tree)
        for entry in drone_dict.values():
            self.add_drone_to_tree(entry)

    def fill_map_table(self, map_dict: dict) -> None:
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
