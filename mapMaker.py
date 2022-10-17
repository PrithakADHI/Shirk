import pygame, pandas, sys, math

pygame.init()
screen = pygame.display.set_mode((1280,1280))
clock = pygame.time.Clock()
running = True

offset = [100, 0]

images = []

pos1 = []
pos2 = []

erasure = False
fill = False

for x in range(1,10):
    images.append(pygame.image.load("assets/blocks/" + str(x).strip() + ".png").convert())


def displayText(txt, x, y):
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(txt, True, (0,0,0))
    textRect = text.get_rect()
    textRect.center = (x // 2, y // 2)

    screen.blit(text, textRect)

def make_grid(x, y, mx, my, mb, no):
    global fill
    global map, map2, pos1, pos2
    for i in range(x):
        for j in range(y):
            
            if is_colliding(offset[0] +  i * 32, offset[1] + j * 32, 0, 0, 2580, 1600):
                pygame.draw.rect(screen, (50, 255, 100), ( offset[0] +  i * 32, offset[1] + j * 32, 32, 32), 1)

            if is_colliding(mx, my, offset[0] + i * 32, offset[1] + j * 32, 32, 32):
                displayText(str( i ) + " " + str( j ), 100, 100)
                displayText( str(i * 32) + " " + str(j * 32) + " 32 32" , 200, 300)
                displayText( "Fill = " + str(fill) , 200, 400)
            
            if is_colliding(mx, my, offset[0] + i*32, offset[1] + j*32, 32, 32) and mb[0] and not erasure:

                map.append( str(i*32) + " " + str(j*32) + " 32 32 " + str(no).strip() + "\n"  )
                map = pandas.Series(map).drop_duplicates().tolist()
                map2.append( [i*32, j*32, 32, 32, no] )
                map2 = pandas.Series(map2).drop_duplicates().tolist()


            if pos1 != [] and pos2 != []:
                fill_i = [abs(math.ceil((offset[0] - pos1[0])/32)), abs(math.ceil((offset[1] - pos1[1])/32))]
                fill_j = [abs(math.ceil((offset[0] - pos2[0])/32)), abs(math.ceil((offset[1] - pos2[1])/32))]
                print(f"{fill_i} {fill_j}")

                # for r_i in range( fill_j[0], fill_i[0] ):
                #    for r_j in range( fill_j[1], fill_i[1] ):
                #        map.append(str(r_i * 32) + " " + str(r_j * 32) + " 32 32 " + str(no).strip() + "\n")
                #        map2.append([r_i * 32, r_j * 32, 32, 32, no])

                if fill_j[0] < fill_i[0]:
                    for r_i in range( fill_j[0], fill_i[0] + 1 ):

                        if fill_j[1] < fill_i[1]:
                            for r_j in range( fill_j[1], fill_i[1] + 1 ):
                                map.append(str(r_i * 32) + " " + str(r_j * 32) + " 32 32 " + str(no).strip() + "\n")
                                map2.append([r_i * 32, r_j * 32, 32, 32, no])
                        else:
                            for r_j in range(fill_i[1], fill_j[1] + 1):
                                map.append(str(r_i * 32) + " " + str(r_j * 32) + " 32 32 " + str(no).strip() + "\n")
                                map2.append([r_i * 32, r_j * 32, 32, 32, no])


                if fill_j[0] > fill_i[0]:
                    for r_i in range( fill_i[0], fill_j[0] + 1):
                        if fill_j[1] < fill_i[1]:
                            for r_j in range(fill_j[1], fill_i[1] + 1):
                                map.append(str(r_i * 32) + " " + str(r_j * 32) + " 32 32 " + str(no).strip() + "\n")
                                map2.append([r_i * 32, r_j * 32, 32, 32, no])
                        else:
                            for r_j in range(fill_i[1], fill_j[1] + 1):
                                map.append(str(r_i * 32) + " " + str(r_j * 32) + " 32 32 " + str(no).strip() + "\n")
                                map2.append([r_i * 32, r_j * 32, 32, 32, no])

                pos1 = []
                pos2 = []


def is_colliding(x, y, x1, y1, w, h):
    if x >= x1 and y >= y1 and x <= x1 + w and y <= y1 + h:
        return True

def makeMap( map ):
    for i in map:
        # print(i[4])
        if is_colliding(offset[0] + i[0], offset[1] + i[1], 0, 0, 2560, 1600):
            screen.blit(images[ i[4] - 1 ], (offset[0] + i[0], offset[1] + i[1]))

map = []
map2 = []
clicked = False
no = 1

with open("map.mp") as f:
    #w, h = [int(x) for x in next(f).split()]
    array = [[str(x) for x in line.split()] for line in f]
    for x in array:
        #map.append( [ x[0], x[1], x[2], x[3], x[4] ] )
        if x[0] == "Initial":
            pass
        else:
            map.append(  x[0] + " " + x[1] + " " + x[2] + " " + x[3] + " " + x[4] + "\n")
            map2.append( [ int(x[0]), int(x[1]), int(x[2]), int(x[3]), int(x[4]) ] )

fill = False

prev_x, prev_y = 0, 0

while running:
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if map != []:
                f = open("map.mp", "w")
                f.writelines(map)
                f.close()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                no -= 1
            if event.key == pygame.K_w:
                no += 1
            if event.key == pygame.K_f:
                fill = not fill
                pos1 = [mx, my]
            if event.key == pygame.K_e:
                erasure = not erasure

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: no += 1
            if event.button == 5: no -= 1

            if event.button == 1 and fill:
                fill = not fill
                pos2 = [mx, my]
                print(f"{pos1} {pos2}")


    # mx, my = pygame.mouse.get_pos()
    mb = pygame.mouse.get_pressed()

    if mb[0]:
        clicked = True
    else:
        clicked = False

    makeMap(map2)

    if no >= 9:
        no = 9
    if no <= 1:
        no = 1


    k = pygame.key.get_pressed()

    if k[pygame.K_UP]:
        offset[1] += 5
    if k[pygame.K_DOWN]:
        offset[1] -= 5
    if k[pygame.K_RIGHT]:
        offset[0] -= 5
    if k[pygame.K_LEFT]:
        offset[0] += 5

    if k[pygame.K_ESCAPE]:
        print(map)
        if map != []:
            f = open("map.mp", "w")
            f.writelines(map)
            f.close()
        pygame.quit()
        sys.exit()

    move_x, move_y = pygame.mouse.get_rel()
    if k[pygame.K_SPACE]:
        offset[0] += move_x
        offset[1] += move_y

    make_grid(80,40, mx, my, mb, no)


    pygame.draw.rect(screen, (128,128,128), (0,0,3000,32))

    displayText( str(no), 100, 400 )

    icon_img = images[no - 1]
    screen.blit(icon_img, (32,0))

    clock.tick(60)
    pygame.display.flip()
    screen.fill((255,255,255))