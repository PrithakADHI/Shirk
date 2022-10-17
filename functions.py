import pygame

from classes import *

screen = pygame.display.get_surface()

def displayText(txt, x, y, font_size=24, color=(0, 0, 0)):
    font = pygame.font.Font('assets/Fonts/QUIRKYSPRING Regular.ttf', font_size)
    text = font.render(txt, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)

    screen.blit(text, textRect)
    return textRect


def make_map(fileName):
    global walls
    global level
    with open(fileName) as f:
        # w, h = [int(x) for x in next(f).split()]
        array = [[x for x in line.split()] for line in f]
        for x in array:
            if x[0] == 'NextLvl':
                nxtLvl.append(nextLevel(int(x[1]), int(x[2]), x[3], x[4], x[5]))
            elif x[0] == "Initial":
                P.hitbox.x = int(x[1])
                P.hitbox.y = int(x[2])
                offset[0] = 0
                offset[1] = 0
            elif x[0] == "Level":
                level = x[1]
            elif x[0] == "endLvl":
                endLvl.append(endLevel(int(x[1]), int(x[2])))
            else:
                walls.append(Object(int(x[0]), int(x[1]), int(x[2]), int(x[3]), int(x[4])))


def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


def is_colliding(x, y, x1, y1, w, h):
    if x >= x1 and y >= y1 and x <= x1 + w and y <= y1 + h:
        return True


def game_over():
    global level
    screen.fill((255, 255, 255))
    displayText("GAME OVER!!!!", width // 2, height // 2, 32)

    pygame.display.update()
    time.sleep(1)
    level = "Menu"


def make_mana_balls(filename):
    if os.path.isfile(filename):
        with open(filename) as f:
            # w, h = [int(x) for x in next(f).split()]
            array = [[int(x) for x in line.split()] for line in f]
        for x in array:
            mana_list.append(manaInc(x[0], x[1]))


def make_enemies(filename):
    if os.path.isfile(filename):
        with open(filename) as f:
            # w, h = [int(x) for x in next(f).split()]
            array = [[int(x) for x in line.split()] for line in f]
        for x in array:
            E_List.append(Enemy1(x[0], x[1]))


def tutorial_level():
    global level
    make_map("Tutorial/map.mp")
    make_mana_balls("Tutorial/Tutorial_Mana_List.mp")
    make_enemies("Tutorial/Tutorial_Enemy_List.mp")

    level = "Tutorial"


def Level1():
    global level
    make_map("Level1/map1.mp")
    make_mana_balls("Level1/mana_list1.mp")
    make_enemies("Level1/enemy_list1.mp")
    P.mana = 0
    level = "Chapter 1"

def testLevel():
    global level
    make_map("Level1/map4.mp")
    make_mana_balls("mana_list.mp")

    level = "Test"

def clickableBox(text, x, y, font_size, color):
    mx, my = pygame.mouse.get_pos()
    mb = pygame.mouse.get_pressed()
    rect = displayText(text, x, y, font_size, color)

    if is_colliding(mx, my, rect.x - 10, rect.y - 5, rect.w + 20, rect.h + 5):
        rect = displayText(text, x, y, font_size, (55, 119, 255))
        pygame.draw.rect(screen, (55, 119, 255), (rect.x - 10, rect.y - 5, rect.w + 20, rect.h + 5), 5, 10)
    else:
        rect = displayText(text, x, y, font_size, color)
        pygame.draw.rect(screen, color, (rect.x - 10, rect.y - 5, rect.w + 20, rect.h + 5), 5, 10)

    if is_colliding(mx, my, rect.x - 10, rect.y - 5, rect.w + 20, rect.h + 5) and mb[0]:
        return True


def menu():
    """
    displayText("MrMagno", 1100, 200, 32, (200,200,200))
    displayText("Play", 1100, 200+100, 20, (200,200,200))

    pygame.draw.rect(screen, (255,255,255), (1100-30, 300-20, 60, 40), 2)

    if is_colliding(mx, my, 1100-30, 300-20, 60, 40) and mb[0]:
        #tutorial_level()
        #make_map("map.mp")
        #level = "1"
        Level1()
    """

    global walls, E_List, mana_list, menuRunning, level, nxtLvl, endLvl

    walls = []
    E_List = []
    mana_list = []
    nxtLvl = []
    endLvl = []
    P.mana = 0
    screen.fill((255, 255, 255))
    displayText("Shirk", width // 2, height // 2 - 200, 56, (200, 85, 61))

    if clickableBox("Play", width // 2, height // 2, 32, (88, 139, 139)):
        transition()
        menuRunning = True

    pygame.display.flip()


def transition():
    pass


def levelMenu():
    global menuRunning
    screen.fill((255, 255, 255))
    if clickableBox("Chapter 1", 150, 100, 32, (192, 155, 216)):
        Level1()
        menuRunning = False

    if clickableBox("Chapter 2", 150, 300, 32, (192, 155, 216)):
        pass

    displayText("Chapter Selection", 900, 100, 32, (232, 63, 111))
    displayText("Shirk", 900, 75, color=(232, 63, 111))

    if clickableBox("Tutorial", 900, 200, 32, (192, 155, 216)):
        tutorial_level()
        menuRunning = False

    if clickableBox("Tests", 900, 600, 32, (192, 155, 216)):
        testLevel()
        menuRunning = False

    if clickableBox("Chapter 3", 150, 500, 32, (192, 155, 216)):
        pass

    if clickableBox("Chapter 4", 150, 700, 32, (192, 155, 216)):
        pass
    pygame.display.flip()
