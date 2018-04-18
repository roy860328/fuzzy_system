from __future__ import division
import pygame
import math
import fuzzy_system


class Car(object):
    def __init__(self, x, y, degree, magnification, edge):
        self.x = x
        self.y = y
        self.degree = degree
        self.radius = 3 * magnification
        self.steeringWheel = 10
        self.b = 2 * self.radius

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
            IntersectPoint = calculateIntersectPoint(Line1p1, Line1p2, Line2p1, Line2p2)
            if IntersectPoint != None:
                distance = self._obstacleDistance(IntersectPoint[0], IntersectPoint[1])
                if distance < minDistance:
                    minDistance = distance
                    IntersectPointX, IntersectPointY = IntersectPoint[0], IntersectPoint[1]

        return IntersectPointX, IntersectPointY

    def _carMove(self):

        # steeringWheel = fuzzy_system.sss(self.straight, self.right, self.left)
        self._setSteeringWheelAngle(steeringWheel)
        
        self.x = self.x + math.cos(math.radians(self.degree) + math.radians(self.steeringWheel)) +\
                 math.sin(math.radians(self.degree)) * math.sin(math.radians(self.steeringWheel))
        self.y = self.y - math.cos(math.radians(self.degree) + math.radians(self.steeringWheel)) - \
                 math.sin(math.radians(self.degree)) * math.sin(math.radians(self.steeringWheel))

        temp = self.degree - math.asin(2*math.sin(math.radians(self.steeringWheel))/self.b)
        if temp > -90 and temp < 270:
            self.degree = temp

    def _setSteeringWheelAngle(self, steeringWheel):
        self.steeringWheel = steeringWheel
    

class Destination(object):
    def __init__(self, positionx, positiony, rangex, rangey):
        self.positionx = positionx
        self.positiony = positiony
        self.rangex = rangex
        self.rangey = rangey
    def draw(self, gameDisplay):
        pygame.draw.rect(gameDisplay, (0, 0, 0), [self.positionx, self.positiony, self.rangex, self.rangey])


class Edge(object):
    def __init__(self, edge):
        self.edge = edge

    def draw(self, gameDisplay):
        for i in range(len(self.edge)-1):
            pygame.draw.line(gameDisplay, (0, 0, 255), (self.edge[i,0], self.edge[i,1]), (self.edge[i+1,0], self.edge[i+1,1]))



# Calc the gradient 'm' of a line between p1 and p2
def calculateGradient(p1, p2):
    # Ensure that the line is not vertical
    if (p1[0] != p2[0]):
        m = (p1[1] - p2[1]) / (p1[0] - p2[0])
        return m
    else:
        return None


# Calc the point 'b' where line crosses the Y axis
def calculateYAxisIntersect(p, m):
    return p[1] - (m * p[0])


# Calc the point where two infinitely long lines (p1 to p2 and p3 to p4) intersect.
# Handle parallel lines and vertical lines (the later has infinate 'm').
# Returns a point tuple of points like this ((x,y),...)  or None
# In non parallel cases the tuple will contain just one point.
# For parallel lines that lay on top of one another the tuple will contain
# all four points of the two lines
def getIntersectPoint(p1, p2, p3, p4):
    m1 = calculateGradient(p1, p2)
    m2 = calculateGradient(p3, p4)

    # See if the the lines are parallel
    if (m1 != m2):
        # Not parallel

        # See if either line is vertical
        if (m1 is not None and m2 is not None):
            # Neither line vertical
            b1 = calculateYAxisIntersect(p1, m1)
            b2 = calculateYAxisIntersect(p3, m2)
            x = (b2 - b1) / (m1 - m2)
            y = (m1 * x) + b1
        else:
            # Line 1 is vertical so use line 2's values
            if (m1 is None):
                b2 = calculateYAxisIntersect(p3, m2)
                x = p1[0]
                y = (m2 * x) + b2
            # Line 2 is vertical so use line 1's values
            elif (m2 is None):
                b1 = calculateYAxisIntersect(p1, m1)
                x = p3[0]
                y = (m1 * x) + b1
            else:
                assert False

        return ((x, y),)
    else:
        # Parallel lines with same 'b' value must be the same line so they intersect
        # everywhere in this case we return the start and end points of both lines
        # the calculateIntersectPoint method will sort out which of these points
        # lays on both line segments
        b1, b2 = None, None  # vertical lines have no b value
        if m1 is not None:
            b1 = calculateYAxisIntersect(p1, m1)

        if m2 is not None:
            b2 = calculateYAxisIntersect(p3, m2)

        # If these parallel lines lay on one another
        if b1 == b2:
            return p1, p2, p3, p4
        else:
            return None


# For line segments (ie not infinitely long lines) the intersect point
# may not lay on both lines.
#
# If the point where two lines intersect is inside both line's bounding
# pygame.Rectangles then the lines intersect. Returns intersect point if the line
# intesect o None if not
def calculateIntersectPoint(p1, p2, p3, p4):
    p = getIntersectPoint(p1, p2, p3, p4)

    if p is not None:
        width = p2[0] - p1[0]
        height = p2[1] - p1[1]
        r1 = pygame.Rect(p1, (width, height))
        r1.normalize()

        width = p4[0] - p3[0]
        height = p4[1] - p3[1]
        r2 = pygame.Rect(p3, (width, height))
        r2.normalize()

        # Ensure both pygame.Rects have a width and height of at least 'tolerance' else the
        # collidepoint check of the pygame.Rect class will fail as it doesn't include the bottom
        # and right hand side 'pixels' of the pygame.Rectangle
        tolerance = 1
        if r1.width < tolerance:
            r1.width = tolerance

        if r1.height < tolerance:
            r1.height = tolerance

        if r2.width < tolerance:
            r2.width = tolerance

        if r2.height < tolerance:
            r2.height = tolerance

        for point in p:
            try:
                res1 = r1.collidepoint(point)
                res2 = r2.collidepoint(point)
                if res1 and res2:
                    point = [int(pp) for pp in point]
                    return point
            except:
                # sometimes the value in a point are too large for PyGame's pygame.Rect class
                str = "point was invalid  ", point
                print(str)

        # This is the case where the infinately long lines crossed but
        # the line segments didn't
        return None

    else:
        return None