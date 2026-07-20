"""This file describes the different types of algorithms used in searching the navmap.

Each algorithm will reset the navmap to search it again.

"""
import time
from dataclasses import dataclass, field

from app.model.navmap import Tile
from abc import ABC, abstractmethod

class Search(ABC):
    """Abstract class for performing searches

    Attributes:
        stats: the stats object that holds statistics in regards to this search
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
        """Finds the children of the given node.

        Will find the children nodes and automatically assign
        parenting and children rules to both the node and its children

        Args:
            node: the node to get the children of

        returns:
            a set of children nodes
        """
        max_r, max_c = self.navmap.shape
        nr, nc = node.data  # node row, node column
        r = set()
        for cr, cc in [  # child row, child column
            (nr + 1, nc), # first, up
            (nr - 1, nc), # then, down
            (nr, nc - 1), # then, left
            (nr, nc + 1), # finally, right
            ]: # list to enforce order
            # simple bounds check
            if 0 <= cr < max_r and 0 <= cc < max_c:
                child = Node((cr, cc), node)
                node.children.append(child)
                r.add(child)
        return r

@dataclass
class Stats:
    """Stores statistics to be returned by algorithms."""
    time: int = 0
    nodes_expanded: int = 0
    path_length: int = 0
    path: list = field(default_factory=list)
    goal: bool = False
    visited: set = field(default_factory=set)

class BreadthFirstSearch(Search):
    """Performs a breadth-first tree search on a navmap."""

    def __init__(self, navmap):
        Search.__init__(self, navmap)
        self.frontier = [] # a FIFO queue, collection of positions been in
        self.frontier_nodes = [] # collection of the respective nodes
        self.visited = set() # a set of visited nodes
        self.goal_node = None # the ending node, the goal, with a traceable parent

    def search(self):
        _clear_map(self.navmap)
        start = time.perf_counter_ns() # start of search

        self.frontier.append(self.navmap.entrance)
        self.frontier_nodes.append(Node(self.navmap.entrance, None))
        if not self._goal_test(self.frontier_nodes[0]): # goal test on the first node
            # first one was not the goal
            while len(self.frontier) > 0 and not self.goal: # while not empty and no goal
                self.stats.nodes_expanded = self.stats.nodes_expanded + self._expand()

        self.stats.time_taken = time.perf_counter_ns() - start # end of search
        self.stats.goal = self.goal
        self.stats.visited = self.visited

        # trace parents to find the path
        node = self.goal_node
        if self.goal:
            while node.parent is not None:
                self.stats.path_length = self.stats.path_length + 1
                self.stats.path.insert(0, node.data)
                node = node.parent

        return self.stats

    def _expand(self):
        self.frontier.pop(0)
        node = self.frontier_nodes.pop(0)

        self.visited.add(node.data)

        match self.navmap[node.data]:
            case Tile.OBSTACLE: return 0 # wall, can't do anything here
            case Tile.HAZARD: return 0 # hazard, can't go here

        if self._goal_test(node): # goal found
            self.goal_node = node
            return 0

        for child in self.children_of(node):
            if child.data not in self.visited and child.data not in self.frontier:
                self.frontier.insert(-1, child.data)
                self.frontier_nodes.insert(-1, child)


        return 1

    def _goal_test(self, node):
        if self.navmap[node.data] == Tile.EXIT:
            self.goal = True
            self.goal_node = node

        return self.goal or None # return true, false, or none

class DepthFirstSearch(Search):
    """Performs a deapth-first search on a navmap."""

    # duplicate of BFS, with the change of LIFO instead of FIFO

    def __init__(self, navmap):
        Search.__init__(self, navmap)
        self.frontier = [] # a LIFO queue
        self.visited = set() # a set of visited nodes

    def search(self):
        _clear_map(self.navmap)
        start = time.perf_counter_ns()

        self.frontier.append(self.navmap.entrance)
        if not self._goal_test(self.frontier[0]): # goal test on the first node
            # first one was not the goal
            while len(self.frontier) > 0 and not self.goal: # while not empty and no goal
                self.stats.nodes_expanded = self.stats.nodes_expanded + self._expand()

        self.stats.time_taken = time.perf_counter_ns() - start
        self.stats.goal = self.goal
        self.stats.visited = self.visited
        return self.stats

    def _expand(self):
        node = self.frontier.pop(0)
        self.visited.add(node)

        match self.navmap[node]:
            case Tile.OBSTACLE: return 0 # wall, can't do anything here
            case Tile.HAZARD: return 0 # hazard, can't go here

        if self._goal_test(node): return 0 # goal found

        for child in self.children_of(node):
            if child not in self.visited and child not in self.frontier:
                self.frontier.insert(0, child)

        return 1

    def _goal_test(self, node):
        if self.navmap[node] == Tile.EXIT: self.goal = True

        return self.goal or None # return true, false, or none


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

    rows, columns = navmap.shape
    for r in range(rows):
        for c in range(columns):
            if navmap[r, c] not in {Tile.OBSTACLE, Tile.HAZARD, Tile.EXIT, Tile.ENTRANCE}:
                navmap[r, c] = Tile.EMPTY

class Node:
    """A basic node with a parent and n children."""
    def __init__(self, data, parent):
        self.parent = parent
        self.children = []
        self.data = data