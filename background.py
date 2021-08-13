import pygame
from typing import Tuple
import assets


class Background:

    def __init__(self, img: str, screen, pos = (0, 0), speed: float = 0.3):
        
        self.bg_image = pygame.image.load(assets.BACKGROUND).convert_alpha()
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
        if x <= 10 and key_press[pygame.K_a] and x >=  self.bg_x + 10:
            self.bg_x += self.speed

        if y <= 10 and key_press[pygame.K_w] and y >=  self.bg_y + 10:
            self.bg_y += self.speed

        if x >= screen_rect.width - 150 and key_press[pygame.K_d] and x <= self.bg_x + image_rect.width - 150:
            self.bg_x -= self.speed

        if y >= screen_rect.height - 150 and key_press[pygame.K_s] and y <= self.bg_y + image_rect.height - 150:
            self.bg_y -= self.speed
