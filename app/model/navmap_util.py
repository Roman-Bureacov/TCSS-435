"""collection of modification for a navigation map

Here contained is the collection of functions that can be used to manipulate a navigation map

"""
from random import randint
from app.model.navmap import Tile
import numpy as np

def randomize(navmap,
              obstacle_weight= 100,
              empty_weight= 100):
    """places random tiles around the map

    places random tiles around the map, with specified weights.
    Places one entrance and one exit.

    Args:
        navmap: the navmap to modify
        obstacle_weight: the weight in which to place obstacles
        empty_weight: the weight in which to place empty tiles
    """
    rows, columns = navmap.shape
    
    bag = np.array([ # bag of tiles to choose from
        (r, c)
        for r in range(rows)
        for c in range(columns)
    ])
    np.random.shuffle(bag)

    r, c = bag[0]
    navmap[r, c] = Tile.ENTRANCE
    navmap.entrance = (r, c)

    r, c = bag[1]
    navmap[r, c] = Tile.EXIT
    navmap.exit = (r, c)

    r, c = bag[2]
    navmap[r, c] = Tile.HAZARD

    # place the empty and obstacle tiles around the map
    for i in bag[3:]: # skip the first three
        r, c = i
        rand = randint(0, obstacle_weight + empty_weight)
        if rand < obstacle_weight: navmap[r, c] = Tile.OBSTACLE
        else: navmap[r, c] = Tile.EMPTY
