#!/usr/bin/env python

import numpy as np
import math


class Graph:
	def __init__(self, map):
		self.map = map
		self.dim = map.size
		self.dimX = map[0].size
		self.dimY = map.size/map[0].size

	def RetrieveCoord(self,node):
		return node / self.dimY, node % self.dimX

	def DistanceList(self,node):
		dList = []
		nY, nX = self.RetrieveCoord(node)

		for i in range(0,self.dim):
			gY, gX = self.RetrieveCoord(i)
			euclidean = math.sqrt(math.pow(nY - gY,2) + math.pow(nX - gX,2))
			dList.append(euclidean)

		return dList

	def CreateGraph(self):
		dim = self.map.size
		graph = []
		for i in range(0,dim):
			graph.append(self.DistanceList(i))
		return np.reshape(graph,[dim,dim])


if __name__ == '__main__':
	testArray = range(0,9)
	matrixTest = np.reshape(testArray,[3,3])
	graphTest = Graph(matrixTest)