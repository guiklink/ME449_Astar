#!/usr/bin/env python

import pygame
import library
import time

# Define some colors for the tiles
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHTRED = (255, 200, 200)
ORANGE = (255, 128, 0)
BLUE = (0, 0, 255)

class TheGrid:	#This class hols the main skeleton of the program, it will create the pygame grid and call all the necessary functions
	def __init__(self, nWidth, nHeight): 	# define the dimensions of your grid
		self.outputParents = None			#this variable is used for debugging

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

		self.clickCount = 3 	# 1 = set START | 2 = set GOAL | 3 = set OBSTACLES
		self.startPos = None	
		self.goalPos = None


		self.theGraph = library.Graph(self.nHeight, self.nWidth)	# Initialize the graph library that handle euclidean cost graphs
		print '\nCreating Cost Graph...'
		self.theGraph.CreateGraph()									# Initialize the enclidean cost graph 
		print '\nCost Graph created!'

		self.inputCircleRadius = 1
		self.obstaclesCircles = []										# a list for all circular obstacles

	
	def RestartTiles(self):
		self.grid = []

		for row in range(self.nWidth):	# Loops to initializa the tiles list
			# Add an empty array that will hold each cell
			# in this row
			self.grid.append([])
			for column in range(self.nHeight):
				self.grid[row].append(0) # Append a cell


	def WriteOnGrid(self, list, value):				# Function that receive a list of [i,j] positions and write a value on it
		for pos in list:
			self.grid[pos[0]][pos[1]] = value

	def WritePath(self, parents):					# Function that receive a dict of nodes and its parents and draw sets the values in the grid for final path
		print '\n\nPARENTS = ',parents
		pathNode = self.goalPos
		path = [pathNode]

		while pathNode != self.startPos:		# While not in the START position keep looking for the parent 
			pathNode = parents[str(pathNode)]	# Build the path list in a reverse way
			path.append(pathNode)
		self.WriteOnGrid(path, 2)
		path.reverse()							# Unreverse the list in order to print it in the right order
		self.outputParents = parents
		print '\n\n---------------------- PATH TO GOAL -------------------------------------------------'
		print '\n', path
		print '\n-------------------------------------------------------------------------------------'


	def DrawGrid(self):	#Function that draw the grid, is called everytime the grid is refreshed or updated
		# Set the screen background
		self.screen.fill(BLACK)

		# Draw the grid
		for row in range(self.nHeight):			# Depending on the value on the grid fill it with the appropriate color
			for column in range(self.nWidth):
				color = WHITE
				if self.grid[row][column] == 1: # Empty tiles 
					color = GREEN
				elif self.grid[row][column] == 2: # Goal 
					color = RED
				elif self.grid[row][column] == 3: # Obstacles
					color = ORANGE
				elif self.grid[row][column] == 4: # Explored Tiles
					color = LIGHTRED
				elif self.grid[row][column] == 5: # Current tile
					color = BLUE
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

	def PastCostInit(self):
		dict = {}
		for row in range(self.nHeight):
			for column in range(self.nWidth):
				dict.update({str([row, column]):None})
		return dict

	def A_Star(self):
		print 'Using A* ...'

		graph = self.theGraph
		costGraph = self.theGraph.euclideanGraph

		open = [self.startPos]						# This is a sorted list (cost) of the open positions
		
		past_cost = self.PastCostInit()
		past_cost.update({str(self.startPos):0})	# This is a dict that has the cost to all nodes openned
		closed = []									# All the nodes that were already expanded (avoid infinite loops)
		parentDict = {str(self.startPos):None}

		while len(open) > 0:		
			current = open.pop(0)	# retrieve the first node from the open list (smallest cost so far)
			closed.append(current)	# add to closed list

			if current == self.goalPos:	# is the current node is the goal finish algorithm
				print 'PATH FOUND !!!!'
				open = []				# make open empty to finish the loop
				self.WritePath(parentDict)
				return parentDict
			else:
				neighbors = self.neighborLocations(current) # retrieve all the neighbo coords for the current position

				print '\nITERATION'					# This prints are used for debugging
				print 'START = ', self.startPos
				print 'GOAL = ', self.goalPos
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
						tmp_cost_heur = tmp_cost + costGraph[graph.RetrieveNode(self.goalPos)][graph.RetrieveNode(nbr)]
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
			time.sleep(0.2)						# Wait for a little bit so the user can see the changes in the grid

		return {}

	def IsPathStraighLine(self, parents):
		x1 = self.startPos[1]
		y1 = self.startPos[0]
		x2 = self.goalPos[1]
		y2 = self.goalPos[0]

		print 'x1 = ',x1
		print 'y1 = ',y1
		print 'x2 = ',x2
		print 'y2 = ',y2

		m = (y2 - y1) / (x2 - x1)

		print '\nLine Equation: y - ',y1,' = ', m, ' * (x - ', x1,')'

		pathNode = self.goalPos

		while pathNode != self.startPos:		# While not in the START position keep looking for the parent 
			if pathNode[0]-y1!=m*(pathNode[1]-x1):
				return False
			pathNode = parents[str(pathNode)]
		return True	
			

	def PlanToGoal(self):						# Function to encapsulate the A* (Computer Scientist habbits never dies!)
		print 'Planning to goal ...'
		result = self.A_Star()
		if len(result) == 0:
			print '\n\nThere is no path for this goal!!!'
		else:
			if self.IsPathStraighLine(result):
				print '\nIt is a line!'
			else:
				print '\nIt is NOT a line!'


	def DrawObstacleCircle(self, cCenter, cRadius):
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
					if (cRadius >= distance):
						listToDraw.append(nbrCircle)
						openCircles = [nbrCircle] + openCircles
		self.WriteOnGrid(listToDraw,3)


	def Start(self):							# Function to initialize the grid

		self.screen = pygame.display.set_mode(self.size)

		#Loop until the user clicks the close button.
		done = False

		self.clock = pygame.time.Clock()
		# -------- Main Program Loop -----------
		while done == False:
			for event in pygame.event.get(): # User did something
				if event.type == pygame.QUIT: # If user clicked close
					done = True # Flag that we are done so we exit this loop
				elif event.type == pygame.MOUSEBUTTONDOWN:
					# User clicks the mouse. Get the position
					pos = pygame.mouse.get_pos()
					# Change the x/y screen coordinates to grid coordinates
					column = pos[0] // (self.width + self.margin)
					row = pos[1] // (self.height + self.margin)
					# Set that location to zero
					self.grid[row][column] = self.clickCount
					if self.clickCount <= 2:
						if self.clickCount == 1:
							self.startPos = [row,column]
						elif self.clickCount == 2:
							self.goalPos = [row,column]
						self.clickCount += 1
					elif self.clickCount == 3:
						self.DrawObstacleCircle([row,column], self.inputCircleRadius)
					print("Click ", pos, "Grid coordinates: ", row, column)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						print 'START'
						self.PlanToGoal()
					if event.key == pygame.K_s:
						print 'Select a START position:'
						self.clickCount = 1
					if event.key == pygame.K_g:
						print 'Select a GOAL position:'
						self.clickCount = 2
					if event.key == pygame.K_c:
						self.inputCircleRadius = int(input("Enter Radius in tiles of your circle: "))
						self.clickCount = 3

			self.DrawGrid()
			
		# Be IDLE friendly. If you forget this line, the program will 'hang'
		# on exit.
		pygame.quit()


if __name__ == '__main__':
	theGrid = TheGrid(40,40)