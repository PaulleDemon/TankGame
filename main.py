import pygame
import player as pl

pygame.init()
pygame.display.set_caption("Tank Game")

screen = pygame.display.set_mode((1000, 600))

running = True

player = pl.Player(screen, (500, 500))


while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    key_press = pygame.key.get_pressed()

    player.keyEvent(key_press)
    player.mouseEvent(pygame.mouse.get_pos())
    player.update()

    pygame.display.update() 