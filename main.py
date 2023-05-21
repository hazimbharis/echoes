import pygame, math, random, pygame.freetype

# pygame setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((1280, 500), flags=pygame.SCALED, vsync=1)
pygame.display.set_caption("Echoes")
clock = pygame.time.Clock()
running = True
dt = 0 # delta time
my_font = pygame.freetype.Font('m5x7.ttf', 72)
score_font = pygame.freetype.Font('m5x7.ttf', 48)
# text_surface = my_font.render('You Lose', True, (255, 255, 255), 0)[0]
# score_surface = score_font.render('Score: ' + clock.get_time().__str__(), True, (255, 255, 255), 0)[0]

# load bg image
bg1 = pygame.image.load("plain_background.png").convert()
bg2 = pygame.image.load("stalagmite_background.png").convert()
bg1 = pygame.transform.scale(bg1,(1280,500))
bg2 = pygame.transform.scale(bg2,(1280,500))

playerStandingSprite = pygame.image.load('standing_frame.png').convert_alpha()
playerWalkingSprite = pygame.image.load('walking_animation.gif').convert_alpha()
playerJumpingSprite = pygame.image.load('jumping_frame.png').convert_alpha()

bg1_width = bg1.get_width()
bg1_height = bg1.get_height()
bg2_width = bg2.get_width()
bg2_height = bg2.get_width()

bgx = 0
bgx2 = bg1.get_width()

# load sound
echo_sound = pygame.mixer.Sound('heartbeat_2.wav')
# get rect for bg image
bg_rect = bg1.get_rect()

# define game variables
scrollspeed = 0
tiles = math.ceil(1280 / bg1_width) + 1
obstacle = pygame.Rect(800, 200, 80, 80)

player_pos = pygame.Vector2(80, 440)
player_rect = pygame.Rect(player_pos.x, player_pos.y, 20, 20)

x_change = 0
y_change = 0

screen_shake = 0
particles = []
circle_effects = []
gameover = False
final_score = 0

# runner variables
gravity = 1
obstacle_speed = 3
obstacle_count = int((1280 / 100) - 1)
obstacles = []
rectangles = []
curr_obs_count = 0

def generateNewRect(obstacles,i):
    pos = random.randint(1280, 1280)  # x position
    rectHeight = random.randint(10, 100)  # y position
    valid = True
    for y in range(0, len(obstacles)):  # iterate over all of them, if any break rule then restart
        if abs(obstacles[y][0] - pos) < 100:
            valid = False
            break
    # otherwise must be correct
    if (valid):
        obstacles[i][0] = pos
        obstacles[i][1] = rectHeight


for x in range(0,obstacle_count):
    pos = random.randint(300, 1280)  # x position
    rectHeight = random.randint(10,100) # y position
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


