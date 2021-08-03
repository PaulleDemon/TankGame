import pygame
import math


class Player:

    def __init__(self, screen, pos, speed: float = 0.3):
        
        self.screen = screen
        self.pos_x, self.pos_y = pos
        self.speed = speed

        self.player_image = pygame.image.load(r"assets\playerTank.png")

        self.transformed_image = self.player_image
    
    def update(self):
        self.screen.blit(self.transformed_image, (self.pos_x, self.pos_y))

    def keyEvent(self, key_press):

        if key_press[pygame.K_a]:
            self.pos_x -= self.speed

        if key_press[pygame.K_w]:
            self.pos_y -= self.speed
        
        if key_press[pygame.K_d]:
            self.pos_x += self.speed
        
        if key_press[pygame.K_s]:
            self.pos_y += self.speed
    
    def center(self):
        width, height = self.player_image.get_rect().width, self.player_image.get_rect().height
        return (self.pos_x*2 + width) /2, (self.pos_y*2 + height)/2
    
    def _calcAdjHyp(self, mousepos):
        mouse_x, mouse_y = mousepos
        center_x, center_y = self.center()

        adj = mouse_x - center_x
        opp = mouse_y - center_y
        
        hyp = math.hypot(adj, opp)

        return adj, opp, hyp

    def _calcAngle(self, mousepos):
        adj, opp, hyp = self._calcAdjHyp(mousepos)
        nx, ny = adj/hyp, opp/hyp # normalize

        return math.degrees(math.atan2(-nx, -ny))


    def mouseEvent(self, mousepos):
        
        x, y = mousepos


        angle = self._calcAngle(mousepos)

        self.transformed_image = pygame.transform.rotate(self.player_image, angle)