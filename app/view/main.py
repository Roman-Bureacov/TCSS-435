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
                        padx=MINOR_PADX, pady=MINOR_PADY) # child of root

# set up the row headers
visual_grid = VisualGridFrame(visual_frame, maze, tile_width=25)
visual_grid.pack()
visual_frame.pack()

# second frame, below the grid, the input
input_frame = InputFrame(root) # child of root

input_frame.configure(width=500, height=100, padx=MINOR_PADX, pady=MINOR_PADY)
input_frame.pack()
input_frame.pack_propagate(False)

root.mainloop()