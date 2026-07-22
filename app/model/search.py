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

        self._perform()

        self.stats.time = time.perf_counter_ns() - start # end of search
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

    def _perform(self):
        root = Node(self.navmap.entrance, None)
        if not self._goal_test(root):  # goal test on the first node
            # first one was not the goal
            self.frontier.append(root)
            while len(self.frontier) > 0 and not self.goal:  # while not empty and no goal
                self.stats.nodes_expanded += self._expand()

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

    def translate_time(self, ns):
        """ Translates a time span into a more readable format

        Args:
            ns: the time span in nanoseconds

        Returns
            a string with the new time and unit
        """
        r = ns
        u = "ns"
        if r > 10**3:
            r /= 10**3 # convert into microsecond
            u = "mus"
            if r > 10**3: # convert into millisecond
                r /= 10**3
                u = "ms"
                if r > 10**3: # convert into seconds
                    r /= 10**3
                    u = "s"
                    if r > 60: # convert into minutes
                        r /= 60
                        u = "m"
                        if r > 60: # convert into hours
                            r /= 60
                            u = "h"

        return f"{r:.2f} {u}"

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

    def __init__(self, navmap):
        Search.__init__(self, navmap)
        self.count = 0

    def _perform(self):
        root = Node(self.navmap.entrance, None)

        if not self._goal_test(root):  # goal test on the first node
            # first one was not the goal
            self.frontier_nodes = dict() # mapping of node -> cost
            # all nodes will store:
            #   (total cost, self cost, recency, node)
            # the self cost is to be used as a tie-breaker
            # recency is a last-resort tie-breaker, most recent goes
            heapnode = (0, 0, self.counter(), root)
            heapq.heappush(self.frontier, heapnode)
            self.frontier_nodes[root] = heapnode
            while len(self.frontier) > 0 and not self.goal:  # while not empty and no goal
                self.stats.nodes_expanded += self._expand()

    # we need the cheapest element always accessible... what about a min heap?
    # https://docs.python.org/3/library/heapq.html
    def _expand(self):
        total_cost, self_cost, recency, node = heapq.heappop(self.frontier)
        self.frontier_nodes.pop(node)

        self.visited.add(node)

        match self.navmap[node.data]:
            case Tile.OBSTACLE:
                return 0  # wall, can't do anything here
            case Tile.HAZARD:
                return 0  # hazard, can't go here

        if self._goal_test(node):  # goal found
            return 0

        for child in self.children_of(node):
            if child not in self.visited and child not in self.frontier_nodes:
                # min heap
                child_cost = self._cost_of(child, node)
                total = total_cost + child_cost
                heapnode = (total, child_cost, self.counter(), child)
                heapq.heappush(self.frontier, heapnode)
                self.frontier_nodes[child] = heapnode
            elif child in self.frontier_nodes:
                # get child from heap
                current_cost, child_cost, count, _ = self.frontier_nodes[child]
                new_child_cost = self._cost_of(child, node)
                new_cost = total_cost + child_cost
                if new_cost < current_cost: # replace that node if it's more expensive
                    i = self.frontier.index((current_cost, child_cost, count, child))
                    self.frontier[i] = (new_cost, child_cost, self.counter(), child)
                    heapq.heapify(self.frontier) # re-heap
                    self.frontier_nodes[child] = new_cost

        return 1

    # noinspection PyMethodMayBeStatic
    def _cost_of(self, child, parent):
        cr, cc = child.data
        pr, pc = parent.data

        if cr < pr:
            return 1  # up is 1
        elif cr > pr:
            return 2  # down is 2
        elif cc < pc:
            return 3  # left is 3
        else:
            return 4  # right is 4

    def counter(self):
        self.count += 1
        return self.count

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