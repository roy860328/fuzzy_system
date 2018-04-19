

#-1 == Small, 0 == Medium, 1 == Large
class Fuzzifier(object):
    def __init__(self):
        self.d1scale, self.d1mu = 0, 0
        self.d2scale, self.d2mu = 0, 0
        self.d3scale, self.d3mu = 0, 0
    def run(self, straight, right, left):
        self.straightFuzzifier(straight)
        self.rightFuzzifier(right)
        self.leftFuzzifier(left)
        steeringWheel = self.defuzzifier()
        return steeringWheel
    def straightFuzzifier(self, straight):
        #Small
        if straight <= 5:
            scale = -1
            mu = 1
        elif 5 < straight and straight <= 15:
            scale = -1
            mu = (-1*straight/15 + 4/3)
        #Medium
        elif 15 < straight and straight <= 25:
            scale = 0
            mu = 0
        #Large
        elif 25 < straight:
            scale = 1
            mu = 1
        self.d1scale, self.d1mu = scale, mu
    def rightFuzzifier(self, right):
        #Small
        if right <= 10:
            scale = -1
            mu = 1
        elif 10 < right and right <= 12:
            scale = -1
            mu = (-2*right/5 + 4.2)
        # Medium
        elif 12 < right and right <= 20:
            scale = 0
            mu = (2*right/25 - 0.6)
        elif 20 < right and right <= 24:
            scale = 0
            mu = (-1*right/8 + 7/2)
        #Large
        elif 24 < right and right <= 32:
            scale = 1
            mu = (1*right/16 - 1)
        elif 30 < right:
            scale = 1
            mu = 1
        self.d2scale, self.d2mu = scale, mu
    def leftFuzzifier(self, left):
        # Small
        if left <= 10:
            scale = -1
            mu = 1
        elif 10 < left and left <= 12:
            scale = -1
            mu = (-2 * left / 5 + 4.2)
        # Medium
        elif 12 < left and left <= 20:
            scale = 0
            mu = (2 * left / 25 - 0.6)
        elif 20 < left and left <= 24:
            scale = 0
            mu = (-1 * left / 8 + 7 / 2)
        # Large
        elif 24 < left and left <= 32:
            scale = 1
            mu = (1 * left / 16 - 1)
        elif 30 < left:
            scale = 1
            mu = 1
        self.d3scale, self.d3mu = scale, mu
    def defuzzifier(self):
        #left large distance
        if self.d3scale == 1:
            steeringWheel = -1*self.d3mu*50
        #right large distance
        elif self.d2scale == 1:
            steeringWheel = 1*self.d2mu*50
        #left medium distance
        elif self.d3scale == 0:
            steeringWheel = -1*self.d3mu*5 - 40
        #right medium distance
        elif self.d2scale == 0:
            steeringWheel = 1*self.d2mu*5 + 40
        #straight large or medium distance and left small distance
        elif (self.d1scale == 1 or self.d1scale == 0) and self.d3scale == -1:
            if self.d1mu == 1:
                steeringWheel = 10
            else:
                steeringWheel = -1*self.d1mu*20 + 40
        # straight large or medium distance and right small distance
        elif (self.d1scale == 1 or self.d1scale == 0) and self.d2scale == -1:
            if self.d1mu == 1:
                steeringWheel = -10
            else:
                steeringWheel = 1*self.d1mu*20 - 40
        return steeringWheel
def fuzzy_System_Return_Angle(straight, right, left):
    fuzzifier = Fuzzifier()
    steeringWheel = fuzzifier.run(straight, right, left)

    # print(steeringWheel)
    # steeringWheel = -7
    return steeringWheel