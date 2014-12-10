#!/usr/bin/env python

import math
import gkUtilities as gk
import random as rd


theListOfNodes = None 			# a list for all the graph nodes
theGraphOfNodes = None			# 2D array that works as the graph matrix
theListCircles = None			# list of all the circular obstacles
NO_PATH = -1 					# if there s no path between nodes this value is assigned


def Plot(listNodes, listCircles, graph, start, goal, pathTree):
	path = []							# build the path from pathTree in this node
	if pathTree != None:
		node = goal
		path = [goal]
		while pathTree[node] != None:	# explore the tree until the father None which is the parent first node
			node = pathTree[node]
			path = [node] + path
	print '\nSolution Path: ',path

	gk.plotRoadMap(100,100,listNodes,listCircles, graph, start, goal,path)	# call plotting function in my library

def getEuclideanDist(n1, n2):	# returns the euclidean distance between 2 nodes
	return math.sqrt(math.pow(n2[1]-n1[1],2) + math.pow(n2[0]-n1[0],2))


def create2DGraph(listNodes):	#returns a 2D array that has the costs between the nodes G(i,j)=G(j,i)= euclideanCost(j,i)
	graph = []					# G(i,i) = 0
								# Follows the graph specifications from the question #1
	for i in listNodes:
		row = []
		for j in listNodes:
			row.append(getEuclideanDist(i,j))
		graph.append(row)
	return graph


def isNodeInAnyCircle(node, listOfCircles, robotRadius):	# detects if a node is inside of any circle in the list of circles
	for c in listOfCircles:
		eucDist = getEuclideanDist(node,[c.row, c.column])
		if (eucDist - robotRadius) <= c.radio:				# if the euclidean distance is less than a radius of a circle it is touching it
			return True
	return False

def removeNodesInCircle(listOfNodes, listOfCircles, graph, robotRadius):	# is a node is inside a circle make all the costs from it and to it  equals the NO_PATH value
	global NO_PATH					# variable with the cost for an invalid edge

	tmpGraph = graph 				# store the graph into a manipulable temp variable
	nRows = len(tmpGraph) 			# number of rows
	nColumn = len(tmpGraph[0]) 		# number of columns

	for index in range(len(listOfNodes)):
		if isNodeInAnyCircle(listOfNodes[index], listOfCircles,robotRadius):
			invalidLine = [NO_PATH] * nColumn		# creates a new row of invalid values
			tmpGraph[index] = invalidLine				# raplace row
			for i in range(nRows):
				tmpGraph[i][index] = NO_PATH			# update the whole column with invalid values
	return tmpGraph

def willItTouchCircle(point1, point2, circle,robotRadius):
	Ax = float(point1[1])					# Coordinates for point A
	Ay = float(point1[0])

	Bx = float(point2[1])					# Coordinates for point B
	By = float(point2[0])

	Cx = float(circle.column)				# Coordinates for circle center
	Cy = float(circle.row)
	Cr = float(circle.radio) + robotRadius	# Circle radius

	print '\nNode\npoint1 ', point1
	print 'point2 ', point2

	if Ay != By and Ax != Bx:		# for the case when m (slope) is not 0
		m = (By - Ay) / (Bx - Ax)	# calculate m
		print 'By = ',By
		print 'Ay = ',Ay
		print 'Bx = ',Bx
		print 'Ax = ',Ax
		print 'M = ',m
		mInv = -1/m 				# slope of the orthogonal line

		b1 = Ay - m * Ax 			# points of the ortogonal
		b2 = Cy - mInv * Cx			

		Ix = (b2 - b1) / (m - mInv) # calculate points in the intersection 
		Iy = m * Ix + b1
	elif Ay == By: 					# for the cases where the lines share a coordinate
		Ix = Cx
		Iy = Ay
	elif Ax == Bx:
		Ix = Ax
		Iy = Cy

	distItoC = getEuclideanDist([Ix,Iy],[Cx,Cy]) 	# distance intersection to circle center 
	dist1to2 = getEuclideanDist(point2,point1)		# distance from point 1 to 2
	dist1toC = getEuclideanDist([Cy,Cx],point1)		# distance point 1 to circle center
	dist2toC = getEuclideanDist([Cy,Cx],point2) 	# distance point 2 to circle center


	if distItoC <= Cr and dist1to2 > dist1toC and dist1to2 > dist2toC : # !!! use some trigonometric triangulations
		print '\nTouch CIRCLE!'
		return True
	else:
		print '\nDo NOT Touch CIRCLE!'
		return False
	


def removeEdgesTouchingCircle(listNodes, graph, listCircles,robotRadius): # this function will use willItTouchCircle to set NO_PATH values for the edges that touch an obstacle
	global NO_PATH
	tmpGraph = graph

	for i in range(len(listNodes)): # iterate to compare each node with each other from the list
		for j in range(len(listNodes)):
			for circle in listCircles:
				if listNodes[i] != listNodes[j] and willItTouchCircle(listNodes[i],listNodes[j],circle,robotRadius): # if the nodes are not the same and the straight line between then touch an obstacle remove edge
					tmpGraph[i][j] = NO_PATH
	return tmpGraph

