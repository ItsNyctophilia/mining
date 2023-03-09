"""This serves to define the dashboard class.

Defines the attributes it has along with the methods that it uses.
"""
import tkinter
from tkinter import ttk
from typing import Dict
from mining.utils.map import Map
from .map import GUI_Map
from mining.zerg_units.drones import Drone


class Dashboard(tkinter.Toplevel):
    """Serves as blueprint for the dashboard class.
    This outlines the attributes and methods needed.
    """

    def __init__(self, parent):
        """Serve as the constructor for the Dashboard object.

        Arguments:
            parent (tkinter.Toplevel): Takes in a tkinter top level window
        """
        super().__init__(parent)
        self.photo = tkinter.PhotoImage(file="icon.png")

        self.configure(bg="#2C292C")
        self.map_dict = {}
        self.map_count = 0
        # Configure the style of Heading in Treeview widget
        self.wm_iconphoto(False, self.photo)
        self.prep_dashboard_trees()
        self.title("Overlord's Dashboard")

    # https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def make_tree(self, column_dictionary: Dict[str, int]) -> ttk.Treeview:
        """Build trees for the dashboard to use.

        Dashboards typically serve spreadsheets in the gui.

        Arguments:
            column_dictionary: Contains dictionaries and width values for
            each column.
        """
        style = ttk.Style()
        style.theme_use("clam")

        # Configure the style of Heading in Treeview widget
        style.configure("Treeview.Heading", background="#ad73ac")

        # Using treeview widget
        tree_view = ttk.Treeview(self, selectmode="browse")

        # Defining number of columns
        tree_view["columns"] = tuple(column_dictionary)

        # Defining heading
        tree_view["show"] = "headings"

        for column_count, (column, width) in enumerate(
                column_dictionary.items()
        ):
            string_column = str(column_count)
            tree_view.column(string_column, width=width, anchor="se")
            tree_view.heading(string_column, text=column)
        return tree_view

    def create_map_gui(self, example_map: Map) -> None:
        """
        This creates a GUI for every map that the overlord has.
        """

        self.map_count += 1
        new_map = GUI_Map(self, f'Map {self.map_count}', example_map)
        new_map.prepare_GUI_map()
        self.map_dict[new_map] = example_map
        self.add_map_table(example_map)

    def update_maps(self) -> None:
        """
        Updates the GUI Map with what it's physical map contains.
        """
        for gui_map, map_id in self.map_dict.items():
            gui_map.update()

    # https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def prep_dashboard_trees(self) -> None:
        """
        Prepare the three tree views in the dashboard.
        """

        map_dict = {"Window Title": 180, "Map ID": 180}

        action_tree = {"Action": 180, "Tick": 180}

        drone_tree = {
            "Drone ID": 180,
            "Drone Type": 180,
            "Health": 120,
            "Capacity": 120,
            "Moves": 120,
        }
        padding = (20, 20)
        self.map_tree = self.make_tree(map_dict)
        self.map_tree.grid(row=0, column=0, padx=padding, pady=padding)
        self.turn_tree = self.make_tree(action_tree)
        self.turn_tree.grid(row=0, column=1, padx=padding, pady=padding)
        self.drone_tree = self.make_tree(drone_tree)
        self.drone_tree.grid(
            row=1, column=0, columnspan=2, padx=padding, pady=padding
        )

    def add_drone_to_tree(self, new_drone: Drone) -> None:
        """Add a drone to the drone tree in the gui.

        Arguments:
            new_drone (Drone) : this is the drone we are adding to the tree in
                the dashboard.
        """
        type_of_drone = type(new_drone).__name__
        self.drone_tree.insert(
            "",
            "end",
            text="Listbox",
            values=(
                id(new_drone),
                type_of_drone,
                new_drone.health,
                new_drone.capacity,
                new_drone.moves,
            ),
        )

    def clear_table(self, tree: ttk.Treeview) -> None:
        """Clear any of the tables in the GUI.

        Arguments:
            tree (ttk.Treeview): This is the tree we will be clearing.
        """
        for entry in tree.get_children():
            tree.delete(entry)

    def update_drone_table(self, drone_dict: Dict[int, Drone]) -> None:
        """Clear drone table and adds a new dictionary of drones to the table.

        Arguments:
            drone_dict (dict) : This dictionary should contain all the drones
                that will be added to the drone table.
        """
        self.clear_table(self.drone_tree)
        for entry in drone_dict.values():
            self.add_drone_to_tree(entry)

    def add_map_table(self, new_map: Map) -> None:
        """Fill map table with new maps that come from a dictionary.

        Arguments:
            new_map (map) : The map that will have it's ID added to the table
        """
        self.map_tree.insert(
            "",
            "end",
            text="Listbox",
            values=(f"Map {self.map_count}", id(new_map)),
        )
