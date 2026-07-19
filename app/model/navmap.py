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
        self.grid = np.full((self.rows, self.columns), dtype=Tile, fill_value=Tile.EMPTY)
        self.shape = self.grid.shape
        self.entrance = None
        self.exit = None

    def __getitem__(self, index):
        row, col = index
        return self.grid[row, col]

    def __setitem__(self, index, value):
        row, col = index
        self.grid[row, col] = value

    def resize(self, rows, columns):
        # noinspection PyDeprecation
        # reason: numpy documentation says nothing about this being deprecated
        np.ndarray.resize(self.grid, rows, columns, refcheck=False)
        self.shape = self.grid.shape