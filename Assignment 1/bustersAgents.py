from __future__ import print_function
# bustersAgents.py
# ----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import csv
from builtins import range
from wekaI import Weka
from builtins import object
import util
from game import Agent
from game import Directions
from keyboardAgents import KeyboardAgent
import inference
import busters

class NullGraphics(object):
    "Placeholder for graphics"
    def initialize(self, state, isBlue = False):
        pass
    def update(self, state):
        pass
    def pause(self):
        pass
    def draw(self, state):
        pass
    def updateDistributions(self, dist):
        pass
    def finish(self):
        pass

class KeyboardInference(inference.InferenceModule):
    """
    Basic inference module for use with the keyboard.
    """
    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        allPossible = util.Counter()
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if emissionModel[trueDistance] > 0:
                allPossible[p] = 1.0
        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        pass

    def getBeliefDistribution(self):
        return self.beliefs


class BustersAgent(object):
    "An agent that tracks and displays its beliefs about ghost positions."

    def __init__( self, index = 0, inference = "ExactInference", ghostAgents = None, observeEnable = True, elapseTimeEnable = True):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable
        self.prev_line= ''
        self.prev_dirPac= '0'
        self.weka = Weka()
        self.weka.start_jvm()

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        #for index, inf in enumerate(self.inferenceModules):
        #    if not self.firstMove and self.elapseTimeEnable:
        #        inf.elapseTime(gameState)
        #    self.firstMove = False
        #    if self.observeEnable:
        #        inf.observeState(gameState)
        #    self.ghostBeliefs[index] = inf.getBeliefDistribution()
        #self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        return Directions.STOP

    def printLineData(self, gameState):

        
        
        line=str(gameState.getPacmanPosition()[0])+ ',' + str(gameState.getPacmanPosition()[1]) + ','
        
        if 'North' in gameState.getLegalPacmanActions():
            line+='North'+','
        else:
            line+='None'+','

        if 'South' in gameState.getLegalPacmanActions():
            line+='South'+','
        else:
            line+='None'+','
        
        if 'East' in gameState.getLegalPacmanActions():
            line+='East'+','
        else:
            line+='None'+','

        if 'West' in gameState.getLegalPacmanActions():
            line+='West'+','
        else:
            line+='None'+','

        if 'Stop' in gameState.getLegalPacmanActions():
            line+='Stop'+','
        else:
            line+='None'+','
               
        line+= str(gameState.getLivingGhosts().count(True)) +','+str(gameState.getGhostPositions()[0][0]) +','+str(gameState.getGhostPositions()[0][1]) +','+str(gameState.getGhostPositions()[1][0]) +','+str(gameState.getGhostPositions()[1][1]) +','+ str(gameState.getGhostPositions()[2][0]) +','+str(gameState.getGhostPositions()[2][1]) +','+str(gameState.getGhostPositions()[3][0]) +','+str(gameState.getGhostPositions()[3][1]) +','
        
        if not type(gameState.data.ghostDistances[0])==int:
            line += '0'+','
        else: 
            line += str(gameState.data.ghostDistances[0]) + ','
        
        if not type(gameState.data.ghostDistances[1])==int:
            line += '0'+','
        else: 
            line += str(gameState.data.ghostDistances[1]) + ','  
            
        if not type(gameState.data.ghostDistances[2])==int:
            line += '0'+','
        else: 
            line += str(gameState.data.ghostDistances[2]) + ','
            
        if not type(gameState.data.ghostDistances[3])==int:
            line += '0'+','
        else: 
            line += str(gameState.data.ghostDistances[3]) + ','
            
        if not type(gameState.getNumFood())==int:
            line += '0'+','
        else: 
            line += str(gameState.getNumFood()) + ','
            
        if not type(gameState.getDistanceNearestFood())==int:
            line += '0'+','
        else: 
            line += str(gameState.getDistanceNearestFood()) + ','
                
        line += str(gameState.getScore()) 

        directionPac= str(gameState.data.agentStates[0].getDirection())

        if self.countActions==0:
            print_now= ''
        else:
            print_now=self.prev_line + ',' + str(gameState.getScore()) + ',' + self.prev_dirPac

        self.prev_line= line
        self.prev_dirPac= directionPac

        return print_now
        


class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index = 0, inference = "KeyboardInference", ghostAgents = None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)
        self.countActions = 0

    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def chooseAction(self, gameState):
        self.countActions = self.countActions + 1
        return KeyboardAgent.getAction(self, gameState)

from distanceCalculator import Distancer
from game import Actions
from game import Directions
import random, sys

