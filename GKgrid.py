#!/usr/bin/env python

import pygame
import library
import time

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHTRED = (255, 200, 200)
ORANGE = (255, 128, 0)
BLUE = (0, 0, 255)

class TheGrid:
	def __init__(self, nWidth, nHeight):
		self.output = None
		self.costMatrix = None

		self.nWidth = nWidth
		self.nHeight = nHeight

		self.width = 600 / nWidth
		self.height = 600 / nHeight
		self.margin = 1
		self.grid = []

		for row in range(nWidth):
			# Add an empty array that will hold each cell
			# in this row
			self.grid.append([])
			for column in range(nHeight):
				self.grid[row].append(0) # Append a cell

		pygame.init()

		self.size = [600 + nWidth,600 + nHeight]
		# Set title of screen
		pygame.display.set_caption("A* Grid")

		self.screen = None
		# Used to manage how fast the screen updates
		self.clock = None

		self.clickCount = 1 	# 1 = set START | 2 = set GOAL | 3 = set OBSTACLES
		self.startPos = None
		self.goalPos = None

	def WriteOnGrid(self, list, value):
		for pos in list:
			self.grid[pos[0]][pos[1]] = value

	def WritePath(self, parents):
		print '\n\nPARENTS = ',parents
		pathNode = self.goalPos
		path = [pathNode]

		while pathNode != self.startPos:
			pathNode = parents[str(pathNode)]
			path.append(pathNode)
		self.WriteOnGrid(path, 2)
		path.reverse()
		self.output = parents
		print '\n\nPATH TO GOAL = ', path


	def DrawGrid(self):
		# Set the screen background
		self.screen.fill(BLACK)

		# Draw the grid
		for row in range(self.nHeight):
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

	def neighborLocations(self, coord):	
		row = coord[0]
		column = coord[1]
		list = []

		columnMin = max([column - 1, 0])					# the value o (X,Y) for neighbors should be a loop going from (X-1,Y-1) to (X+1,Y+1) 
		columnMax = min([column + 1, self.nWidth - 1])	# the functions MIN and MAX make sure these values wont be less than 0 or more than
		rowMin = max([row - 1, 0])					# the maximum size of our grid
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

	def A_Star(self, graph):
		print 'Using A* ...'

		costGraph = graph.CreateGraph()

		self.costMatrix = costGraph

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
			else:
				neighbors = self.neighborLocations(current) # retrieve all the neighbo coords for the current position

				print '\nITERATION'
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

					if  (past_cost[str(nbr)] == None) or (tmp_cost < past_cost[str(nbr)]):
							past_cost.update({str(nbr):tmp_cost})
							parentDict.update({str(nbr):current})

				nbrCostSortedList = sorted(nbrDictHeuristic,key=nbrDictHeuristic.__getitem__)			
				# get a list with nbr nodes sorted according its cost 
				nbrCostSortedList = map(library.listFromStrList, nbrCostSortedList) # convert the elements of the list from a string '[i,j]' to a list [i,j] format
				print nbrDict
				print nbrCostSortedList
				past_cost.update(nbrDict)		# add the tmp dict to our main dict
				open = nbrCostSortedList + open	# add a list of sorted nbr according to the travel cost to open
				print 'NEW OPEN = ', open
				print '---------------------------------------------------------------------------'

			self.DrawGrid()
			time.sleep(0.2)



	def PlanToGoal(self):
		print 'Planning to goal ...'
		theGraph = library.Graph(self.nHeight, self.nWidth)
		self.A_Star(theGraph)


	def Start(self):

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
					print("Click ", pos, "Grid coordinates: ", row, column)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						print 'START'
						self.PlanToGoal()

			self.DrawGrid()
			
		# Be IDLE friendly. If you forget this line, the program will 'hang'
		# on exit.
		pygame.quit()


if __name__ == '__main__':
	theGrid = TheGrid(10,10)