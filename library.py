#!/usr/bin/env python

import numpy as np
import math

def listFromStrList(str):
	l = list(str)
	l = filter(lambda a: a != ' ', l)
	l = filter(lambda a: a != '[', l)
	l = filter(lambda a: a != ']', l)

	strl = ''.join(l)
	res = strl.split(',')

	coord = [int(res[0]),int(res[1])]

	return coord

def MatrixOfNodes(rows,columns):
	array2D = []

	counterInit = 0
	counterFinal = columns
	for i in range(rows):
		array2D.append(range(counterInit,counterFinal))
		counterInit += columns
		counterFinal += columns
	return array2D

class Graph:
	def __init__(self, rows, columns):
		self.map = MatrixOfNodes(rows, columns)
		self.dim = rows * columns
		self.dimX = columns
		self.dimY = rows

		self.euclideanGraph = None

	def RetrieveCoord(self,node):
		return node / self.dimY, node % self.dimX

	def RetrieveNode(self, coord):
		return self.map[coord[0]][coord[1]]

	def DistanceList(self,node):
		dList = []
		nY, nX = self.RetrieveCoord(node)

		for i in range(0,self.dim):
			gY, gX = self.RetrieveCoord(i)
			euclidean = math.sqrt(math.pow(nY - gY,2) + math.pow(nX - gX,2))
			dList.append(euclidean)

		return dList

	def CreateGraph(self):
		graph = []
		for i in range(0,self.dim):
			graph.append(self.DistanceList(i))
		self.euclideanGraph = graph


class Node:
	def __init__(self, node, parent):
		self.node = node
		self.parent = parent