'''Random PacMan Agent'''
class RandomPAgent(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        ##print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table
        
    def chooseAction(self, gameState):
        self.countActions = self.countActions + 1
        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        move_random = random.randint(0, 3)
        if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
        if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
        if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
        if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move
        
class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(self, gameState):
        "Pre-computes the distance between every two points."
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0

    def chooseAction(self, gameState):
        """
        First computes the most likely position of each ghost that has
        not yet been captured, then chooses an action that brings
        Pacman closer to the closest ghost (according to mazeDistance!).

        To find the mazeDistance between any two positions, use:
          self.distancer.getDistance(pos1, pos2)

        To find the successor position of a position after an action:
          successorPosition = Actions.getSuccessor(position, action)

        livingGhostPositionDistributions, defined below, is a list of
        util.Counter objects equal to the position belief
        distributions for each of the ghosts that are still alive.  It
        is defined based on (these are implementation details about
        which you need not be concerned):

          1) gameState.getLivingGhosts(), a list of booleans, one for each
             agent, indicating whether or not the agent is alive.  Note
             that pacman is always agent 0, so the ghosts are agents 1,
             onwards (just as before).

          2) self.ghostBeliefs, the list of belief distributions for each
             of the ghosts (including ghosts that are not alive).  The
             indices into this list should be 1 less than indices into the
             gameState.getLivingGhosts() list.
        """
        self.countActions = self.countActions + 1
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions()]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = \
            [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
             if livingGhosts[i+1]]
        return Directions.EAST