while running:

    if gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")
        my_font.render_to(screen, (540, 220), "You Lose", (0, 0, 0))
        score_font.render_to(screen, (580, 270), "Score: " + final_score.__str__(), (0, 0, 0))
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        continue


    x_change = 0
    # y_change = 0
    bgx -= 3
    bgx2 -= 3

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    #moving background with multiple images
    if bgx < bg1.get_width() * -1:
        bgx = bg1.get_width()
    if bgx2 < bg1.get_width() * -1:
        bgx2 = bg1.get_width()

    # draw scrolling background and bg edge
    for i in range(0, tiles):
        # screen.blit(bg, (i * bg_width + scrollspeed, 0))
        screen.blit(bg1, (bgx, 0))
        screen.blit(bg2,(bgx2, 0))
        bg_rect.x = bgx + scrollspeed
        # bg_rect.x = i * bg_width + scrollspeed
        # pygame.draw.rect(screen, (0, 255, 0), bg_rect, 1)

    for i in range(len(obstacles)):
        obstacles[i][0] -= obstacle_speed
        if obstacles[i][0] < -20:
            generateNewRect(obstacles, i)
            # obstacles[i][1] = random.randint(10,150) # new height
            # obstacles[i][0] = random.randint(200,600) # new pos
            # score += 1

    # print(player_pos.y)
    if player_pos.y < 440: #200 for above floor, subtract when jumping
        player_pos.y += y_change
        y_change += gravity

    if player_pos.y > 440:
        player_pos.y = 440
        y_change = 0

    # scroll background
    scrollspeed -= 5

    # reset scroll
    if abs(scrollspeed) > bg1_width:
        scrollspeed = 0

    screen.fill("black")
    score_font.render_to(screen, (10, 10), "Score: " + math.floor(pygame.time.get_ticks()/100).__str__(), (255, 255, 255))

    # draw player circle
    pygame.draw.circle(screen, "red", player_pos, 40)
    screen.blit(playerStandingSprite,
                (player_pos.x - playerStandingSprite.get_width()/2 + 1, player_pos.y - playerStandingSprite.get_height()/2 + 20))




    # Circle Effects ----------------------------------------- #
    # pos, radius, width, speed, decay, color
    for i, circle in sorted(list(enumerate(circle_effects)), reverse=True):

        circle[1] += circle[3]
        circle[2] -= circle[4]
        if circle[2] < 1:
            circle_effects.pop(i)
        else:
            pygame.draw.circle(
                screen,
                circle[5],
                (circle[0][0], circle[0][1]),
                int(circle[1]),
                min(int(circle[2]), int(circle[1])))

        if (circle[0][0] + circle[1]) > (obstacle[0] - obstacle[2]):
            particles.append([[obstacle[0] + obstacle[2]/2, obstacle[1] + obstacle[3]/2], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])

        for rectangle in rectangles:

            if (circle[0][0] + circle[1]) > (rectangle[0] - rectangle[2]):
                particles.append([[rectangle[0] + rectangle[2] / 2, rectangle[1] + rectangle[3] / 2],
                                  [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])

    # draw obstacles
    pygame.draw.rect(screen, (0,0,0), obstacle, 0)
    for i in range(0, len(obstacles)):
        rectangle = pygame.draw.rect(screen, (0, 0, 0), [obstacles[i][0], 480 - obstacles[i][1], 40, obstacles[i][1]])
        rectangles[i] = rectangle

    for rectangle in rectangles:

        if player_rect.colliderect(rectangle):
            screen_shake = 20
            player_pos.x = player_pos.x - x_change
            player_pos.y = player_pos.y - y_change
            pygame.draw.rect(screen, "red", player_rect, 1)
            my_font.render_to(screen, (560,250), "You Lose", (255, 255, 255))
            gameover = True
            final_score = math.floor(pygame.time.get_ticks()/100)
            # screen.blit(text_surface, (560, 250))

    # pygame.draw.rect(screen, (0,0,0), (obstacle[0] + scrollspeed, obstacle[1], obstacle[2] + scrollspeed, obstacle[3]), 0)

    # draw player hitbox
    # pygame.draw.rect(screen, "green", player_rect, 1)

    # input handling
    keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     y_change -= 300 * dt
    # if keys[pygame.K_s]:
    #     y_change += 300 * dt
    # print(y_change)
    if keys[pygame.K_SPACE] and player_pos.y > 360:
        y_change -= 150 * dt
    if keys[pygame.K_a]:
        x_change -= 300 * dt
    if keys[pygame.K_d]:
        x_change += 300 * dt

    # player_pos.x = player_pos.x + x_change
    # player_pos.y = player_pos.y + y_change
    # player_rect.x = player_pos.x - 40
    # player_rect.y = player_pos.y - 40

    player_pos.x = player_pos.x + x_change
    player_pos.y = player_pos.y + y_change
    player_rect.x = player_pos.x - 10
    player_rect.y = player_pos.y + 10

    if keys[pygame.K_SPACE] and (player_pos.y - y_change) == 440:
        screen_shake = 20
        echo_sound.play()
        particles.append([[player_pos.x, player_pos.y], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])
        circle_effects.append([(player_pos.x, player_pos.y), 10, 4, 5, 0.2, (255, 255, 255)]) # pos, radius, width, speed, decay, color
        circle_effects.append([(player_pos.x, player_pos.y), 0, 10, 7, 0.1, (255, 255, 255)]) # pos, radius, width, speed, decay, color
        #circle_effects = []                                 0,  7, 4, 0.1

    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        pygame.draw.circle(screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)  # can cause flickering for larger particle sizes

    if screen_shake > 0:
        screen_shake -= 1

    render_offset = [0, 0]

    if screen_shake:
        render_offset[0] = random.randint(0, 8) - 4
        render_offset[1] = random.randint(0, 8) - 4
        pass

    if player_rect.colliderect(obstacle):
        screen_shake = 20
        player_pos.x = player_pos.x - x_change
        player_pos.y = player_pos.y - y_change
        pygame.draw.rect(screen, "red", player_rect, 1)

    if player_pos.x < 10:
        player_pos.x = 10

    if player_pos.x > 1270:
        player_pos.x = 1270

    # RENDER YOUR GAME HERE
    floor = pygame.draw.rect(screen, (0,0,0), [0, 480, screen.get_width(), 20])

    # flip() the display to put your work on screen
    screen.blit(screen, render_offset)
    pygame.display.flip()

    dt = clock.tick(60)/1000 # limits FPS to 30

pygame.quit()

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
