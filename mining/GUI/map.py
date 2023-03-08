"""Defines Map class along with the methods and attributes that it uses."""
import tkinter

from mining.utils import Icon, Map, Tile


class GUI_Map(tkinter.Toplevel):
    """Serves as the constructor for the Map object.

    Arguments:
        parent (tkinter.Toplevel): Takes in a tkinter top level window
    """

    def __init__(self, parent, title: str, physical_map: Map) -> None:
        """Initialize the GUI map.

        Args:
            parent (_type_): The parent window.
            title (str): The title of this window.
            physical_map (Map): The actual data for the map window.
        """
        super().__init__(parent)
        self.photo = tkinter.PhotoImage(file="icon.png")
        self.wm_iconphoto(False, self.photo)
        self.geometry("300x300+0+0")
        self.minsize(600, 600)
        self.title(title)
        self.physical_map = physical_map
        self.log = tkinter.Text(
            self, width=100, height=100, state="normal", wrap="none"
        )
        self.log.pack()
        self.log.font = ("TkFixedFont", 16)

    def prepare_GUI_map(self) -> None:
        """Prepare map by filling it with unknown characters."""
        self.log.config(state="normal")
        for x in range(200):
            for y in range(200):
                self.log.insert(f"{x}.{y}", "\u02FD")
            self.log.insert(f"{x}.200", "\n")
        self.log.config(state="disabled")

    def update(self):
        """Update GUI Map with any updated coordinates."""
        for item in self.physical_map._stored_tiles_.values():
            self.translate_tile(item)

    def translate_tile(self, new_tile: Tile) -> None:
        """Write a tile object to the map.

        new_tile (Tile) : Specifies the tile that should be written into the
            map
        """
        self.log.config(state="normal")
        unicode_dict = {
            Icon.WALL: "\u00A4",
            Icon.ACID: "\u05e1",
            Icon.MINERAL: "\u0275",
            Icon.ZERG: "\u017e",
            Icon.DEPLOY_ZONE: "\u02c5",
            Icon.EMPTY: " ",
        }
        unicode_character = unicode_dict.get(new_tile.icon, "\u2061")

        coordinates = f"{new_tile.coordinate.y}.{new_tile.coordinate.x}"
        self.log.insert(coordinates, unicode_character)
        self.log.config(state="disabled")
