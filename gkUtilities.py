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


def plotRoadMap(rows, columns, listOfNodes,circleObstList,graph):

		plt.axis([0,columns-1,rows-1,0])

		fig = plt.gcf()

		toPlot = plt.subplot(111)

		toPlot.xaxis.set_major_locator(MultipleLocator(columns/20))	# Set grid interval for axis X
		toPlot.yaxis.set_major_locator(MultipleLocator(rows/20))	# Set grid interval for axis Y

		toPlot.xaxis.grid(True,'major',linewidth=1)			# Plot grids
		toPlot.yaxis.grid(True,'major',linewidth=1)


		for node in listOfNodes:
			xPath = []
			yPath = []
			xPath.append(node[1])		# load all the positions of X in the list to plot
			yPath.append(node[0])		# load all the positions of Y in the list to plot
			#plt.plot(xPath,yPath)				# Plot line blue line
			plt.plot(xPath, yPath, 'ro', label='Positions')	# Plot red dots


		# Plot the edges between nodes
		if graph != None:
			for i in range(len(listOfNodes)):
				for j in range(len(listOfNodes)):
					if graph[i][j] > 0:
						xPath = []
						yPath = []
						xPath = [listOfNodes[i][1],listOfNodes[j][1]]	# load all the positions of X in the list to plot
						yPath = [listOfNodes[i][0],listOfNodes[j][0]]	# load all the positions of Y in the list to plot
						plt.plot(xPath,yPath, 'b')								# Plot line blue line


		#Plot the obstacle circles
		for circle in circleObstList:
			circle=plt.Circle((circle.column,circle.row),circle.radio,color='#FFA500')
			fig.gca().add_artist(circle)
			

		plt.show()	# Plot it


def WillItTouchCircle(point1, point2, circle):
	# compute the euclidean distance between A and B

	Ax = point1[1]
	Ay = point1[0]

	Bx = point2[1]
	By = point2[0]

	Cx = circle.column
	Cy = circle.row
	R = circle.radio 

	print '\nAx=',Ax,' | Ay=',Ay
	print '\nBx=',Bx,' | By=',By
	LAB = math.sqrt(math.pow(Bx-Ax,2)+ math.pow(By-Ay,2))

	# compute the direction vector D from A to B
	Dx = (Bx-Ax)/LAB
	Dy = (By-Ay)/LAB

	# Now the line equation is x = Dx*t + Ax, y = Dy*t + Ay with 0 <= t <= 1.

	# compute the value t of the closest point to the circle center (Cx, Cy)
	t = Dx*(Cx-Ax) + Dy*(Cy-Ay)    

	# This is the projection of C on the line from A to B.

	# compute the coordinates of the point E on line and closest to C
	Ex = t*Dx+Ax
	Ey = t*Dy+Ay

	# compute the euclidean distance from E to C
	LEC = math.sqrt( math.pow(Ex-Cx,2)+ math.pow(Ey-Cy,2))

	# test if the line intersects the circle
	if LEC < R:
		print '\nTouch the circle.'
		return True
	# else test if the line is tangent to circle
	elif LEC == R:
		print '\nTouch the circle.'
		return True
	else:
		print '\nDont Touch the circle.'
		return False

def RemovePathsThatHitObstacles(dictPath, circleList):		#Receive a dict of the shape {Key:[[path],cost]} and delete the paths that hit an obstacle circle
	newDictPath = dictPath
	keyList = newDictPath.keys()
	#print '\nCircle List = ', len(circleList)
	for pointTuple in keyList:
		#print '\nKeylist = ',newDictPath.keys()
		point1, point2 =  GraphKeyHeader(pointTuple)
		for circle in circleList:
			if point1 != point2 and WillItTouchCircle(point1,point2,circle):
				#print '\nis removing ...',point1,' - ', point2
				del(newDictPath[str(point1) + '|' + str(point2)])
				break
	return newDictPath