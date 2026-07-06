"""This file functions as the entry point for the user interface

"""

import tkinter as tk

from app.model import navmap_util
from app.model.navmap import Navmap

from app.model.globs import glob_rows, glob_cols, MINOR_PADX, MINOR_PADY
from app.view.InputFrame import InputFrame
from app.view.VisualFrame import VisualGridFrame

# SECTION: param
frame_width = 800
frame_height = 500

tile_width = 25

maze = Navmap(glob_rows, glob_cols)

# SECTION: user interface

root = tk.Tk()
root.configure(borderwidth=10)

root.title("App")
root.geometry(f"{frame_width}x{frame_height}")

label = tk.Label(root, text="Hello World")
label.pack()

# first frame, the grid, the visual part
visual_frame = tk.Frame(root,
                        width=frame_width, height=frame_height,
                        padx=MINOR_PADX, pady=MINOR_PADY)

visual_grid = VisualGridFrame(visual_frame, maze, tile_width=25)
visual_grid.pack()
visual_frame.pack()

# second frame, below the grid, the input
input_frame = InputFrame(root)

input_frame.configure(width=500, height=100, padx=MINOR_PADX, pady=MINOR_PADY)
input_frame.pack()
input_frame.pack_propagate(False)

# event handling
def handle_resize_event(e):
    r, c = input_frame.input_row_resize, input_frame.input_col_resize
    # simple rejection
    try:
        r = int(r)
        c = int(c)
        if r < 1 or c < 1: raise ValueError
    except ValueError:
        print("Unacceptable input on row-column resize")
        return

    maze.resize(r, c)
    visual_grid.rebuild()


def handle_randomize_event(e):
    obstacle_weight, empty_weight = input_frame.input_obstacle_weight, input_frame.input_empty_weight
    # simple rejection
    try:
        obstacle_weight = int(obstacle_weight)
        empty_weight = int(empty_weight)
        if obstacle_weight < 1 or empty_weight < 1: raise ValueError
    except ValueError:
        print("Unacceptable input on tile weights on randomization")
        return

    navmap_util.randomize(maze,
                          obstacle_weight=obstacle_weight,
                          empty_weight=empty_weight
                          )
    visual_grid.redraw()
    pass

input_frame.bind(InputFrame.EVENTS.RESIZE.value, handle_resize_event)
input_frame.bind(InputFrame.EVENTS.RANDOMIZE.value, handle_randomize_event)

root.mainloop()