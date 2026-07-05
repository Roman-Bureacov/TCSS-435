"""Definitions to be used globally

global definitions.

"""
from enum import Enum

glob_rows = 10
glob_cols = 25
MINOR_PADX = 5
MINOR_PADY = 5

Tile = Enum('Tile', [
    ('EMPTY', 0),
    ('OBSTACLE', 1),
    ('ENTRANCE', 2),
    ('HAZARD', 3),
    ('EXIT', 4)
])