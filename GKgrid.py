#!/usr/bin/env python

import pygame
import library
import time

# Define some colors for the tiles
BLACK = (0, 0, 0)			# Black for the background
WHITE = (255, 255, 255)		# Empty tile
GREEN = (0, 255, 0)			# Start
RED = (255, 0, 0)			# Path
LIGHTRED = (255, 200, 200)	# Expanded neighbors
ORANGE = (255, 128, 0)		# Obstacles
BLUE = (0, 0, 255)			# Current
PURPLE = (153, 0, 153)		# Nodes
DARKRED = (152, 0, 0)		# Goal

# 0: Empty | 1: Start | 2: Goal | 3: Obstacle | 4: Explored Nbr | 5: Current | 6: Nodes | 7: Path

class TheGrid:	#This class hols the main skeleton of the program, it will create the pygame grid and call all the necessary functions
	def __init__(self, nWidth, nHeight): 	# define the dimensions of your grid
		self.outputParents = None			#this variable is used for debugging
		self.outputNodesPath = None

		self.nWidth = nWidth	
		self.nHeight = nHeight

		self.width = 600 / nWidth	# Calculate the dimension ratio to make possible that NxN tiles can be displayted in a
		self.height = 600 / nHeight # 600x600 px screen
		self.margin = 1 			# Set the margins size
		self.grid = []				# 2D-List that hold the grids

		for row in range(nWidth):	# Loops to initializa the tiles list
			# Add an empty array that will hold each cell
			# in this row
			self.grid.append([])
			for column in range(nHeight):
				self.grid[row].append(0) # Append a cell

		pygame.init()				# init pygame library variables

		self.size = [600 + nWidth,600 + nHeight] # screen size for the drawing funtion
		# Set title of screen
		pygame.display.set_caption("A* Grid")	# Screen name

		self.screen = None
		# Used to manage how fast the screen updates
		self.clock = None

		self.clickCount = 3 	# 1 = set START | 2 = set GOAL | 3 = set OBSTACLES | 6 = Nodes
		self.startPos = None	
		self.goalPos = None


		self.theGraph = library.Graph(self.nHeight, self.nWidth)	# Initialize the graph library that handle euclidean cost graphs
		print '\nCreating Cost Graph...'
		self.theGraph.CreateGraph()									# Initialize the enclidean cost graph 
		print '\nCost Graph created!'

		self.inputCircleRadius = 1
		self.obstaclesCirclesList = []								# a list for all circular obstacles
		self.nodesList = []											# a list for the Nodes to be used

	
	def RestartTiles(self):
		self.grid = []

		for row in range(self.nWidth):	# Loops to initializa the tiles list
			# Add an empty array that will hold each cell
			# in this row
			self.grid.append([])
			for column in range(self.nHeight):
				self.grid[row].append(0) # Append a cell

	def ClearTmpTiles(self, clearCells):
		for row in range(self.nHeight):
			for column in range(self.nWidth):
				if self.grid[row][column] in clearCells:
					self.grid[row][column] = 0

	def WriteOnGrid(self, list, value):				# Function that receive a list of [i,j] positions and write a value on it
		for pos in list:
			self.grid[pos[0]][pos[1]] = value

	def WritePath(self, parents, start, goal):		# Function that receive a dict of nodes and its parents and draw sets the values in the grid for final path
		print '\n\nPARENTS = ',parents
		pathNode = goal
		path = []

		while pathNode != start:		# While not in the START position keep looking for the parent 
			pathNode = parents[str(pathNode)]	# Build the path list in a reverse way
			path.append(pathNode)
		self.WriteOnGrid(path, 7)
		self.WriteOnGrid(self.nodesList, 6)
		self.WriteOnGrid([self.startPos], 1)
		self.WriteOnGrid([self.goalPos], 2)
		path.reverse()							# Unreverse the list in order to print it in the right order
		self.outputParents = parents
		print '\n\n---------------------- PATH TO GOAL -------------------------------------------------'
		print '\n', path
		print '\n-------------------------------------------------------------------------------------'
		return path


	def DrawGrid(self):	#Function that draw the grid, is called everytime the grid is refreshed or updated
		# Set the screen background
		self.screen.fill(BLACK)

		# Draw the grid
		for row in range(self.nHeight):			# Depending on the value on the grid fill it with the appropriate color
			for column in range(self.nWidth):
				color = WHITE
				if self.grid[row][column] == 1: # Start 
					color = GREEN
				elif self.grid[row][column] == 2: # Goal 
					color = DARKRED
				elif self.grid[row][column] == 3: # Obstacles
					color = ORANGE
				elif self.grid[row][column] == 4: # Explored Tiles
					color = LIGHTRED
				elif self.grid[row][column] == 5: # Current tile
					color = BLUE
				elif self.grid[row][column] == 6: # Nodes
					color = PURPLE
				elif self.grid[row][column] == 7: # Path
					color = RED
				pygame.draw.rect(self.screen, color, [(self.margin+self.width)*column+self.margin, (self.margin+self.height)*row+
					self.margin, self.width, self.height])
		# Limit to 60 frames per second
		self.clock.tick(60)
		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()

	def neighborLocations(self, coord):	# Function to retrieve the neighbors of a position
		row = coord[0]
		column = coord[1]
		list = []

		columnMin = max([column - 1, 0])				# the value o (X,Y) for neighbors should be a loop going from (X-1,Y-1) to (X+1,Y+1) 
		columnMax = min([column + 1, self.nWidth - 1])	# the functions MIN and MAX make sure these values wont be less than 0 or more than
		rowMin = max([row - 1, 0])						# the maximum size of our grid
		rowMax = min([row + 1, self.nHeight-1])

		for i in range(columnMin,columnMax + 1):
			for j in range(rowMin, rowMax + 1):
				if(i != column or j != row) and (self.grid[j][i] != 3):
					list.append([j,i])
		return list

	def PastCostInit(self):						# Dicts throw an exeption if an unexisting key is querried
		dict = {}								# initialize a dict with all tiles of the grid with a cost set as None
		for row in range(self.nHeight):			# A* algorithm checks if the cost is None to give the 1st update
			for column in range(self.nWidth):
				dict.update({str([row, column]):None})
		return dict

	def NodeGraphInit(self):						# Dicts throw an exeption if an unexisting key is querried
		dict = {}								# initialize the graph dict so when if the path doesnt exist the value None will be granted
		for n1 in self.nodesList:			
			for n2 in self.nodesList:
				dict.update({str(n1)+ '|' +str(n2):None})
				dict.update({str(n2)+ '|' +str(n1):None})
		return dict

	def A_Star(self, start, goal):
		print 'Using A* ...'

		graph = self.theGraph
		costGraph = self.theGraph.euclideanGraph

		open = [start]						# This is a sorted list (cost) of the open positions
		
		past_cost = self.PastCostInit()
		past_cost.update({str(start):0})			# This is a dict that has the cost to all nodes openned
		closed = []									# All the nodes that were already expanded (avoid infinite loops)
		parentDict = {str(start):None}

		while len(open) > 0:		
			current = open.pop(0)	# retrieve the first node from the open list (smallest cost so far)
			closed.append(current)	# add to closed list

			if current == goal:			# is the current node is the goal finish algorithm
				print 'PATH FOUND !!!!'
				open = []				# make open empty to finish the loop
				return parentDict, past_cost[str(current)]
			else:
				neighbors = self.neighborLocations(current) # retrieve all the neighbo coords for the current position

				print '\nITERATION'					# This prints are used for debugging
				print 'START = ', start
				print 'GOAL = ', goal
				print 'CURRENT = ', current
				print 'NEIGHBORS = ',neighbors
				print 'OPEN = ',open
				print 'CLOSED = ',closed

				nbrDict = {}	# init a tmp dict
				nbrDictHeuristic = {}
				for nbr in neighbors:
					if nbr not in closed:	# for all nbr that werent annalyzed

						self.WriteOnGrid([nbr], 4) # mark the explored nodes in the grid
						self.WriteOnGrid([current], 5) # mark the explored nodes in the grid

						tmp_cost = past_cost[str(current)] + costGraph[graph.RetrieveNode(current)][graph.RetrieveNode(nbr)] 
						# retrieve the cost spent to the current node and add it to the cost to go to the respective nbr 
						tmp_cost_heur = tmp_cost + costGraph[graph.RetrieveNode(goal)][graph.RetrieveNode(nbr)]
						#(RetrieveNode transform a [i,j] based coordinate to its node number so we can retrieve the cost from the Graph)
				
						#nbrDict.update({str(nbr):tmp_cost})							# add the cost to go to each nbr to the temp dict
						nbrDictHeuristic.update({str(nbr):tmp_cost_heur})

					if  (past_cost[str(nbr)] == None) or (tmp_cost < past_cost[str(nbr)]): # Check if we already know the cost for this NBR or if we got a better cost then before 
							past_cost.update({str(nbr):tmp_cost})		# Update the cost to this NBR
							parentDict.update({str(nbr):current})		# The CURRENT will be the new parent for NBR

				nbrCostSortedList = sorted(nbrDictHeuristic,key=nbrDictHeuristic.__getitem__)	# Sort the expanded NBRs by its cost to goal (past cost + heuristic)		
				# get a list with nbr nodes sorted according its cost 
				nbrCostSortedList = map(library.listFromStrList, nbrCostSortedList) # convert the elements of the list from a string '[i,j]' to a list [i,j] format
				print nbrDict   				# More debugging prints !!!!!
				print nbrCostSortedList
				past_cost.update(nbrDict)		# add the tmp dict to our main dict
				open = nbrCostSortedList + open	# add a list of sorted nbr according to the travel cost to open
				print 'NEW OPEN = ', open
				print '---------------------------------------------------------------------------'

			self.DrawGrid()						# Redraw the grid with the new changes
			time.sleep(0.1)						# Wait for a little bit so the user can see the changes in the grid

		return {}
			
	def DrawPathList(self, nodesGraph):
		listOfPathsAndCosts = nodesGraph.values()		# Extract only the values (paths) of our Dict that holds the graph
		listOfPaths = []
		for lPC in listOfPathsAndCosts:					# Remove the costs since we only need the path list
			listOfPaths.append(lPC.pop(0))
		for path in listOfPaths:
			self.WriteOnGrid(path, 7)
		self.WriteOnGrid(self.nodesList, 6)
		self.WriteOnGrid([self.startPos], 1)
		self.WriteOnGrid([self.goalPos], 2)


	def PlanToGoal(self):						# Function to encapsulate the A* (Computer Scientist habbits never dies!)
		print 'Planning to goal ...'
		resultGraph_Astar = self.NodeGraphInit()
		for node in self.nodesList:
			for expNode in self.nodesList:
				if resultGraph_Astar[str(node)+ '|' +str(expNode)] == None:
					resultPath, cost = self.A_Star(node, expNode)
					resultPathList = self.WritePath(resultPath, node, expNode)
					resultGraph_Astar.update({str(node)+ '|' +str(expNode):[resultPathList, cost]})
					resultPathList.reverse()
					resultGraph_Astar.update({str(expNode)+ '|' +str(node):[resultPathList, cost]})
					if len(resultPath) == 0:
						print '\n\nThere is NO path between', node,' and ', expNode
					else:
						print '\n\nPath FOUND between', node,' and ', expNode
					self.ClearTmpTiles([4,7])
		self.DrawPathList(resultGraph_Astar)
		self.outputNodesPath = resultGraph_Astar
		

	def DrawObstacleCircle(self, cCenter, cRadius):		# Use a A* similar technich to select the tiles that must contain the circle
		self.obstaclesCirclesList.append(library.ObstacleCircle(cCenter[0], cCenter[1], cRadius)) #append the circle in the obstacle list
		listToDraw = [cCenter]
		openCircles = [cCenter]
		closedCircles = []
		while len(openCircles) > 0:
			currentCircle = openCircles.pop(0)
			closedCircles.append(currentCircle)
			nbrCirclesList = self.neighborLocations(currentCircle)
			for nbrCircle in nbrCirclesList:
				if nbrCircle not in closedCircles:
					distance = self.theGraph.euclideanGraph[self.theGraph.RetrieveNode(cCenter)][self.theGraph.RetrieveNode(nbrCircle)]	
					if (cRadius >= distance):					# in order to be in the circle the euclidean distance to the center must be less or equal than the ratio value
						listToDraw.append(nbrCircle)
						openCircles = [nbrCircle] + openCircles
		self.WriteOnGrid(listToDraw,3)


	def Start(self):											# Function to initialize the grid

		self.screen = pygame.display.set_mode(self.size)

		#Loop until the user clicks the close button.
		done = False

		self.clock = pygame.time.Clock()
																# -------- Main Program Loop -----------
		while done == False:
			for event in pygame.event.get(): 					# User did something
				if event.type == pygame.QUIT: 					# If user clicked close
					done = True 								# Flag that we are done so we exit this loop
				elif event.type == pygame.MOUSEBUTTONDOWN:
																# User clicks the mouse. Get the position
					pos = pygame.mouse.get_pos()
																# Change the x/y screen coordinates to grid coordinates
					column = pos[0] // (self.width + self.margin)
					row = pos[1] // (self.height + self.margin)
																# Set that location to zero
					self.grid[row][column] = self.clickCount	# Update the grid tile with the respective value (1=GOAL | 2=START | 3=OBSTACLES)
					if self.clickCount <= 2:
						if self.clickCount == 1:
							self.startPos = [row,column]			# Saves the start position in a class variable
							self.nodesList.append(self.startPos)	#add to the nodes list
						elif self.clickCount == 2:
							self.goalPos = [row,column]				# Saves the goal position in a class variable
							self.nodesList.append(self.goalPos)		# add to the nodes list
						self.clickCount += 1
					elif self.clickCount == 3:					
						self.DrawObstacleCircle([row,column], self.inputCircleRadius)	# call a function to draw the obstacle circle
					elif self.clickCount == 6:
						print '\nNew node added.'
						self.nodesList.append([row,column])
					print("Click ", pos, "Grid coordinates: ", row, column)
				elif event.type == pygame.KEYDOWN:				# capture keyboard keys
					if event.key == pygame.K_SPACE:
						print 'START'
						self.PlanToGoal()
					if event.key == pygame.K_s:
						print 'Select a START position:'
						self.clickCount = 1
					if event.key == pygame.K_g:
						print 'Select a GOAL position:'
						self.clickCount = 2
					if event.key == pygame.K_r:
						print '\n'
						self.inputCircleRadius = int(input("Enter Radius in tiles of your circle: "))
						self.clickCount = 3
					if event.key == pygame.K_p:
						print '\nOpening math plot lib ...'
						library.plotRoadMap(self.nHeight, self.nWidth, self.obstaclesCirclesList, [])
					if event.key == pygame.K_q:
						print '\nClosing  ...'
						done = True
					if event.key == pygame.K_n:
						print '\nClick to add new nodes.'
						self.clickCount = 6
					if event.key == pygame.K_o:
						print '\nReady to add obstacles!!!'
						self.clickCount = 3
					if event.key == pygame.K_c:
						print '\nClearing temp tile colors ...'
						self.ClearTmpTiles([4,5,7])

			self.DrawGrid()
			
		# Be IDLE friendly. If you forget this line, the program will 'hang'
		# on exit.
		pygame.quit()


if __name__ == '__main__':
	theGrid = TheGrid(20,20)
	theGrid.Start()