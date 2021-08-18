from typing import Tuple

import pygame
import Tank as pl
from controller import Controller
import background as bg
import assets


pygame.init()
pygame.display.set_caption("Tank Game")

screen = pygame.display.set_mode((1000, 600))

running = True

bg_speed = 5

controller = Controller(screen, spawn_pos=[(500, 300), (200, 500)])
player = pl.Player(assets.PLAYER_TANK, screen, (250, 200), controller=controller, speed=5, fire_speed=5, fire_delay=50)
controller.setPlayer(player)

background = bg.Background(assets.BACKGROUND, screen, (-800, -600), speed=bg_speed)

bg_rect = background.getRect()

split = (100, 100)

backg_wall = bg.BackgroundWall(assets.BACKGROUND_WALL1, screen, bg_rect, (0, 0), speed=bg_speed, split=split)
wall_coll1 = backg_wall.getCollisionObject()

backg_wall2 = bg.BackgroundWall(assets.BACKGROUND_WALL2, screen, bg_rect, speed=bg_speed, split=split)
rect = backg_wall2.get_rect()
backg_wall2.setPos(bg_rect.width-rect.width, 0)
wall_coll2 = backg_wall2.getCollisionObject()

backg_wall3 = bg.BackgroundWall(assets.BACKGROUND_WALL3, screen, bg_rect, speed=bg_speed, split=split)
rect = backg_wall3.get_rect()
backg_wall3.setPos(0, bg_rect.height-rect.height)
wall_coll3 = backg_wall3.getCollisionObject()

backg_wall4 = bg.BackgroundWall(assets.BACKGROUND_WALL4, screen, bg_rect, speed=bg_speed, split=split)
rect = backg_wall4.get_rect()
backg_wall4.setPos(bg_rect.width-rect.width, bg_rect.height-rect.height)
wall_coll4 = backg_wall4.getCollisionObject()


bush = bg.BackgroundWall(assets.BUSH, screen, bg_rect, pos=(190, 100), speed=bg_speed, split=(10, 10))
bush_collision = bush.getCollisionObject()

for wall in [(backg_wall, wall_coll1), (backg_wall2, wall_coll2), (backg_wall3, wall_coll3),
             (backg_wall4, wall_coll4)]:
    controller.addObstacle(*wall)


def checkWallCollision(points: Tuple[int, int, int, int]):
    return any((wall_coll1.rect_collide(points)[0], wall_coll2.rect_collide(points)[0],
               wall_coll3.rect_collide(points)[0], wall_coll4.rect_collide(points)[0],
               bush_collision.rect_collide(points)[0]))


controller.spawnEnemy()

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.fire(event.pos)

    key_press = pygame.key.get_pressed()

    background.keyEvent(key_press, player.pos())
    background.update()

    pos = background.getPos()
    controller.setBgPos(pos)
    controller.updateObstacles()

    player.keyEvent(key_press)
    player.mouseEvent(pygame.mouse.get_pos())

    if checkWallCollision(player.getBbox()):
        player.resetPreviousPos()
        background.resetPreviousPos()

    controller.updatePlayers()

    pygame.display.update() 

