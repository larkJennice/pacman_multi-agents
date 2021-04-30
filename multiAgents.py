# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Actions
from game import Agent
from numpy import inf
import math

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState, index):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """


#     currPos = currentGameState.getPacmanPosition(index)
#     currFood = currentGameState.getFood()
#     currGhostStates = currentGameState.getGhostStates()
#     currScaredTimes = [ghostState.scaredTimer for ghostState in currGhostStates]
#     currCapsule = currentGameState.getCapsules()
#     score = 0 
#     minGhost = 1e7
#     sumGhost = 0
#     capsuleScore = 0
    lose = -1e7
    win = 1e7
    
    if currentGameState.isWin():
        return win
    if currentGameState.isLose():
        return lose
    currPos = currentGameState.getPacmanPosition(index)
    currGhostStates = currentGameState.getGhostStates()
    currFood = currentGameState.getFood()
    currCapsules = currentGameState.getCapsules()
    currScaredTimes = [ghostState.scaredTimer for ghostState in currGhostStates]
    currFoodList = currFood.asList()
    ghosts = []
    min_ghost = 1e7
    for ghostState in currGhostStates:
        if ghostState.scaredTimer == 0:
            little_ghost = manhattanDistance(ghostState.getPosition(),currPos)
            ghosts.append(little_ghost)
            if (little_ghost < min_ghost):
                min_ghost = little_ghost
    if (min_ghost == 1e7):
        min_ghost = -2

        
    scared_ghosts = []
    min_scared_ghost = 1e7 
    for ghostState in currGhostStates:
        if ghostState.scaredTimer > 0:
            scared_little = manhattanDistance(ghostState.getPosition(),currPos)
            scared_ghosts.append(scared_little)
            if (min_scared_ghost > scared_little):
                min_scared_ghost = scared_little
                                              
    if min_scared_ghost == 1e7:
        min_scared_ghost = 0
        
    food_dis = []
    min_food = 1e7
    for food in currFoodList:
        one_food = manhattanDistance(food, currPos)
        food_dis.append(one_food)
        if one_food < min_food:
            min_food = one_food

    #No capsule when unnecessary, more closer distance to food, go for food, no ghost near by, more close to the scared ghost
    #minus the min in order to get more closer, minus 1/min or + min to get further (+min is worse than -1/min)
    return currentGameState.getScore()[0]*10-33*len(currCapsules)-1.5*min_food-5*len(currFoodList)-2*(1/min_ghost)-2*min_scared_ghost

#     nearest_food = min(manhattanDistance(food,currPos) for food in currFood.asList())
#     for ghost in currGhostStates:
#         ghostDis = (manhattanDistance(ghost.getPosition(), currPos))
#         sumGhost += ghostDis
#         if ghostDis < minGhost:
#             minGhost = ghostDis
#         if ghost.scaredTimer > 0:
#             score += (manhattanDistance(ghost.getPosition(), currPos))*5
#         elif manhattanDistance(ghost.getPosition(), currPos)<5:
#             score -= (manhattanDistance(ghost.getPosition(), currPos))*2
        
# #     for capsule in currCapsule:
# #         if (sumGhost <=15) and 

# #     return currentGameState.getScore()[index]*10 + (1/ nearest_food) + score
#     if (minGhost)>20:
#         return currentGameState.getScore()[index]*10 + ((1/ nearest_food)**2)*minGhost*0.8 + score
#     else:
#         return currentGameState.getScore()[index]*10 + ((1/ nearest_food)**2)*minGhost + score
class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, index = 0, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = index # Pacman is always agent index 0
        self.evaluationFunction = lambda state:util.lookup(evalFn, globals())(state, self.index)
        self.depth = int(depth)



class MultiPacmanAgent(MultiAgentSearchAgent):
    """
    You implementation here
    """

    def getAction(self, gameState):
        index = self.index # pacman index
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

#         best_score, best_choice = self.getMinMax(gameState,0,0,0)
#       Inspired by psudocode from YouTube https://www.youtube.com/watch?v=u8JNW-2Ei8w and psudocode from Kaiqi Zhang
        best_score, best_choice = self.getExpMax(gameState,0,0,0)
        return best_choice
    def getExpMax(self, gameState, agent_index, depth, getExpMax_getMax_getExp):
        if (getExpMax_getMax_getExp == 0):
            if agent_index >= gameState.getNumAgents():
                depth += 1
                agent_index = 0
            if (depth==self.depth or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState),Directions.STOP
            elif (agent_index == 0):
                return self.getExpMax(gameState, agent_index, depth ,1)
            else:
                return self.getExpMax(gameState, agent_index, depth, 2)
        elif (getExpMax_getMax_getExp == 1): 
            actions = gameState.getLegalActions(agent_index) 
            best_score = float(-inf)
            best_choice = Directions.STOP          
            if not actions:
                return self.evaluationFunction(gameState),Directions.STOP             
            for action in actions:
                next_step = gameState.generateSuccessor(agent_index, action)
                score, choice = self.getExpMax(next_step,(agent_index+1), depth, 0)
                if score > best_score:
                    best_score = score
                    best_choice = action
            return best_score, best_choice
        elif (getExpMax_getMax_getExp == 2):     
            actions = gameState.getLegalActions(agent_index)
            best_score = 0
            best_choice = Directions.STOP
            if not actions:
                return self.evaluationFunction(gameState),Directions.STOP                                 
            for action in actions:
                next_step = gameState.generateSuccessor(agent_index, action)
                score, choice = self.getExpMax(next_step,(agent_index+1),depth,0)
                choice = action
                best_score += score * (1/len(actions))
            return best_score, best_choice
    
    def getMinMax(self, gameState, agent_index, depth, getMinMax_getMax_getMin):
        if getMinMax_getMax_getMin == 0:
            if agent_index >= gameState.getNumAgents():
                agent_index = 0
                depth += 1
            if (depth ==self.depth or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState),Directions.STOP
            elif (agent_index == 0):
                return self.getMinMax(gameState, agent_index, depth, 1)
            else:
                return self.getMinMax(gameState, agent_index, depth, 2)
        elif getMinMax_getMax_getMin == 1:
            actions = gameState.getLegalActions(agent_index)
            if not actions:
                return self.evaluationFunction(gameState),Directions.STOP       
            best_score = float(-inf)
            best_choice = Directions.STOP
            for action in actions:
                next_step = gameState.generateSuccessor(agent_index, action)
                score, choice= self.getMinMax(next_step, (agent_index+1), depth, 0)
                if score > best_score:
                    best_score = score
                    best_choice = action
            return best_score, best_choice
        elif getMinMax_getMax_getMin == 2:
            actions = gameState.getLegalActions(agent_index)
            if not actions:
                return self.evaluationFunction(gameState)       
            best_score = float(inf)
            best_choice = Directions.STOP
            for action in actions:
                next_step = gameState.generateSuccessor(agent_index, action)
                score, choice= self.getMinMax(next_step, (agent_index+1), depth, 0)
                if score < best_score:
                    best_score = score
                    best_choice = action
            return best_score, best_choice
        
class RandomAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions(self.index)
        return random.choice(legalMoves)




