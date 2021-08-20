import random

import pygame
from typing import Tuple
from pycollision import Collision

# fixme: background moves to show black area


class Background:

    def __init__(self, img: str, screen, pos=(0, 0), speed: float = 0.5):

        self.bg_image = pygame.image.load(img).convert_alpha()
        self.speed = speed
        self.bg_x, self.bg_y = pos
        self.screen = screen
        self.previous_x, self.previous_y = pos
        self.pre_x, self.pre_y = pos

    def update(self):
        self.screen.blit(self.bg_image, (self.bg_x, self.bg_y))

    def keyEvent(self, key_press, playerpos: Tuple[float, float]):

        x, y = playerpos

        screen_rect = self.screen.get_rect()
        image_rect = self.bg_image.get_rect()

        self.pre_x, self.pre_y = self.bg_x, self.bg_y

        if 150 >= x >= self.bg_x + 150 and key_press[pygame.K_a]:
            self.previous_x = self.bg_x
            self.bg_x += self.speed

        if 150 >= y >= self.bg_y + 150 and key_press[pygame.K_w]:
            self.previous_y = self.bg_y
            self.bg_y += self.speed

        if screen_rect.width - 350 <= x <= self.bg_x + image_rect.width - 250 and key_press[pygame.K_d]:
            self.previous_x = self.bg_x
            self.bg_x -= self.speed

        if screen_rect.height - 350 <= y <= self.bg_y + image_rect.height - 250 and key_press[pygame.K_s]:
            self.previous_y = self.bg_y
            self.bg_y -= self.speed

    def resetprevPos(self):
        self.pre_x, self.pre_y = self.bg_x, self.bg_y

    def getPos(self):
        return self.bg_x, self.bg_y

    def getRect(self):
        return self.bg_image.get_rect()

    def previousPos(self):
        return self.pre_x, self.pre_y

    def resetPreviousPos(self):
        self.bg_x, self.bg_y = self.previous_x, self.previous_y

    def setPos(self, pos):
        self.bg_x, self.bg_y = pos


class BackgroundWall:

    def __init__(self, img: str, screen, bg_rect, pos=(0, 0), speed: float = 0.5, split=(5, 5)):
        self.bg_image = pygame.image.load(img).convert_alpha()
        self.speed = speed
        self.bg_x, self.bg_y = pos
        self.orgPos = list(pos)
        self.screen = screen

        self.bg_rect = bg_rect

        self._collision = False
        self.collision = Collision(img, split, wall_collision=True, wall_padding=(1, 1, 1, 1))

    def setPos(self, x, y):
        self.orgPos = list((x, y))
        self.bg_x, self.bg_y = x, y
        self.collision.setSpritePos(self.bg_x, self.bg_y)

    def update(self, bgpos: Tuple[float, float]):
        self.bg_x = self.orgPos[0] + bgpos[0]
        self.bg_y = self.orgPos[1] + bgpos[1]
        self.screen.blit(self.bg_image, (self.bg_x, self.bg_y))

        self.collision.setSpritePos(self.bg_x, self.bg_y)

    def getCollisionObject(self):
        return self.collision

    def get_rect(self) -> pygame.Rect:
        return self.bg_image.get_rect()

    def getPos(self):
        return self.bg_x, self.bg_y
