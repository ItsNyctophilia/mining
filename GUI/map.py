"""Defines Map class along with the methods and attributes that it uses."""
import tkinter

from utils.icon import Icon
from utils.tile import Tile


class Map(tkinter.Toplevel):
    """Serves as the constructor for the Map object.

    Arguments:
        parent (tkinter.Toplevel): Takes in a tkinter top level window
    """

    def __init__(self, parent, title: str):
        # TODO: Add docstring
        super().__init__(parent)
        self.photo = tkinter.PhotoImage(file="icon.png")
        self.wm_iconphoto(False, self.photo)
        self.geometry("300x300+0+0")
        self.minsize(600, 600)
        self.title(title)
        self.log = tkinter.Text(
            self, width=100, height=100, state="normal", wrap="none"
        )
        self.log.pack()

    def write_up(self, object_at_place: str, x: int, y: int) -> None:
        """Write certain characters to a specific place in the map.

        Arguments:
            object_at_place (str) : defines what specific character should be
                placed at the coordinate.
            x (int) : Specifies what column the character should be placed in.
            y (int) : Specifies what row the character should be placed in.
        """
        unicode_dict = {
            "wall": "\u2589",
            "acid": "\u2600",
            "minerals": "\u2662",
            "drone": "\u26DF",
            "deployment": "\u25BD",
            "unknown": "\u26F6",
        }
        unicode_character = unicode_dict[object_at_place]
        coordinates = f"{y}.{x}"
        self.log.insert(coordinates, unicode_character)

    def prepare_map(self) -> None:
        """Prepare map by filling it with unknown characters."""
        self.log.config(state="normal")
        for x in range(200):
            for y in range(200):
                self.log.insert(f"{x}.{y}", "\u26F6")
            self.log.insert(f"{x}.200", "\n")
        self.log.config(state="disabled")

    def translate_tile(self, new_tile: Tile) -> None:
        """Write a tile object to the map.

        new_tile (Tile) : Specifies the tile that should be written into the
            map
        """
        self.log.config(state="normal")
        unicode_dict = {
            Icon.WALL: "\u2589",
            Icon.ACID: "\u2600",
            Icon.MINERAL: "\u2662",
            Icon.ZERG: "\u26DF",
            Icon.DEPLOY_ZONE: "\u25BD",
            Icon.EMPTY: "\u26F6",
        }
        unicode_character = unicode_dict.get(new_tile.icon, "\u2061")
        print(unicode_character)
        coordinates = f"{new_tile.coordinate.x}.{new_tile.coordinate.y}"
        self.log.insert(coordinates, unicode_character)
        self.log.config(state="disabled")
