#!/usr/bin/env python

import math
import gkUtilities as gk


theListOfNodes = None 			# a list for all the graph nodes
theGraphOfNodes = None			# 2D array that works as the graph matrix
theListCircles = None			# list of all the circular obstacles
NO_PATH = -1 					# if there s no path between nodes this value is assigned


def Plot(listNodes, listCircles, graph, start, goal, pathTree):
	path = []
	if pathTree != None:
		node = goal
		path = [goal]
		while pathTree[node] != None:
			node = pathTree[node]
			path = [node] + path
	print '\nSolution Path: ',path

	gk.plotRoadMap(100,100,listNodes,listCircles, graph, start, goal,path)

def getEuclideanDist(n1, n2):	# returns the euclidean distance between 2 nodes
	return math.sqrt(math.pow(n2[1]-n1[1],2) + math.pow(n2[0]-n1[0],2))


def create2DGraph(listNodes):	#returns a 2D array that has the costs between the nodes G(i,j)=G(j,i)= euclideanCost(j,i)
	graph = []					# G(i,i) = 0

	for i in listNodes:
		row = []
		for j in listNodes:
			row.append(getEuclideanDist(i,j))
		graph.append(row)
	return graph


def isNodeInAnyCircle(node, listOfCircles):	# detects if a node is inside of any circle in the list of circles
	for c in listOfCircles:
		eucDist = getEuclideanDist(node,[c.row, c.column])
		if eucDist <= c.radio:				# if the euclidean distance is less than a radius of a circle it is touching it
			return True
	else:
		return False

def removeNodesInCircle(listOfNodes, listOfCircles, graph):	# is a node is inside a circle make all the costs from it and to it  equals the NO_PATH value
	global NO_PATH

	tmpGraph = graph
	nRows = len(tmpGraph)
	nColumn = len(tmpGraph[0])

	for index in range(len(listOfNodes)):
		if isNodeInAnyCircle(listOfNodes[index], listOfCircles):
			invalidLine = [NO_PATH] * nColumn		# creates a new row of invalid values
			tmpGraph[index] = invalidLine				# raplace row
			for i in range(nRows):
				tmpGraph[i][index] = NO_PATH			# update the whole column with invalid values
	return tmpGraph

def willItTouchCircle(point1, point2, circle):
	# compute the euclidean distance between A and B
	Ax = point1[1]
	Ay = point1[0]

	Bx = point2[1]
	By = point2[0]

	Cx = circle.column
	Cy = circle.row
	Cr = circle.radio

	m = By - Ay / Bx - Ax

	mInv = -1/m

	b1 = Ay - m * Ax
	b2 = Cy - mInv * Cx

	Ix = (b2 - b1) / (m - mInv)
	Iy = m * Ix + b1

	distItoC = getEuclideanDist([Ix,Iy],[Cx,Cy])

	if distItoC <= Cr:
		print '\nTouch CIRCLE!'
		return True
	else:
		print '\nDo NOT Touch CIRCLE!'
		return False

def removeEdgesTouchingCircle(listNodes, graph, listCircles):
	global NO_PATH
	tmpGraph = graph

	for i in range(len(listNodes)):
		for j in range(len(listNodes)):
			for circle in listCircles:
				if listNodes[i] != listNodes[j] and willItTouchCircle(listNodes[i],listNodes[j],circle):
					tmpGraph[i][j] = NO_PATH
	return tmpGraph

def getNeighbors(nodeN, graph):
	nbrs = []

	for i in range(len(graph[nodeN])):
		if nodeN != i and graph[nodeN][i] >= 0:	# if the cost is negatice it means theres no possible path, so its not a nbr
			nbrs.append(i)
	return nbrs

def A_Star(graph, listNodes, start, goal):
	open = [start]
	past_cost = {start:0}
	closed = []
	parent = {start:None}

	current = None

	while len(open) > 0:
		current = open.pop(0)

		print '\nCURRENT = ',current
		print 'OPEN = ', open
		print 'CLOSED = ', closed

		if current not in closed:
			closed.append(current)
			if current == goal:
				print '\nA* Path Found'
				return parent, past_cost[current]
			else:
				nbrs = getNeighbors(current,graph)

				heuristicDict = {}
				for nbr in nbrs:
					tmpCost = past_cost[current] + graph[current][nbr]
					heuristicCost = tmpCost + getEuclideanDist(listNodes[current],listNodes[nbr])
					heuristicDict.update({nbr:heuristicCost})

					if nbr not in past_cost.keys() or tmpCost < past_cost[nbr]:
						past_cost.update({nbr:tmpCost})
						parent.update({nbr:current})

				# Sort the neighbors by its heuristic cost and insert it into the open list
				sortedNbrsList = sorted(heuristicDict,key=heuristicDict.__getitem__)
				open = sortedNbrsList + open 	#CHANGED
	print '\nA* Path NOT Found'
	return {}, -1 


def Main(nodeGraph, start, goal, circleList, robotRadius):
	pass 


def Init():
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
	theListOfNodes = [n0,n1,n2,n3,n4,n5,n6,n7,n8]		# List of the coordinates of all nodes (ORDER MATTER)
	theGraphOfNodes = create2DGraph(theListOfNodes)		# 2D Array that is the cost graph between nodes can be custom initialized

	c0 = gk.ObstacleCircle(10,69,12)
	c1 = gk.ObstacleCircle(39,28,18)
	c2 = gk.ObstacleCircle(50,45,8)
	c3 = gk.ObstacleCircle(68,93,10)
	c4 = gk.ObstacleCircle(72,75,13)
	c5 = gk.ObstacleCircle(90,73,10)
	theListCircles = [c0,c1,c2,c3,c4,c5]


	


if __name__ == '__main__':
	Init()