class BasicAgentAA(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        #print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    def printInfo(self, gameState):
        print("---------------- TICK ", self.countActions, " --------------------------")
        # Map size
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print("Width: ", width, " Height: ", height)
        # Pacman position
        print("Pacman position: ", gameState.getPacmanPosition())
        # Legal actions for Pacman in current position
        print("Legal actions: ", gameState.getLegalPacmanActions())
        # Pacman direction
        print("Pacman direction: ", gameState.data.agentStates[0].getDirection())
        # Number of ghosts
        print("Number of ghosts: ", gameState.getNumAgents() - 1)
        # Alive ghosts (index 0 corresponds to Pacman and is always false)
        print("Living ghosts: ", gameState.getLivingGhosts())
        # Ghosts positions
        print("Ghosts positions: ", gameState.getGhostPositions())
        # Ghosts directions
        print("Ghosts directions: ", [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)])
        # Manhattan distance to ghosts
        print("Ghosts distances: ", gameState.data.ghostDistances)
        # Pending pac dots
        print("Pac dots: ", gameState.getNumFood())
        # Manhattan distance to the closest pac dot
        print("Distance nearest pac dots: ", gameState.getDistanceNearestFood())
        # Map walls
        print("Map:")
        print( gameState.getWalls())
        # Score
        print("Score: ", gameState.getScore())
        
    def Problem_in_Legal(self, gameState):
        self.countActions = self.countActions + 1
        self.printInfo(gameState)
        move = Directions.STOP
        legal = gameState.getLegalPacmanActions() ##Legal position from the pacman

        distances=gameState.data.ghostDistances
        index=distances.index(min(x for x in distances if x is not None))

        if ( gameState.getPacmanPosition()[0] > gameState.getGhostPositions()[index][0] ) and ( gameState.getPacmanPosition()[1] > gameState.getGhostPositions()[index][1] ) and (Directions.WEST in legal or Directions.SOUTH in legal):             
                    move_random = random.randint(0, 1)
                    if   ( move_random == 0 ) and ( Directions.WEST in legal ):
                        move = Directions.WEST
                        
                    else :
                        if Directions.SOUTH in legal:
                            move = Directions.SOUTH
                         
                    if   ( move_random == 1 ) and ( Directions.SOUTH in legal ):
                        move = Directions.SOUTH
                        
                    else:
                        if Directions.WEST in legal:
                            move = Directions.WEST

        if ( gameState.getPacmanPosition()[0] < gameState.getGhostPositions()[index][0] ) and ( gameState.getPacmanPosition()[1] < gameState.getGhostPositions()[index][1] ) and (Directions.EAST in legal or Directions.NORTH in legal):             
                    move_random = random.randint(0, 1)
                    if   ( move_random == 0 ) and ( Directions.EAST in legal ):
                        move = Directions.EAST
                        
                    else :
                        if Directions.NORTH in legal:
                            move = Directions.NORTH
                         
                    if   ( move_random == 1 ) and ( Directions.NORTH in legal ):
                        move = Directions.NORTH
                        
                    else:
                        if Directions.EAST in legal:
                            move = Directions.EAST

        if ( gameState.getPacmanPosition()[0] > gameState.getGhostPositions()[index][0] ) and ( gameState.getPacmanPosition()[1] < gameState.getGhostPositions()[index][1] ) and (Directions.WEST in legal or Directions.NORTH in legal):             
                    move_random = random.randint(0, 1)
                    if   ( move_random == 0 ) and ( Directions.WEST in legal ):
                        move = Directions.WEST
                        
                    else :
                        if Directions.NORTH in legal:
                            move = Directions.NORTH
                         
                    if   ( move_random == 1 ) and ( Directions.NORTH in legal ):
                        move = Directions.NORTH
                        
                    else:
                        if Directions.WEST in legal :
                            move = Directions.WEST

        if ( gameState.getPacmanPosition()[0] < gameState.getGhostPositions()[index][0] ) and ( gameState.getPacmanPosition()[1] > gameState.getGhostPositions()[index][1] ) and (Directions.EAST in legal or Directions.SOUTH in legal):             
                    move_random = random.randint(0, 1)
                    if   ( move_random == 0 ) and ( Directions.EAST in legal ):
                        move = Directions.EAST
                        
                    else:
                        if Directions.SOUTH in legal :
                            move = Directions.SOUTH
                         
                    if   ( move_random == 1 ) and ( Directions.SOUTH in legal ):
                        move = Directions.SOUTH
                        
                    else:
                        if Directions.EAST in legal:
                            move = Directions.EAST

        if ( gameState.getPacmanPosition()[0] == gameState.getGhostPositions()[index][0] ) and ( gameState.getPacmanPosition()[1] > gameState.getGhostPositions()[index][1] ):             

                    if Directions.SOUTH in legal:
                        move = Directions.SOUTH
                        
                    else:
                        move_random = random.randint(0, 1)
                        if   ( move_random == 0 ) and ( Directions.EAST in legal ): move = Directions.EAST
                        if   ( move_random == 1 ) and ( Directions.WEST in legal ): move = Directions.WEST

        if ( gameState.getPacmanPosition()[0] == gameState.getGhostPositions()[index][0] ) and ( gameState.getPacmanPosition()[1] < gameState.getGhostPositions()[index][1] ):             

                    if Directions.NORTH in legal:
                        move = Directions.NORTH
                        
                    else:
                        move_random = random.randint(0, 1)
                        if   ( move_random == 0 ) and ( Directions.EAST in legal ): move = Directions.EAST
                        if   ( move_random == 1 ) and ( Directions.WEST in legal ): move = Directions.WEST

        if ( gameState.getPacmanPosition()[0] < gameState.getGhostPositions()[index][0] ) and ( gameState.getPacmanPosition()[1] == gameState.getGhostPositions()[index][1] ):             

                    if Directions.EAST in legal:
                        move = Directions.EAST
                        
                    else:
                        move_random = random.randint(0, 1)
                        if   ( move_random == 0 ) and ( Directions.SOUTH in legal ): move = Directions.SOUTH
                        if   ( move_random == 1 ) and ( Directions.NORTH in legal ): move = Directions.NORTH

        if ( gameState.getPacmanPosition()[0] > gameState.getGhostPositions()[index][0] ) and ( gameState.getPacmanPosition()[1] == gameState.getGhostPositions()[index][1] ):             

                    if Directions.WEST in legal:
                        move = Directions.WEST
                        
                    else:
                        move_random = random.randint(0, 1)
                        if   ( move_random == 0 ) and ( Directions.SOUTH in legal ): move = Directions.SOUTH
                        if   ( move_random == 1 ) and ( Directions.NORTH in legal ): move = Directions.NORTH
        
        return move   

    def chooseAction(self, gameState):
        weka = Weka()
        weka.start_jvm()
        self.countActions = self.countActions + 1
        self.printInfo(gameState)
        move = Directions.STOP
        legal = gameState.getLegalPacmanActions() ##Legal position from the pacman
        
        x=[]
        
        PacPosX =gameState.getPacmanPosition()[0]
        PacPosY=gameState.getPacmanPosition()[1]

        x.append(PacPosX)
        x.append(PacPosY)

        if "North" in legal: 
            x.append("North")
        elif "North" not in legal: 
            x.append("None")
        if "South" in legal: 
            x.append("South")
        elif "South" not in legal: 
            x.append("None")
        if "East" in legal: 
            x.append("East")
        elif "East" not in legal: 
            x.append("None")
        if "West" in legal: 
            x.append("West")
        elif "West" not in legal: 
            x.append("None")      
            

        x.append(gameState.getGhostPositions()[0][0])
        x.append(gameState.getGhostPositions()[0][1])
        x.append(gameState.getGhostPositions()[1][0])
        x.append(gameState.getGhostPositions()[1][1])
        x.append(gameState.getGhostPositions()[2][0])
        x.append(gameState.getGhostPositions()[2][1])
        x.append(gameState.getGhostPositions()[3][0])
        x.append(gameState.getGhostPositions()[3][1])
        x.append(gameState.getScore())
        move = weka.predict("./RandomForest.model", x, './NOtraining_keyboard(Phase_2).arff')
        
        if move == 'South' and move in legal:
            return Directions.SOUTH
        else:
            return BasicAgentAA.Problem_in_Legal(self,gameState)
        if move == 'North' and move in legal:
            return Directions.NORTH
        else:
            return BasicAgentAA.Problem_in_Legal(self,gameState)
        if move == 'East' and move in legal:
            return Directions.EAST
        else:
            return BasicAgentAA.Problem_in_Legal(self,gameState)
        if move == 'West' and move in legal:
            return Directions.WEST
        else:
            return BasicAgentAA.Problem_in_Legal(self,gameState)
        if move == 'Stop' and move in legal:
            return Directions.STOP
        else:
            return BasicAgentAA.Problem_in_Legal(self,gameState)
        
    