"""This serves to define the dashboard class.

Defines the attributes it has along with the methods that it uses.
"""
import tkinter
from tkinter import ttk
from typing import Dict

from zerg.drones import Drone


class Dashboard(tkinter.Toplevel):
    """Serves as blueprint for the dashboard class."""

    def __init__(self, parent):
        """Serve as the constructor for the Dashboard object.

        Arguments:
            parent (tkinter.Toplevel): Takes in a tkinter top level window
        """
        super().__init__(parent)
        self.photo = tkinter.PhotoImage(file="icon.png")

        self.configure(bg="#2C292C")
        # Configure the style of Heading in Treeview widget
        self.wm_iconphoto(False, self.photo)
        self.title("Overlord's Dashboard")
        self.map_tree = self.make_tree("Window Title", "Map ID")
        self.map_tree.grid(row=0, column=0, padx=(20, 20), pady=(20, 20))
        self.turn_tree = self.make_tree("Tick", "Action")
        self.turn_tree.grid(row=0, column=1, padx=(20, 20), pady=(20, 20))
        self.drone_tree = self.make_drone_tree()
        self.drone_tree.grid(
            row=1, column=0, columnspan=2, padx=(20, 20), pady=(20, 20)
        )
        #

    # https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def make_tree(self, column1: str, column2: str) -> ttk.Treeview:
        """Build trees for the dashboard to use.

        Dashboards typically serve spreadsheets in the gui.

        Arguments:
            column1 (string) : the name for this first column in the table
            column2 (string) : the name for the second column in the table
        """
        style = ttk.Style()
        style.theme_use("clam")

        # Configure the style of Heading in Treeview widget
        style.configure("Treeview.Heading", background="#ad73ac")

        # Using treeview widget
        tree_view = ttk.Treeview(self, selectmode="browse")

        # Defining number of columns
        tree_view["columns"] = ("1", "2")

        # Defining heading
        tree_view["show"] = "headings"

        # Assigning the width and anchor to  the
        # respective columns
        tree_view.column("1", width=180, anchor="center")
        tree_view.column("2", width=180, anchor="se")

        # Assigning the heading names to the
        # respective columns
        tree_view.heading("1", text=column1)
        tree_view.heading("2", text=column2)
        return tree_view

    # https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/

    # https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
    def make_drone_tree(self) -> ttk.Treeview:
        """Build drone tree for dashboard to best keep track of drones.

        This will ensure the user knows about each drone
        """
        s = ttk.Style()
        s.theme_use("clam")

        # Configure the style of Heading in Treeview widget
        s.configure("Treeview.Heading", background="#ad73ac")

        # Using treeview widget
        tree_view = ttk.Treeview(self, selectmode="browse")

        # Defining number of columns
        tree_view["columns"] = ("1", "2", "3", "4", "5")

        # Defining heading
        tree_view["show"] = "headings"

        # Assigning the width and anchor to  the
        # respective columns
        tree_view.column("1", width=180, anchor="center")
        tree_view.column("2", width=180, anchor="se")
        tree_view.column("3", width=120, anchor="se")
        tree_view.column("4", width=120, anchor="se")
        tree_view.column("5", width=120, anchor="se")

        # Assigning the heading names to the
        # respective columns
        tree_view.heading("1", text="Drone ID")
        tree_view.heading("2", text="Drone Type")
        tree_view.heading("3", text="Health")
        tree_view.heading("4", text="Capacity")
        tree_view.heading("5", text="Moves")
        return tree_view

    # https://www.geeksforgeeks.org/python-tkinter-treeview-scrollbar/
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

    def fill_map_table(self, map_dict: dict) -> None:
        """Fill map table with new maps that come from a dictionary.

        Arguments:
            map_dict (dict) : This dictionary should contain all the maps that
                will be added to the table.
        """
        window_counter = 0
        self.clear_table(self.map_tree)
        for entry in map_dict.values():
            window_counter += 1
            self.map_tree.insert(
                "",
                "end",
                text="Listbox",
                values=(f"Map {window_counter}", entry),
            )
