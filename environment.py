
###create environment with car, obstacle, and the destination###

import pygame
import math
import fuzzy_system
import lineIntersectPoint
import time
#Car object with draw the car and obstacleDistance
class Car(object):
    def __init__(self, x, y, degree, magnification, edge):
        self.x = x
        self.y = y
        #Coordinate angle
        self.degree = degree
        self.radius = 3 * magnification
        #steeringWheel moment angle
        self.steeringWheel = 10
        self.b = self.radius/4

        self.edge = edge
        self.detectRadius = 50 * magnification
        self.straight = 50 * magnification
        self.right = 50 * magnification
        self.left = 50 * magnification

    def draw(self, gameDisplay):
        self._carMove()

        pygame.draw.circle(gameDisplay, (255, 0, 0), (int(self.x), int(self.y)), self.radius)

        IntersectPointX, IntersectPointY = self._sensorDeal(self.degree)
        self.straight = self._obstacleDistance(IntersectPointX, IntersectPointY)
        pygame.draw.line(gameDisplay, (0, 255, 0), (self.x, self.y),
                         (IntersectPointX, IntersectPointY))

        IntersectPointX, IntersectPointY = self._sensorDeal(self.degree-45)
        self.right = self._obstacleDistance(IntersectPointX, IntersectPointY)
        pygame.draw.line(gameDisplay, (0, 255, 0), (self.x, self.y),
                         (IntersectPointX, IntersectPointY))

        IntersectPointX, IntersectPointY = self._sensorDeal(self.degree+45)
        self.left = self._obstacleDistance(IntersectPointX, IntersectPointY)
        pygame.draw.line(gameDisplay, (0, 255, 0), (self.x, self.y),
                         (IntersectPointX, IntersectPointY))

    def _sensorDeal(self, degree):
        pointx, pointy = self._setInitialLinePosition(degree)
        IntersectPointX, IntersectPointY = self._findIntersectPoint(pointx, pointy)
        return IntersectPointX, IntersectPointY

    def _obstacleDistance(self, IntersectPointX, IntersectPointY):
        distance = math.hypot(int(self.x) - IntersectPointX, int(self.y) - IntersectPointY)
        return distance

    def _setInitialLinePosition(self, degree):
        pointx = int(self.x) + self.detectRadius * math.cos(math.radians(degree))
        pointy = int(self.y) - self.detectRadius * math.sin(math.radians(degree))
        return pointx, pointy

    def _findIntersectPoint(self, pointx, pointy):
        IntersectPointX, IntersectPointY = 0, 0
        minDistance = self.detectRadius
        Line1p1 = (int(self.x), int(self.y))
        Line1p2 = (int(pointx), int(pointy))
        for i in range(len(self.edge)-1):
            Line2p1 = (self.edge[i, 0], self.edge[i, 1])
            Line2p2 = (self.edge[i+1, 0], self.edge[i+1, 1])
            IntersectPoint = lineIntersectPoint.calculateIntersectPoint(Line1p1, Line1p2, Line2p1, Line2p2)
            if IntersectPoint != None:
                distance = self._obstacleDistance(IntersectPoint[0], IntersectPoint[1])
                if distance < minDistance:
                    minDistance = distance
                    IntersectPointX, IntersectPointY = IntersectPoint[0], IntersectPoint[1]

        return IntersectPointX, IntersectPointY

    def _carMove(self):

        print(self.straight, self.right, self.left, self.degree)
        # print(self.degree, self.steeringWheel)
        #reset steeringWheel by fuzzy system
        steeringWheel = fuzzy_system.fuzzy_System_Return_Angle(self.straight, self.right, self.left)
        self._setSteeringWheelAngle(steeringWheel)
        # x = math.radians(180)
        # x = math.cos(math.pi/2)
        time.sleep(0.1)
        self.x = self.x + math.cos(math.radians(self.degree + self.steeringWheel)) +\
                 math.sin(math.radians(self.degree)) * math.sin(math.radians(self.steeringWheel))
        self.y = self.y - (math.sin(math.radians(self.degree + self.steeringWheel)) + \
                 math.sin(math.radians(self.steeringWheel)) * math.cos(math.radians(self.degree)))/3

        self.degree = self.degree - math.asin(2*math.sin(math.radians(self.steeringWheel))/self.b)
        # if -90 < temp and temp < 270:
        #     self.degree = temp

    def _setSteeringWheelAngle(self, steeringWheel):
        if steeringWheel > 40:
            steeringWheel = 40
        elif steeringWheel < -40:
            steeringWheel = -40
        self.steeringWheel = steeringWheel
    
#The end of the car have to arrive
class Destination(object):
    def __init__(self, positionx, positiony, rangex, rangey):
        self.positionx = positionx
        self.positiony = positiony
        self.rangex = rangex
        self.rangey = rangey
    def draw(self, gameDisplay):
        pygame.draw.rect(gameDisplay, (0, 0, 0), [self.positionx, self.positiony, self.rangex, self.rangey])

#Draw the wall
class Edge(object):
    def __init__(self, edge):
        self.edge = edge

    def draw(self, gameDisplay):
        for i in range(len(self.edge)-1):
            pygame.draw.line(gameDisplay, (0, 0, 255), (self.edge[i,0], self.edge[i,1]), (self.edge[i+1,0], self.edge[i+1,1]))