def getNeighbors(nodeN, graph): 	# given a node and my graph retrieve a list with all the neighbors of the node
	nbrs = []		

	for i in range(len(graph[nodeN])):
		if nodeN != i and graph[nodeN][i] >= 0:	# if the cost is negatice it means theres no possible path, so its not a nbr
			nbrs.append(i)						# append all nbr that have an edge to my node (!= -1)
	return nbrs

def A_Star(graph, listNodes, start, goal):
	open = {start:9999999}						# open is a dict that holds nodes and its total_cost
	past_cost = {start:0}						# past_cost is a dict that have the node and the real cost to it
	closed = [] 								# closed is a list of the explored nodes
	parent = {start:None} 						# parent is a dict of a node and its parent, will work as a tree

	current = None

	while len(open) > 0: 						# if open gets empty and the goal wasnt found it means theres no possible way to the goal
		# Sort nodes by heuristic cost before retrieving it
		sortedOpenList = sorted(open,key=open.__getitem__) 	# retrieves a a list of nodes sorted by total_cost from open
		current = sortedOpenList[0] 						# makes the first element as current

		del(open[current]) 									# remove the element from the open list

		print '\nCURRENT = ',current 						# some prints for debugging
		print 'OPEN = ', open
		print 'CLOSED = ', closed

		if current not in closed: 							# if current wasnt already explored
			closed.append(current) 							# include it in the closed list
			if current == goal: 							# if the node being explored is the goal a path was found
				print '\nA* Path Found'
				return parent, past_cost[current] 			# return the dict of parents and the cost to it
			else:
				nbrs = getNeighbors(current,graph) 			# retrieve nbrs of current

				heuristicDict = {} 							# temp dict to store the nbr and its total cost
				for nbr in nbrs:
					tmpCost = past_cost[current] + graph[current][nbr] # calculates the cost to nbr comming from current
					heuristicCost = tmpCost #+ getEuclideanDist(listNodes[current],listNodes[nbr]) #calculate total cost summing the real cost + an heuristic value
					heuristicDict.update({nbr:heuristicCost}) 	# load the values in the temp dict

					if nbr not in past_cost.keys() or tmpCost < past_cost[nbr]: # if the new cost found for nbr is better than the one we had before update the cost and who is the better parent for nbr
						past_cost.update({nbr:tmpCost})
						parent.update({nbr:current})

				
				open.update(heuristicDict) # add the values from the temp dict into open list
	print '\nA* Path NOT Found'
	return {}, -1 


def Main(start, goal, robotRadius): 		# Main function works as a script
	global theGraphOfNodes, theListCircles, theListOfNodes

	# Show the map
	Plot(theListOfNodes,theListCircles,None,start,goal,None)

	# Show map with all connections
	Plot(theListOfNodes,theListCircles,theGraphOfNodes,start,goal,None)

	# Remove nodes inside circles 
	theGraphOfNodes = removeNodesInCircle(theListOfNodes, theListCircles,theGraphOfNodes,robotRadius)

	Plot(theListOfNodes,theListCircles,theGraphOfNodes,start,goal,None)

	# Remove the edges touching circles
	theGraphOfNodes = removeEdgesTouchingCircle(theListOfNodes, theGraphOfNodes, theListCircles,robotRadius)

	Plot(theListOfNodes,theListCircles,theGraphOfNodes,start,goal,None)

	# Execute A* storing the parent tree and the cost to goal
	parentTree,cost = A_Star(theGraphOfNodes, theListOfNodes, start, goal)

	print '\n\n=> The path COST is: ', cost

	if cost == -1:
		print '\n----------------------------------'
		print '| IS NOT POSSIBLE TO FIND A PATH |'
		print '----------------------------------\n'
	else:
		# Plot solution path 
		Plot(theListOfNodes,theListCircles,theGraphOfNodes,start,goal,parentTree)


def Init(): 											# initialize values to be used by my A*
	global theGraphOfNodes, theListCircles, theListOfNodes

	n0 = [15,18]
	n1 = [10,45]
	n2 = [43,5]
	n3 = [40,78]
	n4 = [58,37]
	n5 = [73,22]
	n6 = [89,55]
	n7 = [91,90]
	n8 = [75,69]
	theListOfNodes = [n0,n1,n2,n3,n4,n5,n6,n7,n8]		# List of the coordinates of all nodes 
	theGraphOfNodes = create2DGraph(theListOfNodes)		# 2D Array that is the cost graph between nodes can be custom initialized

	c0 = gk.ObstacleCircle(10,69,12) 					
	c1 = gk.ObstacleCircle(39,28,18)
	c2 = gk.ObstacleCircle(50,45,8)
	c3 = gk.ObstacleCircle(68,93,10)
	c4 = gk.ObstacleCircle(72,75,13)
	c5 = gk.ObstacleCircle(90,73,10)
	theListCircles = [c0,c1,c2,c3,c4,c5]

def loadRandomScenario():
	global theGraphOfNodes, theListCircles, theListOfNodes

	nNodes = 10
	theListOfNodes = []
	for i in range(nNodes):
		theListOfNodes.append([rd.random()*100,rd.random()*100])
	
	theGraphOfNodes = create2DGraph(theListOfNodes)

	nCircles = 30
	theListCircles = []
	for i in range(nCircles):
		theListCircles.append(gk.ObstacleCircle(rd.random()*100,rd.random()*100,rd.random()*10))
	

if __name__ == '__main__':
	Init()



