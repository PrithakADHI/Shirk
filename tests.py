import pygame, sys
from pygame.locals import *
import easing_functions

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

easingFunction = easing_functions.CubicEaseInOut()

buttonStartPos = 0
buttonEndPos = 380

frame = 0

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.fill((0, 0, 0))

    easingAmount = easingFunction(frame * 0.01)
    easingAmount = min(1, easingAmount)
    buttonCurrentPos = (buttonEndPos - buttonStartPos) * easingAmount
    pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (buttonCurrentPos, 100, 20, 20))

    frame += 1
    pygame.display.update()

    clock.tick(60)