import pygame, time, sys, random, math, os.path, easing_functions

pygame.init()
width = 1280
height = 800
screen = pygame.display.set_mode((width, height), vsync=True)
clock = pygame.time.Clock()

offset = [0, 0]

isGrounded = False
headBump = False

pygame.display.set_caption("Shirk")

prev_time = time.time()
dt = 0

running = True

story_running = True

textAnim_flag = True

class Animate():
    def __init__(self, start_pos, end_pos, easing_function):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.easing_function = easing_function
        self.frame = 0

    def start(self):
        easingAmount = self.easing_function(self.frame * 0.01)
        easingAmount = min(1, easingAmount)
        current_pos = (self.end_pos - self.start_pos) * easingAmount
        # pygame.draw.rect(screen, (255, 0, 0), (current_pos, 100, 20, 20))

        self.frame += 1

        return self.start_pos + current_pos

class StoryDumps():
    def __init__(self, text_array):
        self.text_array = text_array
        self.active = True
        self.end_1 = 720 // 2 - 100
        self.box_1 = Animate(720 + 200, self.end_1, easing_functions.CubicEaseInOut())
        self.box_2 = Animate(1, 500, easing_functions.CubicEaseInOut())
        self.box_3 = Animate(1280//2, 1280//2 - (500//2), easing_functions.CubicEaseInOut())
        self.starting_animation_finished = False
        self.color_change = True
        self.r = 255
        self.g = 255
        self.b = 255


    def start_animation(self):
        global story_running
        if not self.color_change:
            box1_y = self.box_1.start()

            if box1_y == self.end_1:
                box2_w = self.box_2.start()
                box3_x = self.box_3.start()
                pygame.draw.rect(screen, (255, 255, 255), (box3_x, box1_y, box2_w, 200), 4)

                if box2_w == 500:
                    self.starting_animation_finished = True

            else:
                pygame.draw.rect(screen, (255, 255, 255), (1280 // 2, box1_y, 1, 200), 4)

    def start(self):
        k = pygame.key.get_pressed()

        if k[pygame.K_q]:
            self.active = False

        if self.active:
            if self.color_change:
                self.r -= 3
                self.g -= 3
                self.b -= 3

                if self.r < 0 and self.g < 0 and self.b < 0:
                    self.color_change = False
                    self.r, self.b, self.g = 0, 0, 0

                screen.fill((self.r, self.g, self.b))

            if not self.color_change:
                if not self.starting_animation_finished:
                    screen.fill((0, 0, 0))
                    self.start_animation()
                else:
                    screen.fill((0, 0, 0))
                    pygame.draw.rect(screen, (255, 255, 255), (1280//2 - (500//2), self.end_1, 500, 200), 4)
                    textAnimation(self.text_array[0], 1280//2, 720//2, color=(255, 255, 255), font_size=20)


class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 50
        self.h = 50

        self.speedx = 300
        self.speedy = 350

        self.oghealth = 200
        self.health = 200

        self.mana = 0
        self.ogmana = 300

        self.health_img = pygame.image.load("assets/player/healthbar_img.png")
        # self.img = pygame.image.load("assets/player/1.png")
        self.imgarr = [pygame.image.load("assets/player/1.png").convert_alpha(),
                       pygame.image.load("assets/player/2.png").convert_alpha(),
                       pygame.image.load("assets/player/3.png").convert_alpha(),
                       pygame.image.load("assets/player/4.png").convert_alpha(),
                       pygame.image.load("assets/player/5.png").convert_alpha(),
                       pygame.image.load("assets/player/6.png").convert_alpha(),
                       pygame.image.load("assets/player/7.png").convert_alpha(),
                       pygame.image.load("assets/player/8.png").convert_alpha()]

        self.hitbox = pygame.Rect(self.x + 13, self.y, self.w - 27, self.h)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        self.x_change = 0
        self.accel_x = 0
        self.max_speed = 350
        self.change = 30
        self.y_change = 0
        self.accel_y = 0
        self.dx = 0
        self.dy = 0

    def render(self, ori, no):
        img = pygame.transform.scale(self.imgarr[no], (self.w, self.h))
        if ori == "Left":
            img = pygame.transform.flip(img, True, False)

        # pygame.draw.rect(screen, (255,200,100), (offset[0] + self.hitbox.x, offset[1] + self.hitbox.y, self.hitbox.w, self.hitbox.h), 1)

        screen.blit(img, (offset[0] + self.hitbox.x - 13, offset[1] + self.hitbox.y, self.hitbox.w, self.hitbox.h))

    def render_health_bar(self):
        img = pygame.transform.scale(self.health_img, (100, 100))
        screen.blit(img, (25, 50))

        per = (self.health / self.oghealth) * 100

        # pygame.draw.rect(screen, (255,255,255), (100, 87, 100, 15))
        # pygame.draw.rect(screen, (255,100,140), (100, 87, per, 15))

        per2 = (self.mana / self.ogmana) * 100

        pygame.draw.rect(screen, (255, 255, 255), (100, 97, 100, 15))
        pygame.draw.rect(screen, (100, 200, 255), (100, 97, per2, 15))

    def move(self, dx, dy, colliders):
        # self.move_single_axis(dx, 0, colliders)
        # self.move_single_axis(0, dy, colliders)
        k = pygame.key.get_pressed()

        if k[pygame.K_a]:
            self.accel_x = -self.change
            self.dx = -1

        elif k[pygame.K_d]:
            self.accel_x = self.change
            self.dx = 1

        self.x_change += self.accel_x
        self.y_change += self.accel_y
        if abs(self.x_change) >= self.max_speed:
            self.x_change = self.x_change / abs(self.x_change) * self.max_speed

        if abs(self.y_change) >= self.max_speed:
            self.y_change = self.y_change / abs(self.y_change) * self.max_speed

        if self.accel_x == 0:
            if self.x_change > 0:
                self.x_change -= self.change
                if self.x_change < self.change:
                    self.x_change = 0
            elif self.x_change < 0:
                self.x_change += self.change
                if self.x_change > -self.change:
                    self.x_change = 0

        if self.accel_y == 0:
            if self.y_change > 0:
                self.y_change -= self.change
                if self.y_change < self.change:
                    self.y_change = 0
            elif self.y_change < 0:
                self.y_change += self.change
                if self.y_change > -self.change:
                    self.y_change = 0

        self.move_single_axis(self.x_change * dt, 0, colliders)
        self.move_single_axis(0, dy, colliders)

        if k not in (pygame.K_a, pygame.K_d):
            self.accel_x = 0
            self.dx = 0

        if k not in (pygame.K_w, pygame.K_s):
            self.accel_y = 0
            self.dy = 0

    def move_single_axis(self, dx, dy, colliders):

        self.hitbox.x += dx
        self.hitbox.y += dy

        global isGrounded
        global headBump

        for wall in colliders:
            if self.hitbox.colliderect(wall.rect):
                if dx > 0:
                    # self.rect.right = wall.rect.left
                    self.hitbox.right = wall.rect.left
                if dx < 0:
                    # self.rect.left = wall.rect.right
                    self.hitbox.left = wall.rect.right

                if dy > 0:
                    # self.rect.bottom = wall.rect.top
                    self.hitbox.bottom = wall.rect.top
                    isGrounded = True
                else:
                    isGrounded = False
                if dy < 0:
                    # self.rect.top = wall.rect.bottom
                    headBump = True
                    self.hitbox.top = wall.rect.bottom
                else:
                    headBump = False


class Object(object):
    def __init__(self, x, y, w, h, no):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.img = pygame.image.load("assets/blocks/" + str(no).strip() + ".png").convert_alpha()

    def render(self):
        # Just for testingt
        # pygame.draw.rect(screen, (100,200,255), self.rect, 0)
        img = pygame.transform.scale(self.img, (self.w, self.h))
        if is_colliding(offset[0] + self.rect.x - 100, offset[1] + self.rect.y + 25, -125, 0, 1280, 800):
            screen.blit(img, (offset[0] + self.rect.x, offset[1] + self.rect.y, self.rect.w, self.rect.h))


class Enemy1(object):
    def __init__(self, x, y):
        self.hitbox = pygame.Rect(x, y, 22, 40)
        self.speedx = 300
        self.speedy = 400
        self.img_array = [pygame.image.load("assets/enemies/e11.png").convert_alpha()]
        self.dir = "Right"

    def render(self):
        # Just for testing
        # pygame.draw.rect(screen, (255,100,100), (offset[0] + self.hitbox.x, offset[1] + self.hitbox.y, self.hitbox.w, self.hitbox.h), 3 )
        img = pygame.transform.scale(self.img_array[0], (50, 50))
        if self.dir == "Left":
            img = pygame.transform.flip(img, True, False)
        screen.blit(img, (offset[0] + self.hitbox.x - 18, offset[1] + self.hitbox.y - 10))

    def move(self, dx, dy, colliders, dt):
        self.move_single_axis(dx, 0, colliders, dt)
        self.move_single_axis(0, dy, colliders, dt)

    def move_single_axis(self, dx, dy, colliders, dt):

        self.hitbox.x += dx * dt
        self.hitbox.y += dy * dt

        if dx > 0:
            self.dir = "Right"
        if dx < 0:
            self.dir = "Left"

        for wall in colliders:
            if self.hitbox.colliderect(wall.rect):
                if dx > 0:
                    # self.rect.right = wall.rect.left
                    self.hitbox.right = wall.rect.left
                if dx < 0:
                    # self.rect.left = wall.rect.right
                    self.hitbox.left = wall.rect.right

                if dy > 0:
                    # self.rect.bottom = wall.rect.top
                    self.hitbox.bottom = wall.rect.top
                if dy < 0:
                    # self.rect.top = wall.rect.bottom
                    self.hitbox.top = wall.rect.bottom

    def follow_player(self, player, dt):
        # pygame.draw.rect( screen, (255,100,100), (offset[0] + self.hitbox.x - 300, offset[1] + self.hitbox.y - 300, 600, 600), 1 )
        if player.hitbox.colliderect(pygame.Rect(self.hitbox.x - 300, self.hitbox.y - 300, 600, 600)):
            dx, dy = player.hitbox.x - self.hitbox.x, player.hitbox.y - self.hitbox.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx, dy = dx / dist, dy / dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.
            # self.rect.x += dx * self.speed
            # self.rect.y += dy * self.speed

            self.move(dx * self.speedx * 1.05, 0, walls, dt)

class Enemy2(object):
    def __init__(self, x, y):
        self.hitbox = pygame.Rect(x, y, 22, 40)
        self.speedx = 300
        self.speedy = 300
        self.mana_x = self.hitbox.x
        self.mana_y = self.hitbox.y
        self.img_array = [pygame.image.load("assets/enemies/e11.png").convert_alpha()] # Placeholder for now
        self.dir = "Right"

    def render(self):
        # Just for testing
        # pygame.draw.rect(screen, (255,100,100), (offset[0] + self.hitbox.x, offset[1] + self.hitbox.y, self.hitbox.w, self.hitbox.h), 3 )
        img = pygame.transform.scale(self.img_array[0], (50, 50))
        if self.dir == "Left":
            img = pygame.transform.flip(img, True, False)
        screen.blit(img, (offset[0] + self.hitbox.x - 18, offset[1] + self.hitbox.y - 10))
        # self.draw_mana(self.mana_x, self.mana_y)
        draw_circle_alpha(screen, (255, 255, 255, 200), (offset[0] + self.mana_x, offset[1] + self.mana_y), 15)
        pygame.draw.circle(screen, (255, 100, 100), (offset[0] + self.mana_x, offset[1] + self.mana_y), 10)

    def shoot(self, player, dt):
        dx, dy = 0, 0
        if player.hitbox.colliderect(pygame.Rect(self.hitbox.x - 300, self.hitbox.y - 300, 600, 600)):
            dx, dy = player.hitbox.x - self.hitbox.x, player.hitbox.y - self.hitbox.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx, dy = dx / dist, dy / dist

        self.mana_move(dx * self.speedx * 0.03, dy * self.speedy * 0.03)

    def mana_move(self, dx, dy):
        self.mana_x += dx
        self.mana_y += dy

        if offset[0] + self.mana_x < 0 and offset[1] + self.mana_y < 0:
            self.mana_x, self.mana_y = self.hitbox.x, self.hitbox.y


class particles():
    def __init__(self, pos, vel, timer, col):
        self.pos = pos
        self.vel = vel
        self.timer = timer
        self.col = col


class manaInc():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x - 5, self.y - 5, 10, 10)

    def render(self):
        draw_circle_alpha(screen, (255, 255, 255, 200), (offset[0] + self.x, offset[1] + self.y), 15)
        pygame.draw.circle(screen, (100, 200, 255), (offset[0] + self.x, offset[1] + self.y), 10)

    def collision(self, player):
        if self.rect.colliderect(player.hitbox):
            return True




class nextLevel():
    def __init__(self, x, y, mp, e_list, m_list):
        self.rect = pygame.Rect(x, y, 20, 30)
        self.mp = mp
        self.e_list = e_list
        self.m_list = m_list

    def loadLevel(self):
        global walls
        global E_List
        global mana_list
        global nxtLvl
        global endLvl

        walls = []
        E_List = []
        mana_list = []
        nxtLvl = []
        endLvl = []
        make_map(self.mp)
        make_mana_balls(self.m_list)
        make_enemies(self.e_list)

    def collision(self, player):
        if self.rect.colliderect(player.hitbox):
            transition()
            self.loadLevel()

    def render(self):
        pygame.draw.rect(screen, (78, 212, 114),
                         (offset[0] + self.rect.x, offset[1] + self.rect.y, self.rect.w, self.rect.h))


class endLevel():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 30)

    def collision(self, player):
        global level
        global endLvl
        global E_List
        global mana_list
        global menuRunning
        global walls

        if self.rect.colliderect(player.hitbox):
            screen.fill((255, 255, 255))
            displayText(f"{level} Completed!", 1280 // 2, 720 // 2, 54, (194, 187, 240))
            pygame.display.flip()
            time.sleep(1)
            menuRunning = True
            walls = []
            E_List = []
            mana_list = []
            level = "Menu"
            endLvl = []

    def render(self):
        pygame.draw.rect(screen, (194, 187, 240),
                         (offset[0] + self.rect.x, offset[1] + self.rect.y, self.rect.w, self.rect.h))


def displayText(txt, x, y, font_size=24, color=(0, 0, 0)):
    font = pygame.font.Font('assets/Fonts/QUIRKYSPRING Regular.ttf', font_size)
    text = font.render(txt, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)

    screen.blit(text, textRect)
    return textRect


def textAnimation(txt, x, y, font_size=24, color=(0,0,0)):
    global textAnim_flag
    if textAnim_flag:
        for t_x in txt:
            displayText(t_x, x, y, font_size, color)
            x += (font_size * 0.6)

            time.sleep(0.1)

            pygame.display.flip()
        textAnim_flag = False
    else:
        displayText(txt, x, y, font_size, color)

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


ori = "Left"
P = Player(0, 0)

E_List = []
e2 = Enemy2(500, 1000)
mana_list = []
text_list = []

vel = 5

walls = []
nxtLvl = []
endLvl = []

particle_array = []

background_objects = [[0.015, [1000, 530, 400, 1000]], [0.015, [480, 430, 400, 1000]], [0.025, [120, 100, 400, 900]],
                      [0.05, [30, 40, 400, 800]]]

jump = False
jump_i = 0

fly = False

no = 0

dx = 0
dy = 0

acc = 0
y_change = 0

tr = False

angle = 0
dJump = False

menuRunning = False
level = "Menu"

test = Animate(100, 500, easing_functions.CubicEaseInOut())

test_2 = StoryDumps(['Hello'])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump = True
                isGrounded = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if level != "Menu":
                mx, my = pygame.mouse.get_pos()
                if event.button == 1:
                    E_List.append( Enemy1(mx - offset[0], my - offset[1]) )
                    # pass
                    # mana_list.append( manaInc(mx - offset[0], my - offset[1]) )

    if level == "Menu" and not menuRunning:
        menu()

    if menuRunning:
        levelMenu()

    dy = 400 * dt
    edy = 600 * dt

    mx, my = pygame.mouse.get_pos()
    mb = pygame.mouse.get_pressed()

    if level != "Menu":
        for background_object in background_objects:
            obj_rect = pygame.Rect(background_object[1][0] + offset[0] * background_object[0],
                                   background_object[1][1] + offset[1] * background_object[0], background_object[1][2],
                                   background_object[1][3])
            if background_object[0] == 0.05:
                pygame.draw.rect(screen, (200, 200, 200), obj_rect)
            elif background_object[0] == 0.025:
                pygame.draw.rect(screen, (150, 150, 150), obj_rect)
            elif background_object[0] == 0.015:
                pygame.draw.rect(screen, (100, 100, 100), obj_rect)

    now = time.time()
    dt = now - prev_time
    prev_time = now

    k = pygame.key.get_pressed()
    if level != "Menu":
        if k[pygame.K_a] == False and k[pygame.K_d] == False:
            no = 0

        # if k[pygame.K_j]:
        #    P.mana = 300

        if k[pygame.K_w] and P.mana > 0:
            P.mana -= 50 * dt
            fly = True
            isGrounded = False
            dy = (P.speedy / 2 * -1) * dt
            particle_array.append(particles([P.hitbox.x + 10, P.hitbox.y + 50], [random.randint(0, 20) / 10 - 1, 5],
                                            random.randint(7, 10), [100, 200, 255]))


        if k[pygame.K_a]:
            ori = "Left"
            # dx = (P.speedx * -1) * dt
            if fly == False:
                no += 13 * dt
            if isGrounded:
                particle_array.append(
                    particles([P.hitbox.x + 10, P.hitbox.y + 50], [random.randint(0, 20) / 10 - 1, 0.25],
                              random.randint(2, 6), [128, 128, 128]))

        if k[pygame.K_d]:
            ori = "Right"
            # dx = P.speedx * dt
            if fly == False:
                no += 13 * dt
            if isGrounded:
                particle_array.append(
                    particles([P.hitbox.x + 10, P.hitbox.y + 50], [random.randint(0, 20) / 10 - 1, 0.25],
                              random.randint(2, 6), [128, 128, 128]))

    if k[pygame.K_ESCAPE]:
        f = open("enemy_list.mp", "w")
        for x in E_List:
            f.write( f"{x.hitbox.x} {x.hitbox.y}\n" )

        f.close()

        f = open("mana_list.mp", "w")
        for x in mana_list:
            f.write(f"{x.rect.x} {x.rect.y}\n")

        f.close()

        pygame.quit()
        sys.exit()

    if isGrounded == False:
        no = 1

    if isGrounded == True:
        fly = False

    if jump:
        jump_i += 60 * dt
        accel = 0.13
        # vel = 0

        if headBump:
            jump_i = 0
            jump = False
            vel = 5

        if not fly:
            if jump_i <= 17:
                # ease = easeClass.start()
                vel -= accel
                dy = ((P.speedy * -1) * dt * (vel * .5)) * .75

            if jump_i >= 17:
                vel += accel
                dy = ((P.speedy) * dt * (vel * .5)) * .75

        if jump_i >= (10 + 10):
            jump_i = 0
            jump = False
            dJump = False
            vel = 5

    if P.hitbox.x >= 1280:
        offset[0] -= 1000 * dt

    if P.hitbox.x < 1280:
        offset[0] += 1000 * dt

    if P.hitbox.y <= 450:
        offset[1] += 1000 * dt

    if P.hitbox.y >= 450:
        offset[1] -= 1000 * dt

    if offset[0] <= -100 * 12.82:
        offset[0] = -100 * 12.82

    if offset[0] >= 0:
        offset[0] = 0

    if offset[1] <= -40 * (450 / 40):
        offset[1] = -40 * (450 / 40)

    if offset[1] >= 0:
        offset[1] = 0

    if P.hitbox.y < 0:
        P.hitbox.y = 0
        headBump = True
    else:
        headBump = False

    if no > 6:
        no = 0

    m_no = round(no)

    if P.hitbox.x < 0:
        P.hitbox.x = 0

    if P.hitbox.x > 2540:
        P.hitbox.x = 2540

    # if P.hitbox.y > 1200:
    #    P.hitbox.y = 500

    if level != "Menu":
        for E in E_List:
            E.render()
            E.follow_player(P, dt)
            E.move(0, E.speedy, walls, dt)

            if E.hitbox.y > 1200:
                E_List.remove(E)

            if E.hitbox.colliderect(P.hitbox):
                game_over()

        e2.render()
        e2.shoot(P, dt)

        for E1 in E_List:
            for E2 in E_List:
                if E1 != E2:
                    if E1.hitbox.colliderect(E2.hitbox):
                        E_List.remove(E1)
                        E_List.remove(E2)

        for mana_incs in mana_list:
            mana_incs.render()
            if mana_incs.collision(P):
                P.mana = 300
                mana_list.remove(mana_incs)

        for texts in text_list:
            texts.render()

        faceMouse = False

        for particle in particle_array:
            particle.pos[0] += particle.vel[0]
            particle.pos[1] += particle.vel[1]
            particle.timer -= (1 / 20)

            draw_circle_alpha(screen, (particle.col[0], particle.col[1], particle.col[2], 100),
                              (offset[0] + particle.pos[0], offset[1] + particle.pos[1]), particle.timer * 2)
            pygame.draw.circle(screen, (255, 255, 255), (offset[0] + particle.pos[0], offset[1] + particle.pos[1]),
                               particle.timer)

            if particle.timer <= 0:
                particle_array.remove(particle)

        for wall in walls:
            wall.render()

        for nxt in nxtLvl:
            nxt.render()
            nxt.collision(P)

        for end in endLvl:
            end.render()
            end.collision(P)

        if level == "Tutorial":
            displayText("Use AS to Move and Space to Jump", 650, 50, 16)
            displayText("Use W to fly, it requires mana, get those by bumping into those blue balls", 650, 50 + 32, 16)
            displayText("Avoid the other robots, you can't kill them so run for your life :)", 650, 50 + 32 + 32, 16)
            displayText("Reach the green/purple boxes to end the part/level.", 650, 50 + 32 + 32 + 32, 16)
            displayText("That's it :D, Enjoy!!", 650, 50 + 32 + 32 + 32 + 32, 16)



        P.render(ori, m_no)
        P.move(dx, dy, walls)
        P.render_health_bar()

    dx, dy = 0, 0

    clock.tick(60)
    # displayText(str(clock.get_fps()), 200, 100)
    displayText( str(P.hitbox.x) + " " + str(P.hitbox.y), 200, 50)
    # displayText( str(offset[0]) + " " + str(offset[1]), 200, 100 )
    # displayText( str(isGrounded), 200, 150 )

    if level != "Menu" and not menuRunning:
        test_2.start()

    if level != "Menu":
        pygame.display.flip()
    screen.fill((127, 127, 127))