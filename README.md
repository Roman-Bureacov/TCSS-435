# TCSS 435 A

Roman Bureacov

## A00: HowTo

The app is very human. 

Requirements:

* numpy 2.6
* Python 3.14

start the program by invoking app/view/main.py.

Resize the grid by inputting the new shape (rows, columns)
and hitting "Resize". *note: this does not preserve the map*.

Make the tile by inputting the weights and hitting "Randomize Map".
The higher the weight, the more likely it is to appear on the map.

## A02: Description

### HowTo

The design is very human.

1. Set up the grid dimensions (if necessary), then hit `Resize`, this will
    resize the grid
2. Set the tile weights (empty at 120 and obstacle at 50 is pretty respectable)
    and hit `Randomize Map`, this will place tiles around the map
3. hit any of the search buttons to perform their respective search

### Implementation

The implementation was inspired directly from the book, but required some changes
as the book had a description that was a little too abstract.

At first the implementation was that of depth-first search subclassing 
breadth-first search, but then I realized I can generalize the code even
further and have it all subclass a generic `Search` class.

The implementation is that each search algorithm has its own way of performing 
a search, and furthermore each one is different primarily in the method
of node expansion. A lot of the subclassing is done on the `self._expand`
function.

Uniform-cost search was the most intriguing to implement. It required a way
to get the minimum at a reasonable cost. Recalling my algorithms class, I
implemented that by use of a min-heap. The only inefficiency in the 
implementation, however, is that if a frontier node is to be replaced, then 
it must replace it and re-heapify the heap to maintain the min-heap property.

Part of the problem with replacing children nodes was also finding them. The
way this was done here was by means of a dictionary mapping a node object
to its respective data in the heap, that way the node can be found easily.

Another complication was that even though having the rule of expanding the 
nodes in a predefined order to break ties... what if two nodes cost the same
and are BOTH expanding to the same direction? Thus a simple counter was 
implemented to expand the that was earlier to the frontier.

The statistics I decided to throw into a "fat struct" that can be accessed later,
to minimize how many things I need to return and make things simpler.

This implementation, however, was funky in that I needed to not only find
if there was a path, but also the path length, which implied asking what
the path itself actually was; the way this was implemented was by means of
building a tree (inspired by the fact that the book goes through the algorithms)
from the perspective of tree search. Each expanded node would be the parent to
the expanded children, and so once you know what the final node it, you can
just follow the chain of parents back up to the root, or the entrance.

Finally, it should be mentioned that the rules of depth-first search are a little
restrictive: instead of, say, going 

down -> right -> right -> up

what is observed instead is

down -> right -> right -> right -> up

this is because of the frontier and how the book implements the search 
strategies, in that no children in the frontier are ever considered for
expansion for DFS.

### Tests

Some trial runs were performed on a grid with the following parameters:
* shape of 10 rows by 10 columns
* empty tile weight of 100
* obstacle tile weight of 50

|                    |  Trial 1   |  Trial 2   |  Trail 3   |   Trail 4   |  Trial 5   |
|:------------------:|:----------:|:----------:|:----------:|:-----------:|:----------:|
|  BFS Path Length   |     8      |     4      |     11     |      5      |     17     |
| BFS Nodes Expanded |     27     |     55     |     46     |     30      |     41     |
|      BFS Time      | 288.40 mus | 746.30 mus | 336.50 mus | 300.00  mus | 288.00 mus |
|  DFS Path Length   |     8      |     4      |     13     |     13      |     17     |
| DFS Nodes Expanded |     18     |     4      |     13     |     22      |     52     |
|      DFS Time      | 128.70 mus | 58.80 mus  |   123.40   | 259.20 mus  | 349.60 mus |
|  UCS Path Length   |     8      |     4      |     11     |      5      |     17     |
| UCS Nodes Expanded |     24     |     6      |     46     |     38      |     50     |
|      UCS Time      | 223.00 mus |   107.30   | 426.20 mus |   1.34 ms   | 409.10 mus |


What can be observed here is that usually BFS will expand far more nodes, which
is to be expected as it expands its frontier with each search iteration.

UCS also expands a lot of nodes, but actually seems to sit 
somewhere inbetween DFS and BFS. 

DFS can be really fast, expanding only very 
few nodes compared to its competitor search strategies, however that is all
based on luck and if it can actually reach the goal state. The trail 5
shows this, where it got unlucky and expanded more nodes than the other search
strategies.

### AI Disclosure

AI was only used as a tool in implementation. All code was human-written.

ChatGPT was consulted for debugging and Python implementation tips.