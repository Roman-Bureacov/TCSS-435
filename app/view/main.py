import tkinter as tk

import numpy as np

from app.model.globs import glob_rows, glob_cols, MINOR_PADX, MINOR_PADY, Tile
from app.view.VisualFrame import VisualGridFrame

# param
frame_width = 800
frame_height = 500

tile_width = 25

grid_data = np.empty((glob_rows, glob_cols))
grid_positions = np.empty((glob_rows, glob_cols), dtype=object)
grid_labels = np.empty((glob_rows, glob_cols), dtype=object)

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
visual_grid = VisualGridFrame(visual_frame, glob_rows, glob_cols, tile_width=25)
visual_grid.pack()
visual_frame.pack()

# second frame, below the grid, the input
input_frame = tk.Frame(root) # child of root

row_col_input_frame = tk.Frame(input_frame) # child of input frame, this one is on top

# row input on the left
row_input_frame = tk.Frame(row_col_input_frame)
row_label = tk.Label(row_input_frame,
                     text="Row count: ",
                     )
row_input = tk.Entry(row_input_frame, width=5)

row_label.grid(row=0, column=0)
row_input.grid(row=0, column=1)

# col input on the right
col_input_frame = tk.Frame(row_col_input_frame)
col_label = tk.Label(col_input_frame,
                     text="Column count: ",
                     )
col_input = tk.Entry(col_input_frame, width=5)

col_label.grid(row=0, column=0)
col_input.grid(row=0, column=1)

# organize these frames
row_input_frame.grid(row=0, column=0, padx=MINOR_PADX, pady=MINOR_PADY)
col_input_frame.grid(row=0, column=1, padx=MINOR_PADX, pady=MINOR_PADY)

row_col_input_frame.grid_columnconfigure(0, weight=1)
row_col_input_frame.grid_columnconfigure(1, weight=1)

# this guy is the entry
row_col_input_frame.grid(row=0, column=0, sticky="ew")
input_frame.grid_columnconfigure(0, weight=1) # so the column can expand in width

# this guy is the submit
row_col_button = tk.Button(row_col_input_frame, text="Submit",
                           padx=MINOR_PADX, pady=MINOR_PADY,)
                           #command=labmda: updateGrid(int(row_input.get()), int(col_input.get())))
row_col_button.grid(row=0, column=3)

# randomize button
randomize_button = tk.Button(input_frame, text="Randomize Map")
randomize_button.grid(row=1, column=0)

input_frame.configure(width=500, height=100, padx=MINOR_PADX, pady=MINOR_PADY)
input_frame.pack()
input_frame.pack_propagate(False)

root.mainloop()