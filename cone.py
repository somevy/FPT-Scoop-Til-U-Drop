import pygame
from pygame.locals import *
vec = pygame.math.Vector2
# friction = -0.05
# acc = 1.0

class Cone(pygame.sprite.Sprite):
    def __init__(self, image, pos, leftBorder, rightBorder, player, accMode, friction):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.pos = pos
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.leftBorder, self.rightBorder = leftBorder, rightBorder
        self.player = player
        self.accMode = accMode
        self.friction = friction
        # self.player_position = vec(0, 0)
    
    def draw(self, surfaceIn):
        surfaceIn.blit(self.image, self.rect)
    
    def update(self, creamDisplacement):
        # pass
        self.acc = vec(0, 0)

        pressed_keys = pygame.key.get_pressed()

        if self.player == "p1":
            if pressed_keys[K_a]:
                self.acc.x = -self.accMode
            if pressed_keys[K_d]:
                self.acc.x = self.accMode
            if pressed_keys[K_w]:
                self.acc.y = -self.accMode
            if pressed_keys[K_s]:
                self.acc.y = self.accMode
        else:
            if pressed_keys[K_LEFT]:
                self.acc.x = -self.accMode
            if pressed_keys[K_RIGHT]:
                self.acc.x = self.accMode
            if pressed_keys[K_UP]:
                self.acc.y = -self.accMode
            if pressed_keys[K_DOWN]:
                self.acc.y = self.accMode

        self.acc.x += self.vel.x * self.friction
        self.acc.y += self.vel.y * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > self.rightBorder:
            self.pos.x = self.rightBorder
        if self.pos.x < self.leftBorder:
            self.pos.x = self.leftBorder
        if self.pos.y > 540 + creamDisplacement:
            self.pos.y = 540 + creamDisplacement
        if self.pos.y < (540/4)*3 + self.rect[3]/2:
            self.pos.y = (540/4)*3 + self.rect[3]/2

        self.rect.center = self.pos
                    
        
