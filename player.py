import pygame
import math
from typing import Tuple

import assets


class Tank:

    def __init__(self, img_path: str, screen, pos, speed: float = 0.5, fire_radius: int = 250, fire_delay: int = 500,
                 fire_speed=0.5):

        self.screen = screen
        self.pos_x, self.pos_y = pos
        self.speed = speed
        self.angle = 0
        self.mouse_pos = (0, 0)
        self._fired = False
        self.fire_speed = fire_speed
        self.fire_delay = fire_delay
        self.time_counter = fire_delay

        self.player_image = pygame.image.load(img_path).convert_alpha()

        self.transformed_image = self.player_image
        self._rect = self.player_image.get_rect()

        self.previous_x, self.previous_y = pos
        # self._bullets = set()
        self._fire_radius = fire_radius

    def keyEvent(self, key_press):

        screen_size = self.screen.get_size()

        pos_x, pos_y = self.pos()

        if key_press[pygame.K_a] and pos_x >= 30:
            self.previous_x = self.pos_x
            self.pos_x -= self.speed

        if key_press[pygame.K_w] and pos_y >= 30:
            self.previous_y = self.pos_y
            self.pos_y -= self.speed

        if key_press[pygame.K_d] and pos_x <= screen_size[0] - 100:
            self.previous_x = self.pos_x
            self.pos_x += self.speed

        if key_press[pygame.K_s] and pos_y <= screen_size[1] - 100:
            self.previous_y = self.pos_y
            self.pos_y += self.speed

    def center(self) -> Tuple[int, int]:
        return self.player_image.get_rect(center=(self.pos_x, self.pos_y)).center

    def fire_pos(self):
        new_dict = 32
        x0, y0 = self.center()
        x1, y1 = self.mouse_pos
        _, _, hyp = self._calcAdjHyp(self.mouse_pos)
        ratio = new_dict / hyp
        x, y = (1 - ratio) * x0 + ratio * x1, (1 - ratio) * y0 + ratio * y1

        return x, y

    def _calcAdjHyp(self, mousepos):
        mouse_x, mouse_y = mousepos
        center_x, center_y = self.center()

        adj = mouse_x - center_x
        opp = mouse_y - center_y

        hyp = math.hypot(adj, opp)

        return adj, opp, hyp

    def _calcAngle(self, mousepos):
        adj, opp, hyp = self._calcAdjHyp(mousepos)
        nx, ny = adj / hyp, opp / hyp  # normalize

        return math.degrees(math.atan2(-nx, -ny))

    def mouseEvent(self, mousepos):
        self.mouse_pos = mousepos
        self.angle = self._calcAngle(mousepos)
        self.transformed_image = pygame.transform.rotate(self.player_image, self.angle)
        self._rect = self.transformed_image.get_rect(center=(self.pos_x, self.pos_y))

    def fire(self):

        if not self._fired:
            self._fired = True
            adj, opp, hyp = self._calcAdjHyp(self.mouse_pos)
            n_pos = (adj / hyp, opp / hyp)
            createBullet(self.screen, self, n_pos, self.fire_pos(), self.angle, self._fire_radius, self.fire_speed)
            # bullet = Bullet(self.screen, n_pos, self.fire_pos(), self.angle, self._fire_radius, self.fire_speed)
            # self._bullets.add(bullet)

    def getBbox(self):
        rect = self.transformed_image.get_rect(center=(self.pos_x, self.pos_y))
        return rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]

    def getRectObject(self):
        return self.transformed_image.get_rect(center=(self.pos_x, self.pos_y))

    def resetPreviousPos(self):
        self.pos_x, self.pos_y = self.previous_x, self.previous_y

    def pos(self) -> Tuple[float, float]:
        return self._rect[:2]

    def update(self):
        self.screen.blit(self.transformed_image, self._rect)
        if self.time_counter > 0:
            self.time_counter -= 1

        else:
            self.time_counter = self.fire_delay
            self._fired = False

    def colliderect(self, rect):
        return self.getRectObject().colliderect(rect)

    def collidelist(self, lst):
        return self.getRectObject().collidelist(lst)


class Bullet:

    def __init__(self, screen, tank_object, normalpos, tankpos, angle, fire_radius: int, speed: float = 0.5):
        self.screen = screen
        self._destory = False
        self.bullet_image = pygame.image.load(assets.BULLET).convert_alpha()
        self.transformed_img = self.bullet_image

        self.tank = tank_object  # tank object from which the bullet was fired

        self._fire_radius = fire_radius

        self.normal_pos = normalpos[0] * speed, normalpos[1] * speed
        self._initial_pos = tankpos[0], tankpos[1]

        rect = self.transformed_img.get_rect()
        self.current_pos = tankpos[0] - rect.centerx, tankpos[1] - rect.centery

        self.angle = angle

    def update(self):
        self.transformed_img = pygame.transform.rotate(self.bullet_image, self.angle)
        self.current_pos = (self.normal_pos[0] + self.current_pos[0]), (self.normal_pos[1] + self.current_pos[1])

        # dist = math.hypot((self.current_pos[0] - self._initial_pos[0]), (self.current_pos[1] - self._initial_pos[1]))

        # if dist >= self._fire_radius:
        print("DIST: ", self.dist())
        if self.dist() >= self._fire_radius:
            self._destory = True

        self.screen.blit(self.transformed_img, self.current_pos)

    def dist(self):
        return math.hypot((self.current_pos[0] - self._initial_pos[0]), (self.current_pos[1] - self._initial_pos[1]))

    def destroyed(self):
        return self._destory

    def getRect(self):
        return self.transformed_img.get_rect(center=(self.current_pos))

    def colliderect(self, rect):
        return self.getRect().colliderect(rect)

    def collidelist(self, lst):
        return self.getRect().collidelist(lst)

    def tankObject(self):
        return self.tank


bullets = set()
tanks = set()


def addToTank(tank):
    tanks.add(tank)


def updateTanks():
    for tank in tanks:
        tank.update()


def checkCollision():
    for tank in tanks.copy():

        if tank.collidelist([bullet.getRect() for bullet in bullets if tank!=bullet.tankObject()]) != -1:
            tanks.remove(tank)


def createBullet(screen, tank_object, normal_pos, fire_pos, angle, radius, speed):
    bullet = Bullet(screen, tank_object, normal_pos, fire_pos, angle, radius, speed)
    bullets.add(bullet)


def update_bullets():

    for bullet in bullets.copy():
        bullet.update()

        if bullet.destroyed():
            bullets.remove(bullet)


