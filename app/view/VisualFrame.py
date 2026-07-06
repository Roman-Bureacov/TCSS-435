"""The description of a visual frame, for a grid of labels

The class defined below is a tk frame that holds ways to store and manipulate a grid of labels.

"""

import tkinter as tk
import numpy as np
from app.model.navmap import Tile

class VisualGridFrame(tk.Frame):
    """The class defining a visual tk frame of a grid
    """

    def __init__(self, parent, navmap, tile_width=10):
        """The initializer for the frame

            Args:
                parent: the parent of this frame
                navmap: the navmap to work with
                tile_width: the positive-number for the visual size of the tiles in pixels
        """
        super().__init__(parent)
        self.grid_canvas = tk.Canvas(self)
        self.navmap = navmap
        self.grid_tiles = None
        self.tile_width = tile_width
        self.rebuild()

    def _tile_canvas_pos(self, row, column):
        """Retrieves the tile's x and y coordinates.

            Args:
                row: the row to find
                column: the column to find

            Returns: the (x, y) coordinates as the tuple (int, int)
        """
        return column * self.tile_width, row * self.tile_width

    def rebuild(self):
        """Rebuilds the canvas

            Tells the visual grid to rebuild the grid. Necessary if changing the dimensions.
        """
        self.grid_canvas.destroy()
        rows, columns = self.navmap.shape
        self.grid_canvas = tk.Canvas(self,
                                     width=(columns + 1) * self.tile_width,
                                     height=(rows + 1) * self.tile_width
                                     ) # 1 extra for headers

        self.grid_tiles = np.empty((rows, columns), dtype=object)

        # rebuild the row headers
        for r in range(rows):
            t = str(r)
            x, y = self._tile_canvas_pos(r + 1, 0)
            self.grid_canvas.create_text(
                x + self.tile_width // 2,
                y + self.tile_width // 2,
                text=t
            )


        # rebuild the column headers
        for c in range(columns):
            t = str(c)
            x, y = self._tile_canvas_pos(0, c + 1)
            self.grid_canvas.create_text(
                x + self.tile_width // 2,
                y + self.tile_width // 2,
                text=t
            )

        # rebuild the grid
        for r in range(rows):
            for c in range(columns):
                x, y = self._tile_canvas_pos(r + 1, c + 1) # offset from the headers
                # draw and store the working grid tile
                self.grid_tiles[r, c] = t = self.grid_canvas.create_rectangle(
                    x, y,
                    x + self.tile_width, y + self.tile_width,
                    fill="magenta"
                )
                self._draw_tile(r, c, t)

        self.grid_canvas.pack()

    def redraw(self):
        """Redraws the entire grid.

            Redraws all the tiles. Does not redraw the numbers.
            Useful if changing tiles but not grid dimensions.
        """
        rows, columns = self.navmap.shape
        for r in range(rows):
            for c in range(columns):
                self._draw_tile(r, c, self.navmap[r, c])

    def _draw_tile(self, row, column, tile):
        """Draw the tile specified at the row and column.

            Args:
                row: the row to draw at
                column: the column to draw at
                tile: the tile to draw
        """
        grid_tile = self.grid_tiles[row, column]
        color = "magenta" # undefined color
        match tile:
            case Tile.EMPTY:
                color = "white"
            case Tile.OBSTACLE:
                color = "gray"
            case Tile.ENTRANCE:
                color = "green"
            case Tile.HAZARD:
                color = "red"
            case Tile.EXIT:
                color = "black"

        self.grid_canvas.itemconfig(grid_tile, fill=color)
