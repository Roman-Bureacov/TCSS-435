"""This file contains information on the navmap file and associates.

The navmap is a simple wrapper for the numpy 2-dimensional array.

"""

import numpy as np
from enum import Enum

"""Enum defining what tiles represent"""
Tile = Enum('Tile', [
    ('EMPTY', 0),
    ('OBSTACLE', 1),
    ('ENTRANCE', 2),
    ('HAZARD', 3),
    ('EXIT', 4)
])

class Navmap:
    """Defines the navmap.

    Args:
        rows: the number of rows in the navmap.
        columns: the number of columns in the navmap.
    """
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = np.zeros((self.rows, self.columns), dtype=Tile)
        self.shape = (self.rows, self.columns)

        for r in range(self.rows):
            for c in range(self.columns):
                self.grid[r, c] = Tile.EMPTY

    """Retrieves the tile at the row and column.
    
    Args:
        row: the row to look at
        column: the column to look at
        
    Returns:
        The tile at the row and column as its enum representation.
    """
    def get_tile(self, row, column):
        return self.grid[row, column]

    def __getitem__(self, index):
        row, col = index
        return self.grid[row, col]

    def __setitem__(self, index, value):
        row, col = index
        self.grid[row, col] = value

    """Sets the tile at the row and column.
    
    Args:
        row: the row to look at
        column: the column to look at
        tile: the new tile to place
    """
    def set_tile(self, row, column, tile):
        self.grid[row, column] = tile

