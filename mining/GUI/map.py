"""Defines Map class along with the methods and attributes that it uses."""
import tkinter

from mining.utils import Map, Tile


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
        self.prepare_GUI_map()

    def prepare_GUI_map(self) -> None:
        """Prepare map by filling it with unknown characters."""
        self.log.config(state="normal")
        for x in range(200):
            for y in range(200):
                # self.log.insert(f"{x}.{y}", "\u02FD")
                self.log.insert(f"{x}.{y}", "?")
            self.log.insert(f"{x}.200", "\n")
        self.log.config(state="disabled")

    def update(self) -> None:
        """Update GUI Map with any updated coordinates."""
        for tile in self.physical_map._stored_tiles_.values():
            self.translate_tile(tile)

    def translate_tile(self, new_tile: Tile) -> None:
        """Write a tile object to the map.

        new_tile (Tile) : Specifies the tile that should be written into the
            map
        """
        self.log.config(state="normal")
        # unicode_character = new_tile.icon.unicode() if new_tile.icon else "\u2061"
        unicode_character = new_tile.icon.value if new_tile.icon else "?"
        coordinates = f"{new_tile.coordinate.x}.{new_tile.coordinate.y}"
        self.log.insert(coordinates, unicode_character)
        self.log.config(state="disabled")
