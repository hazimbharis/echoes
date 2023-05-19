import random

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
player_y = 200
width = 450
height = 300
y_change =0
gravity = 1
x_change = 0
obstacle_speed = 2
obstacles = [300,450,600]
active = True

screen = pygame.display.set_mode([width,height])
pygame.display.set_caption('inf runner')
background = black
fps = 60
#font = pygame.font.Font('freesansbold.tff', 16)
timer = pygame.time.Clock()

running = True
while running:
    timer.tick(fps)
    screen.fill(background)
    #score_text = font.render(f'Score: {score}',True,white,black)
    #screen.blit(score_text, (160,250))

    floor = pygame.draw.rect(screen,white,[0,220,width,5] )
    player = pygame.draw.rect(screen,green,[player_x,player_y, 20,20])
    obstacle0 = pygame.draw.rect(screen, red, [obstacles[0],200,20,20])
    obstacle1 = pygame.draw.rect(screen, white, [obstacles[1], 200, 20, 20])
    obstacle2 = pygame.draw.rect(screen, orange, [obstacles[2], 200, 20, 20])

    for event in pygame.event.get(): #for any click, mouse etc
        if event.type == pygame.QUIT:
            running = False
        #jumping code
        if event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_SPACE and y_change ==0: #only jump if not alr jumping
                y_change = 18
            if event.key == pygame.K_RIGHT:
                x_change = 2
            if event.key == pygame.K_LEFT:
                x_change = -2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                x_change = 0
            if event.key == pygame.K_LEFT:
                x_change = 0
    for i in range(len(obstacles)):
        if active:
            obstacles[i] -= obstacle_speed
            if i < -20:
                obstacles[i] = random.randint(470,570)
                score += 1
            if player.colliderect(obstacle0) or player.colliderect(obstacle1) or player.colliderect(obstacle2):
                active = False

    if 0<=player_x <=430:
        player_x += x_change
    if player_x < 0:
        player_x = 0
    if player_x > 430:
        player_x = 430

    if y_change > 0 or player_y < 200: #200 for above floor, subtract when jumping
        player_y -= y_change
        y_change -= gravity

    if player_y > 200:
        player_y= 200 #if player goes thru floor

    if player_y == 200 and y_change < 0:
        y_change = 0


    pygame.display.flip()
pygame.quit()