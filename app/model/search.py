"""This file describes the different types of algorithms used in searching the navmap.

Each algorithm will reset the navmap to search it again.

"""
import heapq
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

        self.frontier = [] # collection of positions been in
        self.visited = set() # a set of visited nodes
        self.goal_node = None # the ending node, the goal, with a traceable parent

    def search(self):
        _clear_map(self.navmap)
        start = time.perf_counter_ns() # start of search

        root = Node(self.navmap.entrance, None)
        self.frontier.append(root)
        if not self._goal_test(root): # goal test on the first node
            # first one was not the goal
            while len(self.frontier) > 0 and not self.goal: # while not empty and no goal
                self.stats.nodes_expanded += self._expand()

        self.stats.time_taken = time.perf_counter_ns() - start # end of search
        self.stats.goal = self.goal
        for n in self.visited:
            self.stats.visited.add(n.data)

        # trace parents to find the path
        if self.goal:
            node = self.goal_node
            while node.parent is not None:
                self.stats.path_length += 1
                self.stats.path.insert(0, node.data)
                node = node.parent

        return self.stats

    @abstractmethod
    def _expand(self):
        """The method in which the search expands nodes"""
        raise NotImplementedError

    def _goal_test(self, node):
        if self.navmap[node.data] == Tile.EXIT:
            self.goal = True
            self.goal_node = node

        return self.goal or None # return true, false, or none

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
        for cr, cc in [  # child row, child column
            (nr - 1, nc), # first, up
            (nr + 1, nc), # then, down
            (nr, nc - 1), # then, left
            (nr, nc + 1), # finally, right
            ]: # list to enforce order
            # simple bounds check
            if 0 <= cr < max_r and 0 <= cc < max_c:
                child = Node((cr, cc), node)
                node.children.append(child)
        return node.children

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

    def _expand(self):
        node = self.frontier.pop(0)

        self.visited.add(node)

        match self.navmap[node.data]:
            case Tile.OBSTACLE: return 0 # wall, can't do anything here
            case Tile.HAZARD: return 0 # hazard, can't go here

        if self._goal_test(node): # goal found
            return 0

        for child in self.children_of(node):
            if child not in self.visited and child not in self.frontier:
                # FIFO
                self.frontier.insert(-1, child)

        return 1

class DepthFirstSearch(Search):
    """Performs a deapth-first search on a navmap."""

    # duplicate of BFS, with the change of LIFO instead of FIFO
    def _expand(self):
        node = self.frontier.pop(0)

        self.visited.add(node)

        match self.navmap[node.data]:
            case Tile.OBSTACLE:
                return 0  # wall, can't do anything here
            case Tile.HAZARD:
                return 0  # hazard, can't go here

        if self._goal_test(node):  # goal found
            return 0

        children_nodes = self.children_of(node)
        children_nodes.reverse()
        for child in children_nodes:
            if child not in self.visited and child not in self.frontier:
                # LIFO
                self.frontier.insert(0, child)

        return 1

class UniformCostSearch(Search):
    """Performs a uniform cost search on a navmap."""

    # we need the cheapest element always accessible... what about a heap?
    # https://docs.python.org/3/library/heapq.html
    def _expand(self):
        node = heapq.heappop(frontier)
        node = self.frontier_nodes.pop(0)

        self.visited.add(node.data)

        match self.navmap[node.data]:
            case Tile.OBSTACLE:
                return 0  # wall, can't do anything here
            case Tile.HAZARD:
                return 0  # hazard, can't go here

        if self._goal_test(node):  # goal found
            return 0

        children_nodes = self.children_of(node)
        children_nodes.reverse()  # otherwise the nodes are added in reverse to the FIFO queue
        for child in children_nodes:
            if child.data not in self.visited and child.data not in self.frontier:
                # FIFO
                self.frontier.insert(0, child.data)
                self.frontier_nodes.insert(0, child)

        return 1

    
    
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

    def __hash__(self):
        return hash(self.data)
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.data == other.data
        else:
            return False