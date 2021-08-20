from typing import Tuple

import pygame
import Tank as pl
from controller import Controller
import background as bg
import assets


def checkWallCollision(points: Tuple[int, int, int, int]):
    return any((wall_coll1.rect_collide(points)[0], wall_coll2.rect_collide(points)[0],
                wall_coll3.rect_collide(points)[0], wall_coll4.rect_collide(points)[0]))


def update_spawn_pos():
    global spawn_lst
    bg_rect = background.getPos()
    pre_bg = background.previousPos()
    bg_x, bg_y = bg_rect[0] - pre_bg[0], bg_rect[1] - pre_bg[1]
    spawn_lst = [(bg_x + x[0], bg_y + x[1]) for x in spawn_lst]


time = 0
max_enemy = 5

# score_font = pygame.font.SysFont('Consolas', 30)
#
def main():

    global running, max_enemy, time
    game_over = False
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                player.fire(event.pos)

        if not game_over:
            key_press = pygame.key.get_pressed()

            background.resetprevPos()
            background.keyEvent(key_press, player.pos())

            player.keyEvent(key_press)
            player.mouseEvent(pygame.mouse.get_pos())

            if controller.getEnemyCount() < max_enemy or time + 1 % 100 == 0:
                controller.spawnEnemy()

            if controller.getScore() + 1 % 25 == 0:
                max_enemy += 1

            if checkWallCollision(player.getBbox()):
                player.resetPreviousPos()
                background.resetPreviousPos()
                background.resetprevPos()

            controller.setSpawnlst(spawn_lst)

            time += 1

            if controller.getLives() == 0:
                game_over = True
                controller.reset()

            update_spawn_pos()
            controller.setBgPos(background.getPos(), background.previousPos())

        background.update()
        controller.update()

        for x in range(controller.getLives()):
            screen.blit(life_image, (50 + ((life_image.get_width() + 10) * x), 10))

        if game_over:
            screen.blit(game_over_font.render("GAME OVER", True, (255, 255, 255)), (100, 500))

        pygame.display.update()


if __name__ == "__main__":

    pygame.init()
    pygame.display.set_caption("Tank Game")

    screen = pygame.display.set_mode((1000, 600))

    running = True

    bg_speed = 5
    lives = 3

    life_image = pygame.image.load(assets.LIFE)

    controller = Controller(screen, lives=lives)
    player = pl.Player(assets.PLAYER_TANK, screen, (250, 200), controller=controller, speed=5, fire_speed=5,
                       fire_delay=50)
    controller.setPlayer(player)

    background = bg.Background(assets.BACKGROUND, screen, (-800, -600), speed=bg_speed)

    bg_rect = background.getRect()

    split = (100, 100)

    backg_wall = bg.BackgroundWall(assets.BACKGROUND_WALL1, screen, bg_rect, (0, 0), speed=bg_speed, split=split)
    wall_coll1 = backg_wall.getCollisionObject()

    backg_wall2 = bg.BackgroundWall(assets.BACKGROUND_WALL2, screen, bg_rect, speed=bg_speed, split=split)
    rect = backg_wall2.get_rect()
    backg_wall2.setPos(bg_rect.width - rect.width, 0)
    wall_coll2 = backg_wall2.getCollisionObject()

    backg_wall3 = bg.BackgroundWall(assets.BACKGROUND_WALL3, screen, bg_rect, speed=bg_speed, split=split)
    rect = backg_wall3.get_rect()
    backg_wall3.setPos(0, bg_rect.height - rect.height)
    wall_coll3 = backg_wall3.getCollisionObject()

    backg_wall4 = bg.BackgroundWall(assets.BACKGROUND_WALL4, screen, bg_rect, speed=bg_speed, split=split)
    rect = backg_wall4.get_rect()
    backg_wall4.setPos(bg_rect.width - rect.width, bg_rect.height - rect.height)
    wall_coll4 = backg_wall4.getCollisionObject()

    for wall in [(backg_wall, wall_coll1), (backg_wall2, wall_coll2), (backg_wall3, wall_coll3),
                 (backg_wall4, wall_coll4)]:

        controller.addObstacle(*wall)

    bg_rect = background.getRect()
    x_middle = (bg_rect.x + bg_rect.width) / 2
    y_middle = (bg_rect.y + bg_rect.height) / 2

    spawn_lst = [(bg_rect.x + 350, y_middle), (x_middle, bg_rect.y + 50),
                 ((bg_rect.x + bg_rect.width) - 1500, y_middle), (x_middle, (bg_rect.y + bg_rect.height) - 1500)]

    controller.setSpawnlst(spawn_lst)

    game_over_font = pygame.font.SysFont('Times', 50, True)
    main()
