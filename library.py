#!/usr/bin/env python

import numpy as np
import math
import matplotlib.pyplot as plt
from pylab import MultipleLocator

def getEuclideanDist(n1, n2):	# returns the euclidean distance between 2 nodes
	return math.sqrt(math.pow(n2[1]-n1[1],2) + math.pow(n2[0]-n1[0],2))

def listFromStrList(str):
	l = list(str)
	l = filter(lambda a: a != ' ', l)
	l = filter(lambda a: a != '[', l)
	l = filter(lambda a: a != ']', l)

	strl = ''.join(l)
	res = strl.split(',')

	coord = [int(res[0]),int(res[1])]

	return coord

def GraphKeyHeader(key):		# retrieves a graph Key = ['point1'|'point2'] and return point1, point2
	list = key.split('|')
	point1 = list[0]
	point2 = list[1]
	return listFromStrList(point1),listFromStrList(point2)

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


def WillItTouchCircle(point1, point2, circle,robotRadius):
	Ax = float(point1[1])					# Coordinates for point A
	Ay = float(point1[0])

	Bx = float(point2[1])					# Coordinates for point B
	By = float(point2[0])

	Cx = float(circle.x)				# Coordinates for circle center
	Cy = float(circle.y)
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

def RemovePathsThatHitObstacles(dictPath, circleList):		#Receive a dict of the shape {Key:[[path],cost]} and delete the paths that hit an obstacle circle
	newDictPath = dictPath
	keyList = newDictPath.keys()
	#print '\nCircle List = ', len(circleList)
	for pointTuple in keyList:
		#print '\nKeylist = ',newDictPath.keys()
		point1, point2 =  GraphKeyHeader(pointTuple)
		for circle in circleList:
			if point1 != point2 and WillItTouchCircle(point1,point2,circle,0):
				#print '\nis removing ...',point1,' - ', point2
				del(newDictPath[str(point1) + '|' + str(point2)])
				break
	return newDictPath