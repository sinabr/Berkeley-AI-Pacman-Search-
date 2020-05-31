# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    # state and actions 
    stack = util.Stack()
    # here we have a enqueued list to avoid loops 
    visitedNodes = []
    first = (problem.getStartState(), [])
    stack.push( first )
    visitedNodes.append( problem.getStartState() )

    while not stack.isEmpty():
        state, moves = stack.pop()
        
        successors = problem.getSuccessors(state)
        for successor in successors:
            # for every next actions (state) possible move :
            nextState = successor[0]
            moveDirection = successor[1]
            if nextState not in visitedNodes:
                updatedPath = moves + [moveDirection]
                if problem.isGoalState(nextState):
                    # Goal found 
                    # add the last direction to the list of actions
                    return updatedPath
                else:
                    # we add the children to the top of the stack so we traverse the first child first
                    stack.push( (nextState, updatedPath) )
                    visitedNodes.append( nextState )

    # no path to goal found
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # we need to traverse the first level first so we need a queue instead
    # it can also be a stack but it takes more work to implement
    queue = util.Queue()
    # here we have a enqueued list of visited nodes both in DFS and BFS
    visited = []
    # we have visited the first 
    visited.append( problem.getStartState() )
    # firstly : we are at start and no action required to get here
    queue.push( (problem.getStartState(), []) )
    

    while queue.isEmpty() == 0:
        state, moves = queue.pop()

        for next in problem.getSuccessors(state):
            nextState = next[0]
            moveDirection = next[1]
            # we don't want to get into loops or see a node more than once (is not optimal)
            if nextState not in visited:
                updatedMoves = moves + [moveDirection]
                if problem.isGoalState(nextState):
                    # the taken actions lead us to the goal
                    # goal found
                    return updatedMoves
                else:
                    # we add the children to the queue to check them after current level
                    queue.push( (nextState, updatedMoves) )
                    visited.append( nextState )

    # no path to goal found
    return[]

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    PQ = util.PriorityQueue()
    visited = []
    PQ.push( (problem.getStartState(), []), 0 )
    visited.append( problem.getStartState() )

    while PQ.isEmpty() == 0:
        state, moves = PQ.pop()

        if problem.isGoalState(state):
            return moves

        elif state not in visited:
            visited.append( state )

        for next in problem.getSuccessors(state):
            nextState = next[0]
            moveDirection = next[1]
            if nextState not in visited:
                cost = problem.getCostOfActions(moves+[moveDirection])
                # edited PQ.update to fit the new representation of states
                PQ.update((nextState, moves + [moveDirection]), cost )
    

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    # Zero works for this (This is trivial as mentioned above)
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    PQ = util.PriorityQueue()
    visitedNodes = []
    startState = problem.getStartState()
    PQ.push((startState , []) , 0 + heuristic(startState,problem))
    visitedNodes.append(startState)
    while not PQ.isEmpty():
        state , moves = PQ.pop()
        # if the current node is the goal node 
        if problem.isGoalState(state) : 
            
            return moves
        # the node is visited
        elif state not in visitedNodes:
            visitedNodes.append(state)
        
        successors = problem.getSuccessors(state)
        for successor in successors:
            nextState = successor[0]
            moveDirection = successor[1]
            if nextState not in visitedNodes:
                
                updatedMoves = moves + [moveDirection]
                cost = problem.getCostOfActions(updatedMoves)
                # pq update is edited
                PQ.update((nextState, updatedMoves), cost + heuristic(nextState , problem) )


    # no path to goal found
    return []







# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
