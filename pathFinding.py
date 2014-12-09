#!/usr/bin/env python

import math
import gkUtilities as gk


theListOfNodes = None 			# a list for all the graph nodes
theGraphOfNodes = None			# 2D array that works as the graph matrix
theListCircles = None			# list of all the circular obstacles
NO_PATH = -1 					# if there s no path between nodes this value is assigned


def Plot(listNodes, listCircles):
	gk.plotRoadMap(100,100,listNodes,listCircles)

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

def touchCircle():
	pass


def isStraightLine():
	pass


def A_Star():
	pass


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
	theListOfNodes = [n0,n1,n2,n3,n4,n5,n6,n7,n8]	# List of the coordinates of all nodes
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



