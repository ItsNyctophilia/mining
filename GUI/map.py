"""
Defines Map class along with the methods and attributes that it uses.
"""
import random
import tkinter
from utils.tile import Tile

class Map(tkinter.Toplevel):
    """serves as the constructor for the Map object

    Arguments:
        parent (tktinker.Toplevel): Takes in a tkinter top level window
    """

    def __init__(self, parent, title: str):
        super().__init__(parent)
        self.photo = tkinter.PhotoImage(file='icon.png')
        self.wm_iconphoto(False, self.photo)
        self.geometry("300x300+0+0")
        self.minsize(600, 600)
        self.title(title)
        self.log = tkinter.Text(self, width=100, height=100, state='normal', wrap='none')
        self.log.pack()

    def prepare_map(self) -> None:
        """
        This prepares a map in the beginning by filling it with unknown characters
        """
        self.log.config(state='normal')
        for x in range(200):
            for y in range(200):
                self.log.insert(f'{x}.{y}', u'\u26F6')
            self.log.insert(f'{x}.200', '\n')
        self.log.config(state='disabled')

    def translate_tile(self, new_tile: Tile) -> None:
        """
        This writes a tile object to the map
        new_tile (tile) : Specifies the tile that should be written into the map
        """
        self.log.config(state='normal')
        unicode_dict = {
            '#': u'\u2589',
            '~': u'\u2600',
            '*': u'\u2662',
            'Z': u'\u26DF',
            '_': u'\u25BD',
            'unknown': u'\u26F6'
        }
        unicode_character = unicode_dict[new_tile.icon]
        print(unicode_character)
        coordinates = f'{new_tile.coordinate.x}.{new_tile.coordinate.y}'
        self.log.insert(coordinates, unicode_character)
        self.log.config(state='disabled')
