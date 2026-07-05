"""collection of modification for a navigation map

Here contained is the collection of functions that can be used to manipulate a navigation map

"""
from random import randint
from globs import Tile

"""places random tiles around the map

places random tiles around the map, with specified weights. 
Places one entrance and one exit.

Args:
    navmap: the navmap to modify
    obstable_weight: the weight in which to place obstables
    empty_weight: the weight in which to place empty tiles
"""
def randomize(navmap,
              obstacle_weight= 100,
              empty_weight= 100):
    navmap[
        randint(0, navmap.shape[0]),
        randint(0, navmap.shape[1])
    ] = Tile.HAZARD

    navmap[
        randint(0, navmap.shape[0]),
        randint(0, navmap.shape[1])
    ] = Tile.EXIT

    # place the empty and obstacle tiles around the map
    for r in range(navmap.shape[0]):
        for c in range(navmap.shape[1]):
            looking_at = navmap[r, c]
            if looking_at == Tile.HAZARD or looking_at == Tile.EXIT: continue
            else:
                r = randint(0, obstacle_weight + empty_weight)
                if r < obstacle_weight: navmap[r, c] = Tile.obstacle_weight
                else: navmap[r, c] = Tile.EMPTY
