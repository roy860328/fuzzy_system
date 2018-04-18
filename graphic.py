import pygame
import os
import numpy as np
import environment

global centerx, centery, magnification
centerx = 400
centery = 300
magnification = 2

def mainGraphic():
    global centerx, centery, magnification
    carcenter, destination, edge = readFile("case01.txt")

    destination = destination*magnification
    destination = environment.Destination(centerx+destination[0], centery-destination[1], (destination[2]-destination[0]), (destination[3]-destination[1]))

    edge = (1, -1)*edge*magnification + (centerx, centery)
    car = environment.Car(centerx + carcenter[0], centery + carcenter[1], carcenter[2], magnification, edge)
    edge = environment.Edge(edge)

    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    gameExit = False

    pygame.init()
    gameDisplay = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
        pygame.display.update()
        gameDisplay.fill((255, 255, 255))

        destination.draw(gameDisplay)
        car.draw(gameDisplay)
        edge.draw(gameDisplay)
        pygame.draw.line(gameDisplay, (0, 0, 255), (0, 0), (200, 100))

        clock.tick(30)
    pygame.quit()
    quit()

def readFile(file):
    try:
        string = ""
        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        rel_path = file
        print(script_dir, rel_path)
        abs_file_path = os.path.join(script_dir, rel_path)
        pfile1 = open(abs_file_path, "r")
        string = pfile1.read()
        string = string.split('\n')
        # string to double list
        string = [i.split(',') for i in string]
        string = [x for x in string if x != ['']]

        carcenter = string[0]
        destination = string[1] + string[2]
        edge = string[3:]
    except Exception as e:
        print(e)

    return np.array(carcenter, dtype=int), \
           np.array(destination, dtype=int), \
           np.array(edge, dtype=int)

mainGraphic()