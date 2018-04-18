

#-1 == Small, 0 == Medium, 1 == Large
class Fuzzifier(object):
    # def __init__(self):
    #     x = 0
    def straightFuzzifier(self, straight):
        #Small
        if straight <= 5:
            scale = -1
            mu = 1
        elif 5 < straight and straight <= 20:
            scale = -1
            mu = (-1*straight/15 + 4/3)
        #Medium
        elif 20 < straight and straight <= 30:
            scale = 0
            mu = 0
        #Large
        elif 30 < straight:
            scale = 1
            mu = 1
        return scale, mu
    def rightFuzzifier(self, right):
        #Small
        if right <= 8:
            scale = -1
            mu = 1
        elif 8 < right and right <= 10:
            scale = -1
            mu = (-2*right/5 + 4.2)
        # Medium
        elif 10 < right and right <= 20:
            scale = 0
            mu = (-2*right/25 - 0.6)
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
        return scale, mu
    def leftFuzzifier(self, left):
        # Small
        if left <= 8:
            scale = -1
            mu = 1
        elif 8 < left and left <= 10:
            scale = -1
            mu = (-2 * left / 5 + 4.2)
        # Medium
        elif 10 < left and left <= 20:
            scale = 0
            mu = (-2 * left / 25 - 0.6)
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
        return scale, mu
class Defuzzifier(object):
    # def __init__(self):
    #     x = 0
    def straightFuzzifier(self, straight):
        x= 0
def fuzzy_System_Return_Angle(straight, right, left):
    fuzzifier = Fuzzifier()
    d1scale, d1mu = fuzzifier.straightFuzzifier(straight)
    d2scale, d2mu = fuzzifier.rightFuzzifier(right)
    d3scale, d3mu = fuzzifier.leftFuzzifier(left)

    steeringWheel = 10
    return steeringWheel