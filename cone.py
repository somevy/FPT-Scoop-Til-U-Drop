import pygame
from pygame.locals import *
vec = pygame.math.Vector2

class Cone(pygame.sprite.Sprite):
    '''Class for ice cream objects'''

    def __init__(self, image, pos, border, accMode, friction, keys):
        '''
        Initializes a Cone object

        Parameters
        ----------
        image : Surface
            Image of the cone sprite
        pos : tuple
            Position of the cone sprite
        border : tuple
            X range boundaries within which the cone sprite moves
        accMode : float
            Acceleration mode of the cone sprite
        friction : float
            Friction coefficient of the cone sprite
        keys : int
            Index of the keys used for controlling the cone sprite
            
        Returns
        -------
        None
        '''

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
        '''
        Draws the cone sprite on a surface

        Parameters
        ----------
        surfaceIn : Surface
            Surface to draw the cone sprite on

        Returns
        -------
        None
        '''

        surfaceIn.blit(self.image, self.rect)
    
    def update(self, creamDisplacement):
        '''
        Updates the position and behavior of the cone sprite

        Parameters
        ----------
        creamDisplacement : int
            Y Displacement of the ice cream sprite

        Returns
        -------
        None
        '''

        self.acc = vec(0, 0)

        pressed_keys = pygame.key.get_pressed()

        # Based on what keys are chosen, looks through a 2D array to go up, left, down, right
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

        # X range boundaries
        if self.pos.x > self.border[1]:
            self.pos.x = self.border[1]
            self.vel = vec(0, 0)
        if self.pos.x < self.border[0]:
            self.pos.x = self.border[0]
            self.vel = vec(0, 0)
        # Y range boundaries
        if self.pos.y > 540 + creamDisplacement:
            self.pos.y = 540 + creamDisplacement
        if self.pos.y < (540/4)*3 + self.rect[3]/2:
            self.pos.y = (540/4)*3 + self.rect[3]/2

        self.rect.center = self.pos