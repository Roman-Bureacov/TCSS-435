"""This file describes the different types of algorithms used in searching the navmap.

Each algorithm will reset the navmap to search it again.

"""
import time
from navmap import Tile
from abc import ABC, abstractmethod

class Search(ABC):
    """Abstract class for performing searches

    Attributes:
        time: the time taken to search
        nodes_expanded: the number of nodes expanded
        path_length: the length of the path found
        goal: the goal (true if found, false if failure, None if not yet found)
    """

    def __init__(self, navmap):
        """Initializes the search object.

        Args:
            navmap: the navmap to navigate
        """
        self.stats = Stats()
        self.goal = None
        self.navmap = navmap


    @abstractmethod
    def search(self):
        """Initiates the search algorithm."""
        raise NotImplementedError


    def children_of(self, node):
        """Returns the children of the given node.

        Args:
            node: the node to get the children of

        returns:
            a set of children nodes
        """
        max_r, max_c = self.navmap.shape
        nr, nc = node  # node row, node column
        r = set()
        for cr, cc in {  # child row, child column
            (nr + 1, nc),
            (nr - 1, nc),
            (nr, nc + 1),
            (nr, nc - 1),
            }:
            # simple bounds check
            if 0 < cr < max_r and 0 < cc < max_c:
                r.add((cr, cc))
        return r

class Stats:
    """Stores statistics to be returned by algorithms."""
    time: int
    nodes_expanded: int
    path_length: int
    goal: bool
    visited: set

class BreadthFirstSearch(Search):
    """Performs a breadth-first search on a navmap."""

    def __init__(self, navmap):
        Search.__init__(self, navmap)
        self.frontier = [] # a FIFO queue
        self.visited = set() # a set of visited nodes

    def search(self):
        start = time.perf_counter_ns()

        self.frontier.append(self.navmap.entrance)
        if not self._goal_test(self.frontier[0]): # goal test on the first node
            # first one was not the goal
            while len(self.frontier) != 0: # while not empty
                if self.goal: break
                self.stats.nodes_expanded = self.stats.nodes_expanded + self._expand()

        self.stats.time_taken = time.perf_counter_ns() - start
        self.stats.goal = self.goal
        self.stats.visited = self.visited
        return self.stats

    def _expand(self):
        node = self.frontier.pop(0)
        self.visited.add(node)

        match self.navmap[node]:
            case Tile.WALL: return 0 # wall, can't do anything here
            case Tile.EXIT: return 0 # hazard, can't go here

        if self._goal_test(node): return 0 # goal found

        for child in self.children_of(node):
            if child not in self.visited or child not in self.frontier:
                self.frontier.insert(0, child)

        return 1

    def _goal_test(self, node):
        if self.navmap[node] == Tile.EXIT: self.goal = True

        return self.goal or None # return true, false, or none

def depth_first_search(navmap):
    """Performs a depth-first search on the navmap.

    Args:
        navmap: the navmap to navigate

    Returns:
        a Stats object
    """
    _clear_map(navmap)

    # TODO: DFS???

def uniform_cost_search(navmap):
    """Performs a uniform cost search on the navmap.

    Args:
        navmap: the navmap to navigate

    Returns:
        a Stats object
    """
    _clear_map(navmap)

    # TODO: UCS???

    
    
def _clear_map(navmap):
    """Clears the navmap of any other data.
    
    Clears the navmap of any potential data that isn't:
      * obstacles
      * hazards
      * exit
      * entrance
    
    Args:
        navmap: the navmap to clear
    """
    
    for r in navmap:
        for c in navmap[r]:
            if navmap[r, c] not in [Tile.OBSTACLE, Tile.HAZARD, Tile.EXIT, Tile.ENTRANCE]:
                navmap[r, c] = Tile.EMPTY

class Stats:
    """Stores statistics to be returned by algorithms.

    The Stats object is a fat struct of many attributes, some of
    which may or may not be used.

    Attributes:
        path_length: the length of the path
        number_nodes_expanded: the number of nodes expanded during the search
        time: the time taken to perform
    """
    def __init__(self):
        self.path_length = None
        self.number_nodes_expanded = None
        self.time = None
        pass

