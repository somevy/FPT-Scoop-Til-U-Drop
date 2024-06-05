import pygame
from pygame.locals import *
vec = pygame.math.Vector2

class Cone(pygame.sprite.Sprite):
    def __init__(self, image, pos, border, accMode, friction, keys):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.pos = pos
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.border = border
        self.accMode = accMode
        self.friction = friction
        self.keys = keys
        self.keySets = [[K_w, K_a, K_s, K_d], 
                        [K_UP, K_LEFT, K_DOWN, K_RIGHT], 
                        [K_i, K_j, K_k, K_l]] 
    def draw(self, surfaceIn):
        surfaceIn.blit(self.image, self.rect)
    
    def update(self, creamDisplacement):
        self.acc = vec(0, 0)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[self.keySets[self.keys][0]]:
            self.acc.y = -self.accMode
        if pressed_keys[self.keySets[self.keys][1]]:
            self.acc.x = -self.accMode
        if pressed_keys[self.keySets[self.keys][2]]:
            self.acc.y = self.accMode
        if pressed_keys[self.keySets[self.keys][3]]:
            self.acc.x = self.accMode

        self.acc.x += self.vel.x * self.friction
        self.acc.y += self.vel.y * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > self.border[1]:
            self.pos.x = self.border[1]
        if self.pos.x < self.border[0]:
            self.pos.x = self.border[0]
        if self.pos.y > 540 + creamDisplacement:
            self.pos.y = 540 + creamDisplacement
        if self.pos.y < (540/4)*3 + self.rect[3]/2:
            self.pos.y = (540/4)*3 + self.rect[3]/2

        self.rect.center = self.pos
                    
        
