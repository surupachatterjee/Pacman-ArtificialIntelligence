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
import random, util,sys

from game import Agent

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

        score = successorGameState.getScore()
        #print "newPos : " + str(newPos)
        #decrement the score, when the ghost is surrounding pacman in next state
        newGhostPos =[]
        for ghost in newGhostStates:
            newGhostPos.append(ghost.getPosition())
        pacmanNextPos = [(newPos[0]+1,newPos[1]),
                         (newPos[0]-1,newPos[1]),
                         (newPos[0],newPos[1]+1),
                         (newPos[0],newPos[1]-1)]

        for ghostPos in newGhostPos:
            if ghostPos in pacmanNextPos:
                score -=1

        #increment score , if the distance of closest food from current position is greater than that from next position

        pacmanCurrPos = currentGameState.getPacmanPosition()
        currFoodList = currentGameState.getFood().asList()

        closest_fooddist_from_curr_pos = min(util.manhattanDistance(pacmanCurrPos, food) for food in currFoodList)
        closest_fooddist_from_next_pos = min(util.manhattanDistance(newPos, food) for food in currFoodList)

        if closest_fooddist_from_curr_pos  > closest_fooddist_from_next_pos:
            score +=1

        return score




def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        return max(gameState.getLegalActions(0), key=lambda action: self.value(gameState.generateSuccessor(0, action), self.depth,1))
        #util.raiseNotDefined()

    def value(self, gameState, depth, agentIndex=0):

        # If the agentIndex is more than number of agents,
        # reset agentIndex to 0 and decrement depth value
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth -=1

        # Check if the terminal state have been reached and return termial utilities
        if gameState.isWin() or gameState.isLose() or depth ==0:
            print "Evaluation value :" + str((self.evaluationFunction(gameState),))
            return (self.evaluationFunction(gameState),)

        # if agentIndex is 0, return max value(Pacman is agent in this case)
        # else return min value
        if agentIndex == 0:
            print "agent index : " + str(agentIndex)
            return self.max_value(gameState,depth,agentIndex)
        else:
            return self.min_value(gameState,depth,agentIndex)

    def max_value(self,gameState,depth,agentIndex):
        v = (-sys.maxint,)
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            nextState = gameState.generateSuccessor(agentIndex,action)
            nextValue = self.value(nextState,depth,agentIndex+1)
            v = max(v,nextValue)
        return v

    def min_value(self,gameState,depth,agentIndex):
        v = (sys.maxint,)
        actions = gameState.getLegalActions(agentIndex)
        for action  in actions:
            nextState = gameState.generateSuccessor(agentIndex,action)
            nextValue = self.value(nextState, depth, agentIndex + 1)
            v = min(v, nextValue)
        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.value(gameState,self.depth,0,-sys.maxint,sys.maxint)[1]
        #util.raiseNotDefined()

    def value(self, gameState, depth, agentIndex, alpha, beta):

        # If the agentIndex is more than number of agents,
        # reset agentIndex to 0 and decrement depth value
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth -= 1

        # Check if the terminal state have been reached and return terminal utilities
        if gameState.isWin() or gameState.isLose() or depth == 0:
            # print "Evaluation value :" + str((self.evaluationFunction(gameState),))
            return (self.evaluationFunction(gameState),)

        # if agentIndex is 0, return max value(Pacman is agent in this case)
        # else return min value
        if agentIndex == 0:
            # print "agent index : " + str(agentIndex)
            return self.max_value(gameState, depth, agentIndex, alpha, beta)
        else:
            return self.min_value(gameState, depth, agentIndex, alpha, beta)

    def max_value(self, gameState, depth, agentIndex, alpha, beta):
        v = (-sys.maxint,)
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            nextState = gameState.generateSuccessor(agentIndex, action)
            nextValue = self.value(nextState, depth, agentIndex + 1, alpha, beta)
            if nextValue[0] > v[0]:
                v = (nextValue[0], action)
            if nextValue[0] > beta:
                return (nextValue[0], action)

            alpha = max(alpha, nextValue[0])
        return v

    def min_value(self, gameState, depth, agentIndex, alpha, beta):
        v = (sys.maxint,)
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            nextState = gameState.generateSuccessor(agentIndex, action)
            nextValue = self.value(nextState, depth, agentIndex + 1, alpha, beta)
            if nextValue[0] < v[0]:
                v = (nextValue[0], action)
            if nextValue[0] < alpha:
                return (nextValue[0], action)
            beta = min(beta, nextValue[0])
        return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return max(gameState.getLegalActions(0),
                   key=lambda action: self.value(gameState.generateSuccessor(0, action), self.depth, 1))
        #util.raiseNotDefined()

    def value(self, gameState, depth, agentIndex=0):

        # If the agentIndex is more than number of agents,
        # reset agentIndex to 0 and decrement depth value
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth -=1

        # Check if the terminal state have been reached and return termial utilities
        if gameState.isWin() or gameState.isLose() or depth ==0:
            #print "Evaluation value :" + str((self.evaluationFunction(gameState),))
            return (self.evaluationFunction(gameState),)

        # if agentIndex is 0, return max value(Pacman is agent in this case)
        # else return min value
        if agentIndex == 0:
            #print "agent index : " + str(agentIndex)
            return self.max_value(gameState,depth,agentIndex)
        else:
            return self.exp_value(gameState,depth,agentIndex)


    def max_value(self,gameState,depth,agentIndex):
        v = (-sys.maxint,)
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            nextState = gameState.generateSuccessor(agentIndex,action)
            nextValue = self.value(nextState,depth,agentIndex+1)
            v = max(v,nextValue)
        return v

    def exp_value(self,gameState,depth,agentIndex):
        v = (0,)
        p = 0
        score = 0
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            nextState = gameState.generateSuccessor(agentIndex,action)
            nextValue = self.value(nextState, depth, agentIndex + 1)
            score += nextValue[0]
            v = ((score/len(actions)),)
        return v

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    #Pacman details
    currentPacmanPos = currentGameState.getPacmanPosition()
    currentFoodList = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    fullFoodList = currentFoodList + capsules
    score  = currentGameState.getScore()


    #Ghost details
    currentGhostStates = currentGameState.getGhostStates()
    ghostScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]

    # Calculating distances
    #Closest ghost distance from the pacman
    min_ghost_distance = min(util.manhattanDistance(currentPacmanPos,ghost.getPosition()) for ghost in currentGhostStates)

    #Closest food distance from pacman
    min_food_distance = min(util.manhattanDistance(currentPacmanPos,food) for food in fullFoodList)if fullFoodList else 0

    #lowest scared time for ghosts in ghostScaredTimes List
    lowest_scared_time_of_ghost = min(ghostScaredTimes)

    # Assign values to attributes that evaluate to a final score,
    # If there is food in FoodList, then it is not good for pacman, so reduce the value here
    food_attr = -len(fullFoodList)

    # Pacman should not be close to the ghost, this attribute can be calculated based on whether the ghost is scared or not
    # If the ghost is scared, the value assigned is positive, but if the ghost is not scared, it is likely to attack Pacman, so
    #reduce the value
    ghost_attr = -5/(min_ghost_distance + 1) if lowest_scared_time_of_ghost ==0 else 10/(min_ghost_distance + 1)

    #If the pacman is away from food, reduce the value
    food_attr_dist = 2/(min_food_distance +1)

    final_score = score* 2 + food_attr_dist + food_attr + ghost_attr + lowest_scared_time_of_ghost*3

    return final_score
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

