import pygame
import player as pl
import background as bg

pygame.init()
pygame.display.set_caption("Tank Game")

screen = pygame.display.set_mode((1000, 600))

running = True

player = pl.Tank(r"assets\playerTank.png", screen, (500, 300))
# background = bg.Background(r"assets\background.png", screen, (0, 0))
background = bg.Background(r"assets\testTile.jpg", screen, (0, 0))


while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.fire()


    key_press = pygame.key.get_pressed()


    background.keyEvent(key_press, player.pos())
    background.update()

    player.keyEvent(key_press)
    player.mouseEvent(pygame.mouse.get_pos())
    player.update()

    pygame.display.update() 
