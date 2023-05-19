import pygame
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 500))
pygame.display.set_caption("Echoes")
clock = pygame.time.Clock()
running = True
dt = 0 # delta time

# load bg image
bg = pygame.image.load("bg.png").convert()
bg_width = bg.get_width()

# get rect for bg image
bg_rect = bg.get_rect()

# define game variables
scroll = 0
tiles = math.ceil(1280 / bg_width) + 1
obstacle = pygame.Rect(400, 200, 80, 80)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # draw scrolling background and bg edge
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))
        bg_rect.x = i * bg_width + scroll
        pygame.draw.rect(screen, (0, 255, 0), bg_rect, 1)

    # scroll background
    scroll -= 5

    # reset scroll
    if abs(scroll) > bg_width:
        scroll = 0

    # draw obstacle
    pygame.draw.rect(screen, (0,0,0), obstacle, 4)

    # draw player circle
    pygame.draw.circle(screen, "red", player_pos, 40)

    # draw player hitbox
    pygame.draw.rect(screen, "green", ((player_pos.x - 40, player_pos.y - 40), (80,80)), 1)

    # input handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
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
