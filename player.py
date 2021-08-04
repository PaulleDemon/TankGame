import pygame
import math


class Tank:

    def __init__(self, img_path: str, screen, pos, speed: float = 0.3, fire_radius: int = 250):
        
        self.screen = screen
        self.pos_x, self.pos_y = pos
        self.speed = speed
        self.angle = 0
        self.mouse_pos = (0, 0)

        self.player_image = pygame.image.load(img_path)

        self.transformed_image = self.player_image

        self._bullets = set()
        self._fire_radius = fire_radius
    

    def update(self):
        self.screen.blit(self.transformed_image, (self.pos_x, self.pos_y))

        for bullet in self._bullets.copy():
            bullet.update()

            if bullet.destroyed():
                self._bullets.remove(bullet)


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
        
        self.mouse_pos = mousepos


        self.angle = self._calcAngle(mousepos)

        self.transformed_image = pygame.transform.rotate(self.player_image, self.angle)


    def fire(self):

        adj, opp, hyp = self._calcAdjHyp(self.mouse_pos)
        pos = (adj/hyp, opp/hyp)

        bullet = Bullet(self.screen, pos, self.center(), self.angle, self._fire_radius)
        self._bullets.add(bullet)


class Bullet:

    def __init__(self, screen, normalpos, tankpos, angle, fire_radius: int, speed: float = 0.3):

        self.screen = screen
        self._destory = False

        self._fire_radius = fire_radius

        self.normal_pos = normalpos[0]*speed, normalpos[1]*speed
        self._initial_pos = normalpos[0] + tankpos[0], normalpos[1] + tankpos[1]
        
        self.current_pos = self._initial_pos
    
        self.angle = angle

        self.bullet_image = pygame.image.load(r"assets\Bullet.png")
        self.transformed_img = self.bullet_image
        

    def update(self):
        self.transformed_img =  pygame.transform.rotate(self.bullet_image, self.angle)
        self.current_pos = (self.normal_pos[0] + self.current_pos[0]), (self.normal_pos[1] + self.current_pos[1])
        
        dist =  math.hypot((self.current_pos[0] - self._initial_pos[0]), (self.current_pos[1] - self._initial_pos[1]))

        if dist >= self._fire_radius:
            self._destory = True

        self.screen.blit(self.transformed_img, self.current_pos)
    

    def destroyed(self):
        return self._destory