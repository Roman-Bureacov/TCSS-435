"""This file contains the information necessary for the input frame of the user interface.

"""
import tkinter as tk
from tkinter import ttk
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
                    ('PERFORM_BFS', "<<perform_bfs>>"),
                    ('PERFORM_DFS', "<<perform_dfs>>"),
                    ('PERFORM_UCS', "<<perform_ucs>>"),
                    ('PERFORM_ASS', "<<perform_ass>>"),
                ])

    _SEARCH_OPTIONS = Enum('_SEARCH_OPTIONS',
                           [
                               ('BREADTH_FIRST_SEARCH', "Breadth-First Search"),
                               ('DEPTH_FIRST_SEARCH', "Depth-First Search"),
                               ('UNIFORM_COST_SEARCH', "Uniform Cost Search"),
                               ('A_STAR_SEARCH', "A* Search"),
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

        self.stats_labels = dict()

        self._setup_row_col_input()
        self._setup_randomization_input()
        self._setup_search_input()
        self._setup_search_stats()

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

    def _setup_search_input(self):
        """sets up the combo box for starting searches on the user interface."""

        button_frame = tk.Frame(self, padx=MINOR_PADX, pady=MINOR_PADY)

        # Combo box of search algorithms
        combo_box = ttk.Combobox(button_frame,
                                 values=[
                                     InputFrame._SEARCH_OPTIONS.BREADTH_FIRST_SEARCH.value,
                                     InputFrame._SEARCH_OPTIONS.DEPTH_FIRST_SEARCH.value,
                                     InputFrame._SEARCH_OPTIONS.UNIFORM_COST_SEARCH.value,
                                     InputFrame._SEARCH_OPTIONS.A_STAR_SEARCH.value,
                                 ],
                                 width=20)
        combo_box.grid(row=0, column=0)

        # the initiator
        def search_button_command():
            opt = combo_box.get()
            match opt:
                case InputFrame._SEARCH_OPTIONS.BREADTH_FIRST_SEARCH.value:
                    self.event_generate(self.EVENTS.PERFORM_BFS.value)
                case InputFrame._SEARCH_OPTIONS.DEPTH_FIRST_SEARCH.value:
                    self.event_generate(self.EVENTS.PERFORM_DFS.value)
                case InputFrame._SEARCH_OPTIONS.UNIFORM_COST_SEARCH.value:
                    self.event_generate(self.EVENTS.PERFORM_UCS.value)
                case InputFrame._SEARCH_OPTIONS.A_STAR_SEARCH.value:
                    self.event_generate(self.EVENTS.PERFORM_ASS.value)

        search_button = tk.Button(button_frame, text="Search",
                                  width=20,
                                  command=search_button_command)
        search_button.grid(row=1, column=0)

        button_frame.grid(row=1, column=1,)

    def _setup_search_stats(self):
        """sets up the stats text below the search buttons."""

        stats_frame = tk.Frame(self, padx=MINOR_PADX, pady=MINOR_PADY)

        # path length label
        path_length_label = tk.Label(stats_frame, text="Path Length: ")
        path_length_label.config(width=20)
        path_length_label.grid(row=0, column=0, sticky="w")
        path_length_stat_label = tk.Label(stats_frame, text="N/A")
        path_length_stat_label.grid(row=0, column=1, sticky="w")
        self.stats_labels["path_length"] = path_length_stat_label

        # nodes expanded label
        nodes_expanded_label = tk.Label(stats_frame, text="Nodes Expanded: ")
        nodes_expanded_label.config(width=20)
        nodes_expanded_label.grid(row=1, column=0, sticky="w")
        nodes_expanded_stat_label = tk.Label(stats_frame, text="N/A")
        nodes_expanded_stat_label.grid(row=1, column=1, sticky="w")
        self.stats_labels["nodes_expanded"] = nodes_expanded_stat_label

        # execution time label
        time_label = tk.Label(stats_frame, text="Time (ns): ")
        time_label.config(width=20)
        time_label.grid(row=2, column=0, sticky="w")
        time_stat_label = tk.Label(stats_frame, text="N/A")
        time_stat_label.grid(row=2, column=1, sticky="w")
        self.stats_labels["time"] = time_stat_label

        stats_frame.grid(row=1, column=0)

    def update_search_stats(self, stats):
        """updates this frame's search statistics using the relevant search stats object.

        Args:
            stats: the stats object generated from a search
        """

        self.stats_labels["path_length"].config(text=stats.path_length)
        self.stats_labels["nodes_expanded"].config(text=stats.nodes_expanded)
        self.stats_labels["time"].config(text=stats.translate_time(stats.time))

