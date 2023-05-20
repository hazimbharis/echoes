import random
import os
import pygame

pygame.init()

#constants
white= (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
orange = (255,165,0)

#game variables
score =0
player_x = 50
player_y = 400
width = 1280
height = 500
y_change =0
gravity = 1
x_change = 0
obstacle_speed = 3
obstacle_count = int((width / 100)  - 1)
obstacles = []
rectangles = []
curr_obs_count =0


for x in range(0,obstacle_count):
    pos = random.randint(200, 1280)  # x position
    rectHeight = random.randint(0,100) # y position
    if curr_obs_count == 0:
        value = [pos, rectHeight]
        rectangles.append(1)
        obstacles.append(value)
        curr_obs_count += 1
    else:
        valid = True
        for i in range(0,len(obstacles)): #iterate over all of them, if any break rule then restart
            if abs(obstacles[i][0] - pos)<100:
                valid = False
                break
        #otherwise must be correct
        if(valid):
            value = [pos, rectHeight]
            rectangles.append(1)
            obstacles.append(value)
            curr_obs_count += 1


active = True

screen = pygame.display.set_mode([width,height])
pygame.display.set_caption('inf runner')
background = black
fps = 60
#font = pygame.font.Font('freesansbold.tff', 16)
timer = pygame.time.Clock()

def generateNewRect(obstacles,i):

        pos = random.randint(200, 1280)  # x position
        rectHeight = random.randint(0, 100)  # y position
        valid = True
        for y in range(0, len(obstacles)):  # iterate over all of them, if any break rule then restart
            if abs(obstacles[y][0] - pos) < 100:
                valid = False
                break
        # otherwise must be correct
        if (valid):
            obstacles[i][0] = pos
            obstacles[i][1] = rectHeight


playerStandingSprite = pygame.image.load('standing_frame.png').convert_alpha()
playerWalkingSprite = pygame.image.load('walking_animation.gif').convert_alpha()
playerJumpingSprite = pygame.image.load('jumping_frame.png').convert_alpha()
running = True

while running and active:
    print(player_y)
    timer.tick(fps)
    screen.fill(background)
    #score_text = font.render(f'Score: {score}',True,white,black)
    #screen.blit(score_text, (160,250))

    floor = pygame.draw.rect(screen,white,[0,420,width,5] )
    player = pygame.draw.rect(screen,black,[player_x,player_y, 20,20])
   # screen.blit(playerStandingSprite,(player_x-20,player_y-30))

    print(player_y)
    for i in range(0,len(obstacles)):
        rectangle = pygame.draw.rect(screen, red, [obstacles[i][0], 420 - obstacles[i][1], 20, obstacles[i][1]])
        rectangles[i] = rectangle

    for event in pygame.event.get(): #for any click, mouse etc
        if event.type == pygame.QUIT:
            running = False
        #jumping code
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and y_change ==0: #only jump if not alr jumping
                y_change = 18
                screen.blit(playerJumpingSprite,(player_x-20,player_y-30))

            screen.blit(playerWalkingSprite,(player_x-20,player_y-30))
            if event.key == pygame.K_RIGHT:

                x_change = 2
            if event.key == pygame.K_LEFT:
                x_change = -2

        if event.type == pygame.KEYUP:
            screen.blit(playerStandingSprite, (player_x - 20, player_y - 30))
            if event.key == pygame.K_RIGHT:
                x_change = 0
            if event.key == pygame.K_LEFT:
                x_change = 0
    for i in range(len(obstacles)):
        if active:
            obstacles[i][0] -= obstacle_speed
            if obstacles[i][0] < -20:
                generateNewRect(obstacles,i)
               # obstacles[i][1] = random.randint(10,150) # new height
               # obstacles[i][0] = random.randint(200,600) # new pos
                score += 1

            if player.colliderect(rectangles[i]):
                active = False


    if 0<=player_x <=200:
        player_x += x_change
        screen.blit(playerStandingSprite, (player_x - 20, player_y - 30))

    if player_x < 0:
        player_x = 0
        active= False #player loses

    if player_x > 200:
        player_x = 200

    if y_change > 0 or player_y < 400: #200 for above floor, subtract when jumping
        player_y -= y_change
        y_change -= gravity
        screen.blit(playerJumpingSprite, (player_x - 20, player_y - 30))

    if player_y > 400:
        player_y= 400 #if player goes thru floor

    if player_y == 400 and y_change < 0:
        y_change = 0


    pygame.display.flip()
pygame.quit()