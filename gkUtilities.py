#!/usr/bin/env python

import numpy as np
import math
import matplotlib.pyplot as plt
from pylab import MultipleLocator

class ObstacleCircle:
	def __init__(self, row, column, radio):
		self.row = row
		self.column = column
		self.radio = radio


def plotRoadMap(rows, columns, listOfNodes,circleObstList,graph, start, goal,path):

		plt.axis([0,columns-1,rows-1,0])

		fig = plt.gcf()

		toPlot = plt.subplot(111)

		toPlot.xaxis.set_major_locator(MultipleLocator(columns/20))	# Set grid interval for axis X
		toPlot.yaxis.set_major_locator(MultipleLocator(rows/20))	# Set grid interval for axis Y

		toPlot.xaxis.grid(True,'major',linewidth=1)			# Plot grids
		toPlot.yaxis.grid(True,'major',linewidth=1)

		# Plot the nodes
		startNode = listOfNodes[start]
		goalNode = listOfNodes[goal]
		for node in listOfNodes:
			xPath = []
			yPath = []
			xPath.append(node[1])							# load all the positions of X in the list to plot
			yPath.append(node[0])							# load all the positions of Y in the list to plot

			if node == startNode:
				plt.plot(xPath, yPath, 'g^', label='Positions')	# Plot red dots
			elif node == goalNode:
				plt.plot(xPath, yPath, 'r^', label='Positions')	# Plot red dots
			else:
				plt.plot(xPath, yPath, 'yo', label='Positions')	# Plot red dots


		# Plot the edges between nodes
		if graph != None:
			for i in range(len(listOfNodes)):
				for j in range(len(listOfNodes)):
					if graph[i][j] > 0:
						xPath = []
						yPath = []
						xPath = [listOfNodes[i][1],listOfNodes[j][1]]	# load all the positions of X in the list to plot
						yPath = [listOfNodes[i][0],listOfNodes[j][0]]	# load all the positions of Y in the list to plot
						plt.plot(xPath,yPath, 'b')						# Plot line blue line

		# Plot the path to the goal
		xPath = []
		yPath = []
		if path != None:
			for nodeIndex in path:
				node = listOfNodes[nodeIndex]
				xPath.append(node[1])			# load all the positions of X in the list to plot
				yPath.append(node[0])			# load all the positions of Y in the list to plot
		plt.plot(xPath,yPath, 'r')				# Plot line red line


		#Plot the obstacle circles
		for circle in circleObstList:
			circle=plt.Circle((circle.column,circle.row),circle.radio,color='#FFA500')
			fig.gca().add_artist(circle)
			

		plt.show()	# Plot it
