"""Defines Map class along with the methods and attributes that it uses."""
import tkinter

from mining.utils import Icon, Tile, map, coordinate


class GUI_Map(tkinter.Toplevel):
    """Serves as the constructor for the Map object.

    Arguments:
        parent (tkinter.Toplevel): Takes in a tkinter top level window
    """

    def __init__(self, parent, title: str, physical_map: map):
        # TODO: Add docstring
        super().__init__(parent)
        self.photo = tkinter.PhotoImage(file="icon.png")
        self.wm_iconphoto(False, self.photo)
        self.geometry("300x300+0+0")
        self.minsize(600, 600)
        self.title(title)
        self.physicalmap = physical_map
        self.log = tkinter.Text(
            self, width=100, height=100, state="normal", wrap="none"
        )
        self.log.pack()

    def prepare_GUI_map(self) -> None:
        """Prepare map by filling it with unknown characters."""
        self.log.config(state="normal")
        for x in range(200):
            for y in range(200):
                self.log.insert(f"{x}.{y}", "\u26F6")
            self.log.insert(f"{x}.200", "\n")
        self.log.config(state="disabled")
    
    def update(self):
        """Updates GUI Map with any updated coordinates that
        the physical map may have"""
        for item in self.physicalmap._stored_tiles_.values():
            self.translate_tile(item)


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
            Icon.EMPTY: " ",
        }
        unicode_character = unicode_dict.get(new_tile.icon, "\u2061")
    
        coordinates = f"{new_tile.coordinate[1]}.{new_tile.coordinate[0]}"
        self.log.insert(coordinates, unicode_character)
        self.log.config(state="disabled")
