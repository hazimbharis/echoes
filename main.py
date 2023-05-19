import pygame, math, random

class Echo(object):
    def __int__(self, pos):
        self.pos = pos


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 500))
pygame.display.set_caption("Echoes")
clock = pygame.time.Clock()
running = True
dt = 0 # delta time

# load bg imagedd
bg1 = pygame.image.load("plain_background.png").convert()
bg2 = pygame.image.load("stalagmite_background.png").convert()
bg1 = pygame.transform.scale(bg1,(1280,500))
bg2 = pygame.transform.scale(bg2,(1280,500))
bg1_width = bg1.get_width()
bg1_height = bg1.get_height()
bg2_width = bg2.get_width()
bg2_height = bg2.get_width()

bgx = 0
bgx2 = bg1.get_width()


# get rect for bg image
bg_rect = bg1.get_rect()

# define game variables
scroll = 0
tiles = math.ceil(1280 / bg1_width) + 1
obstacle = pygame.Rect(800, 200, 80, 80)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_rect = pygame.Rect(player_pos.x - 40, player_pos.y - 40, 80, 80)

x_change = 0
y_change = 0

screen_shake = 0

while running:
    x_change = 0
    y_change = 0
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

    for i in range(0, tiles):
     screen.blit(bg1, (bgx, 0))
     screen.blit(bg2,(bgx2, 0))
     bg_rect.x = bgx + scroll
     pygame.draw.rect(screen, (0, 255, 0), bg_rect, 1)


    # scroll background
    scroll -= 5

    # reset scroll
    if abs(scroll) > bg1_width:
        scroll = 0

    # draw obstacle
    pygame.draw.rect(screen, (0,0,0), obstacle, 4)

    # draw player circle
    pygame.draw.circle(screen, "red", player_pos, 40)

    # draw player hitbox
    pygame.draw.rect(screen, "green", player_rect, 1)

    # input handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        y_change -= 300 * dt
    if keys[pygame.K_s]:
        y_change += 300 * dt
    if keys[pygame.K_a]:
        x_change -= 300 * dt
    if keys[pygame.K_d]:
        x_change += 300 * dt

    player_pos.x = player_pos.x + x_change
    player_pos.y = player_pos.y + y_change
    player_rect.x = player_pos.x - 40
    player_rect.y = player_pos.y - 40

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

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    screen.blit(screen, render_offset)
    pygame.display.flip()

    dt = clock.tick(60)/1000 # limits FPS to 60

pygame.quit()
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
