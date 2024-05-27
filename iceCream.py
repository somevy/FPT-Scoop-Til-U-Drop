import pygame
import random
from pygame.locals import *
vec = pygame.math.Vector2

class IceCream(pygame.sprite.Sprite):
    def __init__(self, imageList, sprinkleImg, pos, cone, yDisplacement, ySpeed, leftBorder, rightBorder, lives):
        pygame.sprite.Sprite.__init__(self)
        self.imageList = imageList
        self.imageNum = random.randint(0, len(imageList)-1)
        self.image = imageList[self.imageNum]
        self.pos = pos
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.falling = True
        self.collision = False
        self.cone = cone
        self.birdPoop = False
        self.sprinkleCream = False
        self.yDisplacement, self.ySpeed = yDisplacement, ySpeed
        self.leftBorder, self.rightBorder = leftBorder, rightBorder
        self.gameOver = False
        self.lives = lives

        if random.randint(0, 11) == 1:
            self.sprinkleCream = True

            self.image = self.image.copy()
            self.image.blit(sprinkleImg, (10, 20))
            

    def draw(self, surfaceIn):
        surfaceIn.blit(self.image, self.rect)
    
    def update(self):
        if self.imageNum == 5:
            self.birdPoop = True
        else:
            self.birdPoop = False                

        if self.falling:
            self.acc = vec(0, 0)
            self.acc.y = 1.0
            if self.birdPoop:
                self.acc.y += self.vel.y * - 0.10 + self.ySpeed # Makes bird poop go faster
                if self.rect.top > 540:
                    self.imageNum = random.randint(0, len(self.imageList)-1)
                    self.image = self.imageList[self.imageNum]
                    self.pos = [random.randint(self.leftBorder, self.rightBorder) , -100]                    
            else:
                self.acc.y += self.vel.y * - 0.15 + self.ySpeed
                if self.rect.top > 540:
                    if self.lives != 1:
                        self.lives -= 1
                        self.imageNum = random.randint(0, len(self.imageList)-1)
                        self.image = self.imageList[self.imageNum]
                        self.pos = [random.randint(self.leftBorder, self.rightBorder) , -100]    
                    else:
                        self.gameOver = True

            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
            self.rect.center = self.pos
                    
        else:
            # self.acc = vec(0, 0)

            self.pos.y = self.cone.pos.y - self.cone.rect.height - self.yDisplacement
            self.pos.x += self.cone.vel.x + 0.5 * self.cone.acc.x

            if self.pos.x > self.rightBorder:
                self.pos.x = self.rightBorder
            if self.pos.x < self.leftBorder:
                self.pos.x = self.leftBorder

            self.rect.center = self.pos
    
    def is_collided_with(self):
        if self.rect.right <= self.cone.rect.right + 60 and self.rect.left >= self.cone.rect.left - 60:
            # Right side of the ice cream is less than or equal to the right side of the cone
            if self.rect.bottom <= (self.cone.rect.top + 25 - self.yDisplacement) and self.rect.bottom >= (self.cone.rect.top - self.yDisplacement): 
                # Bottom of the ice cream within 25 pxls below the top of the cone/cream
                # Bottom of the ice cream within the top of the cone/cream
                print("y is in range")
                if self.birdPoop:
                    self.falling = False
                    self.gameOver = True

                else:
                    self.falling = False
                    self.collision = True
                    return True