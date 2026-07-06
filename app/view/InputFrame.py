"""This file contains the information necessary for the input frame of the user interface.

"""
import tkinter as tk
from enum import Enum

from app.model.globs import MINOR_PADY, MINOR_PADX, glob_rows, glob_cols, glob_empty_tile_weight, \
    glob_obstacle_tile_weight


class InputFrame(tk.Frame):
    """Class representing a frame of the user interface.

    This class handles the input to the user interface to manipulate the grid.

    """

    EVENTS = Enum('EVENTS',
                  [
                  ('RESIZE', "<<resize_grid>>"),
                  ('RANDOMIZE', "<<randomize_maze>>"),
                  ])

    def __init__(self, parent):
        """Constructor for the InputFrame class.

        Args:
            parent: Parent of the window.
        """
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)  # so the column can expand in width
        self.input_row_resize = tk.IntVar(value=glob_rows)
        self.input_col_resize = tk.IntVar(value=glob_cols)
        self.input_empty_weight = tk.IntVar(value=glob_empty_tile_weight)
        self.input_obstacle_weight = tk.IntVar(value=glob_obstacle_tile_weight)

        self._setup_row_col_input()
        self._setup_randomization_input()

    def _setup_row_col_input(self):
        """sets up the row/column count input for the user interface."""


        # the target visual is: shape: ([  ],[  ]) |Resize|

        row_col_shape_frame = tk.Frame(self, padx=MINOR_PADX, pady=MINOR_PADY)
        row_col_label = tk.Label(row_col_shape_frame, text="Shape: (")
        row_col_label.grid(row=0, column=0)

        row_input = tk.Entry(row_col_shape_frame, width=5, textvariable=self.input_row_resize)
        row_input.grid(row=0, column=1)

        tk.Label(row_col_shape_frame, text=",").grid(row=0, column=2)

        col_input = tk.Entry(row_col_shape_frame, width=5, textvariable=self.input_col_resize)
        col_input.grid(row=0, column=3)

        tk.Label(row_col_shape_frame, text=")").grid(row=0, column=4)

        # submission button
        def _row_col_configure_command():
            self.input_row_resize = row_input.get()
            self.input_col_resize = col_input.get()
            self.event_generate(self.EVENTS.RESIZE.value)

        row_col_button = tk.Button(row_col_shape_frame, text="Resize",
                                   padx=MINOR_PADX, pady=MINOR_PADY,
                                   command=_row_col_configure_command)
        row_col_button.grid(row=0, column=5)

        row_col_shape_frame.grid(row=0, column=0) # this widget sits at the left

    def _setup_randomization_input(self):
        """Sets up the randomization for the grid in the user interface."""
        # randomize button
        randomization_frame = tk.Frame(self, padx=MINOR_PADX, pady=MINOR_PADY)

        # empty tile weight
        empty_tile_weight_frame = tk.Frame(randomization_frame)
        empty_tile_weight_label = tk.Label(empty_tile_weight_frame, text="Empty tile weight: ")
        empty_tile_weight_input = tk.Entry(empty_tile_weight_frame, width=5, textvariable=self.input_empty_weight)

        empty_tile_weight_label.grid(row=0, column=0)
        empty_tile_weight_input.grid(row=0, column=1)
        empty_tile_weight_frame.grid(row=0, column=0,
                                     padx=MINOR_PADX, pady=MINOR_PADY,
                                     sticky="e")


        # obstacle tile weight
        obst_tile_weight_frame = tk.Frame(randomization_frame)
        obst_tile_weight_label = tk.Label(obst_tile_weight_frame, text="Obstacle tile weight: ")
        obst_tile_weight_input = tk.Entry(obst_tile_weight_frame, width=5, textvariable=self.input_obstacle_weight)

        obst_tile_weight_label.grid(row=0, column=0)
        obst_tile_weight_input.grid(row=0, column=1)
        obst_tile_weight_frame.grid(row=1, column=0,
                                    padx=MINOR_PADX, pady=MINOR_PADY,
                                    sticky="e")


        # submission button
        def _randomize_maze_command():
            self.input_empty_weight = empty_tile_weight_input.get()
            self.input_obstacle_weight = obst_tile_weight_input.get()
            self.event_generate(self.EVENTS.RANDOMIZE.value)

        randomize_button = tk.Button(randomization_frame, text="Randomize Map",
                                     padx=MINOR_PADX, pady=MINOR_PADY,
                                     command=_randomize_maze_command)
        randomize_button.grid(row=0, column=1, rowspan=2)

        randomization_frame.grid(row=0, column=1, sticky="ew")




