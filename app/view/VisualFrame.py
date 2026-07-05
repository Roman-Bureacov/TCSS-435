"""The description of a visual frame, for a grid of labels

The class defined below is a tk frame that holds ways to store and manipulate a grid of labels.

"""

import tkinter as tk

import numpy as np

"""The class defining a visual tk frame of a grid
"""
class VisualGridFrame(tk.Frame):

    """The initializer for the frame

    Args:
        parent: the parent of this frame
        rows: the positive-number of rows in the grid
        columns: the positive-number of columns in the grid
        tile_width: the positive-number for the visual size of the tiles in pixels
    """
    def __init__(self, parent, rows, columns, tile_width=10):
        super().__init__(parent)
        self.grid_data = np.empty((rows, columns), dtype=object)
        self.grid_canvas = tk.Canvas(self)
        self.tile_width = tile_width
        self.rebuild()

    """Retrieves the tile's x and y coordinates.
    
    Args:
        row: the row to find
        column: the column to find
        
    Returns: the (x, y) coordinates as the tuple (int, int)
    """
    def _tile_canvas_pos(self, row, column):
        return column * self.tile_width, row * self.tile_width

    """Rebuilds the canvas
    
    Tells the visual grid to rebuild the grid. Necessary if changing the dimensions.
    """
    def rebuild(self):
        self.grid_canvas.destroy()
        self.grid_canvas = tk.Canvas(self,
                                     width=(self.grid_data.shape[1] + 1) * self.tile_width,
                                     height=(self.grid_data.shape[0] + 1) * self.tile_width
                                     ) # 1 extra for headers

        # rebuild the row headers
        for r in range(self.grid_data.shape[0]):
            t = str(r)
            x, y = self._tile_canvas_pos(r + 1, 0)
            self.grid_canvas.create_text(
                x + self.tile_width // 2,
                y + self.tile_width // 2,
                text=t
            )


        # rebuild the column headers
        for c in range(self.grid_data.shape[1]):
            t = str(c)
            x, y = self._tile_canvas_pos(0, c + 1)
            self.grid_canvas.create_text(
                x + self.tile_width // 2,
                y + self.tile_width // 2,
                text=t
            )

        # rebuild the grid
        for r in range(self.grid_data.shape[0]):
            for c in range(self.grid_data.shape[1]):
                x, y = self._tile_canvas_pos(r + 1, c + 1)
                self.grid_canvas.create_rectangle(
                    x, y,
                    x + self.tile_width, y + self.tile_width,
                    fill="magenta"
                )

        self.grid_canvas.pack()

