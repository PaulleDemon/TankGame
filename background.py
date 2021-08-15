import pygame
from typing import Tuple
from pycollision import Collision


class Background:

    def __init__(self, img: str, screen, pos=(0, 0), speed: float = 0.5):

        self.bg_image = pygame.image.load(img).convert_alpha()
        self.speed = speed
        self.bg_x, self.bg_y = pos
        self.screen = screen

    def update(self):
        self.screen.blit(self.bg_image, (self.bg_x, self.bg_y))

    def keyEvent(self, key_press, playerpos: Tuple[float, float]):

        x, y = playerpos

        screen_rect = self.screen.get_rect()
        image_rect = self.bg_image.get_rect()

        # print(image_rect, self.bg_x, self.bg_y, x, y)
        if 10 >= x >= self.bg_x + 10 and key_press[pygame.K_a]:
            self.bg_x += self.speed

        if 10 >= y >= self.bg_y + 10 and key_press[pygame.K_w]:
            self.bg_y += self.speed

        if screen_rect.width - 150 <= x <= self.bg_x + image_rect.width - 150 and key_press[pygame.K_d]:
            self.bg_x -= self.speed

        if screen_rect.height - 150 <= y <= self.bg_y + image_rect.height - 150 and key_press[pygame.K_s]:
            self.bg_y -= self.speed

    def getPos(self):
        return self.bg_x, self.bg_y

    def getRect(self):
        return self.bg_image.get_rect()


class BackgroundWall:

    def __init__(self, img: str, screen, bg_rect, pos=(0, 0), speed: float = 0.5, check_collision=False, split=(5, 5)):
        self.bg_image = pygame.image.load(img).convert_alpha()
        self.speed = speed
        self.bg_x, self.bg_y = pos
        self.orgPos = list(pos)
        self.screen = screen

        self.bg_rect = bg_rect

        self._collision = False

        if check_collision:
            self.collision = Collision(img, wall_collision=True, wall_padding=(2, 2, 2, 2))

    def setPos(self, x, y):
        self.orgPos = list((x, y))
        self.bg_x, self.bg_y = x, y

    def update(self, bgpos: Tuple[float, float]):
        self.bg_x = self.orgPos[0] + bgpos[0]
        self.bg_y = self.orgPos[1] + bgpos[1]
        self.screen.blit(self.bg_image, (self.bg_x, self.bg_y))

    def key_event(self):
        # todo: collision
        pass

    def get_rect(self) -> pygame.Rect:
        return self.bg_image.get_rect()

    def getPos(self):
        return self.bg_x, self.bg_y
