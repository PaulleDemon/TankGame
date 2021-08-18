import random

import pygame
import math
from typing import Tuple
import assets


class Tank:

    def __init__(self, img_path: str, screen, pos, controller, speed: float = 0.5,
                 fire_destroy_radius: int = 250, fire_delay: int = 500, fire_speed=0.5):

        self.screen = screen
        self.pos_x, self.pos_y = pos
        self.speed = speed
        self.angle = 0
        self._fired = False
        self.fire_speed = fire_speed
        self.fire_delay = fire_delay
        self.time_counter = fire_delay
        self.controller = controller

        self.tank_image = pygame.image.load(img_path).convert_alpha()

        self.transformed_image = self.tank_image
        self._rect = self.tank_image.get_rect()

        self.previous_x, self.previous_y = pos
        self._fire_radius = fire_destroy_radius

    def center(self) -> Tuple[int, int]:
        return self.tank_image.get_rect(center=(self.pos_x, self.pos_y)).center

    def fire_pos(self, pos):
        new_dict = 32
        x0, y0 = self.center()
        x1, y1 = pos
        _, _, hyp = self._calcAdjHyp(pos)
        ratio = new_dict / hyp
        x, y = (1 - ratio) * x0 + ratio * x1, (1 - ratio) * y0 + ratio * y1

        return x, y

    def _calcAdjHyp(self, pos):
        mouse_x, mouse_y = pos
        center_x, center_y = self.center()

        adj = mouse_x - center_x
        opp = mouse_y - center_y

        hyp = math.hypot(adj, opp)

        return adj, opp, hyp

    def _calcAngle(self, pos):
        """ calculates angle towards a point """
        adj, opp, hyp = self._calcAdjHyp(pos)
        nx, ny = adj / hyp, opp / hyp  # normalize

        return math.degrees(math.atan2(-nx, -ny))

    def fire(self, pos):

        if not self._fired:
            self._fired = True
            adj, opp, hyp = self._calcAdjHyp(pos)
            n_pos = (adj / hyp, opp / hyp)
            self.controller.createBullet(self, n_pos, self.fire_pos(pos), self.angle,
                                         self._fire_radius, self.fire_speed)

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


class Enemy(Tank):  # todo: complete this, move the enemy with the background else it will follow the player

    def __init__(self, follow_radius, fire_radius, bg_pos=(0, 0), *args, **kwargs):
        super(Enemy, self).__init__(*args, **kwargs)
        self.change_angle()
        self.steps = 0
        self.max_steps = 0

        self.direction_x, self.direction_y = (0, 0)
        self.bg_x, self.bg_y = bg_pos

    def change_angle(self):
        self.angle = random.randint(0, 360)
        self.direction_x = math.cos(math.radians(self.angle)) * 0.2
        self.direction_y = math.sin(math.radians(self.angle)) * 0.2

        self.transformed_image = pygame.transform.rotate(self.tank_image, self.angle)

    def setBgPos(self, bgpos):
        self.bg_x, self.bg_y = bgpos

    def moveRandom(self):

        self.pos_x = self.direction_x + self.pos_x #+ self.bg_x
        self.pos_y = self.direction_y + self.pos_y #+ self.bg_y
        self.steps += 1

        if self.steps > self.max_steps:
            self.steps = 0
            self.max_steps = random.randint(50, 300)
            self.change_angle()

        self._rect = self.transformed_image.get_rect(center=(self.pos_x, self.pos_y))

    def update(self):
        super(Enemy, self).update()
        # print(self.getRectObject())
        print(self.getRectObject())
        self.moveRandom()

    def moveTo(self, pos):
        pass


class Player(Tank):

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.mouse_pos = (0, 0)

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

    def mouseEvent(self, mousepos):
        self.mouse_pos = mousepos
        self.angle = self._calcAngle(mousepos)
        self.transformed_image = pygame.transform.rotate(self.tank_image, self.angle)
        self._rect = self.transformed_image.get_rect(center=(self.pos_x, self.pos_y))


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

    def getBbox(self):
        rect = self.transformed_img.get_rect(center=self.current_pos)
        return rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]