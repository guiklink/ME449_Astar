#!/usr/bin/env python

import numpy as np
import math
import matplotlib.pyplot as plt
from pylab import MultipleLocator

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

class ObstacleCircle:
	def __init__(self, x, y, radio):
		self.x = x
		self.y = y
		self.radio = radio
		

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

def plotRoadMap(rows, columns, circleObstList, pathList):

		plt.axis([0,columns-1,rows-1,0])

		fig = plt.gcf()

		toPlot = plt.subplot(111)

		toPlot.xaxis.set_major_locator(MultipleLocator(columns/20))	# Set grid interval for axis X
		toPlot.yaxis.set_major_locator(MultipleLocator(rows/20))	# Set grid interval for axis Y

		toPlot.xaxis.grid(True,'major',linewidth=1)			# Plot grids
		toPlot.yaxis.grid(True,'major',linewidth=1)

		toPlot.yaxis

		xPath = []
		yPath = []

		for pos in pathList:
			xPath.append(pos.x + 0.5)		# load all the positions of X in the list to plot
			yPath.append(pos.y + 0.5)		# load all the positions of Y in the list to plot

		plt.plot(xPath,yPath)				# Plot line blue line
		plt.plot(xPath, yPath, 'bo', label='Positions')	# Plot circles blue circles

		#print '\n\nPlotting obstacles...'
		for circle in circleObstList:
			circle=plt.Circle((circle.y,circle.x),circle.radio,color='#FFA500')
			fig.gca().add_artist(circle)
			

		plt.show()	# Plot it