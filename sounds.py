import pygame
import assets

pygame.mixer.init()

shoot_sound = pygame.mixer.Sound(assets.GUNSHOT)
shoot_sound.set_volume(0.5)