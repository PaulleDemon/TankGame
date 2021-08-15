import pygame
import player as pl
import background as bg
import assets


pygame.init()
pygame.display.set_caption("Tank Game")

screen = pygame.display.set_mode((1000, 600))

running = True

bg_speed = 2

player = pl.Tank(assets.PLAYER_TANK, screen, (500, 300), speed=2)

background = bg.Background(assets.BACKGROUND, screen, (0, 0), speed=bg_speed)

bg_rect = background.getRect()

backg_wall = bg.BackgroundWall(assets.BACKGROUND_WALL1, screen, bg_rect, (0, 0), speed=bg_speed)

backg_wall2 = bg.BackgroundWall(assets.BACKGROUND_WALL2, screen, bg_rect, speed=bg_speed)
rect = backg_wall2.get_rect()
backg_wall2.setPos(bg_rect.width-rect.width, 0)

backg_wall3 = bg.BackgroundWall(assets.BACKGROUND_WALL3, screen, bg_rect, speed=bg_speed)
rect = backg_wall3.get_rect()
backg_wall3.setPos(0, bg_rect.height-rect.height)


backg_wall4 = bg.BackgroundWall(assets.BACKGROUND_WALL4, screen, bg_rect, speed=bg_speed)
rect = backg_wall4.get_rect()
backg_wall4.setPos(bg_rect.width-rect.width, bg_rect.height-rect.height)

# background = bg.Background(r"assets\testTile.jpg", screen, (0, 0))


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

    pos = background.getPos()

    backg_wall.update(pos)
    backg_wall2.update(pos)
    backg_wall3.update(pos)
    backg_wall4.update(pos)

    player.keyEvent(key_press)
    player.mouseEvent(pygame.mouse.get_pos())
    player.update()

    pygame.display.update() 

