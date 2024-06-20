import pygame
import random
from pygame.locals import *
vec = pygame.math.Vector2

# Movement code taken from Goodgis "Don't Touch My Presents" - https://github.com/Gooodgis/dont-touch-my-presents/

class IceCream(pygame.sprite.Sprite):
    '''Class for ice cream objects'''

    def __init__(self, imageList, skin, sprinkleImg, pos, cone, yDisplacement, ySpeed, border, lives):
        '''
        Initializes an IceCream object

        Parameters
        ----------
        imageList : list
            List of ice cream images
        skin : int
            Index of the current ice cream skin
        sprinkleImg : Surface
            Image of sprinkles to add to the ice cream
        pos : list
            Position of the ice cream sprite
        cone : Cone
            Cone object
        yDisplacement : int
            Vertical displacement of the ice cream sprite
        ySpeed : float
            Vertical speed of the ice cream sprite
        border : tuple
            X range boundaries within which the ice cream sprite moves
        lives : int
            Remaining lives of the player
            
        Returns
        -------
        None
        '''
 
        pygame.sprite.Sprite.__init__(self)
        self.imageList = imageList
        self.skin = skin
        self.imageNum = random.randint(0, len(imageList[skin])-1)
        self.image = imageList[skin][self.imageNum]
        self.pos = pos
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.falling = True
        self.cone = cone
        self.birdPoop = False
        self.sprinkleCream = False
        self.yDisplacement, self.ySpeed = yDisplacement, ySpeed
        self.border = border
        self.gameOver = False
        self.lives = lives

        # Picks a random number between 0 and 10, if 1 gets chosen the ice cream has sprinkles and is worth 3x more
        if random.randint(0, 10) == 1:
            self.sprinkleCream = True
            # New image of the ice cream will have sprinkles on it
            self.image = self.image.copy()
            self.image.blit(sprinkleImg, (10, 20))
            
    def draw(self, surfaceIn):
        '''
        Draws the ice cream sprite on a surface

        Parameters
        ----------
        surfaceIn : Surface
            Surface to draw the ice cream sprite on

        Returns
        -------
        None
        '''

        surfaceIn.blit(self.image, self.rect)
    
    def update(self):
        '''
        Updates ice cream

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''

        # If the imageNum, otherwise known as the index of the imgList, is 5, toggle birdPoop as True
        if self.imageNum == 5:
            self.birdPoop = True
        else:
            self.birdPoop = False                

        # While it is falling, update y position to keep falling
        if self.falling:
            self.acc = vec(0, 0)
            self.acc.y = 1.0
            if self.birdPoop:
                # Makes bird poop go faster than regular ice cream
                self.acc.y += self.vel.y * - 0.10 + self.ySpeed
                if self.rect.top > 540:
                    # When bird poop falls below the screen, it will rebrand itself as a new ice cream
                    self.imageNum = random.randint(0, len(self.imageList[self.skin])-1)
                    self.image = self.imageList[self.skin][self.imageNum]
                    self.pos = [random.randint(self.border[0], self.border[1]) , -100]                    
            else:
                # Falling speed
                self.acc.y += self.vel.y * - 0.15 + self.ySpeed

                if self.rect.top > 540:
                    # When normal ice cream falls below the screen, based on the initial lives it will decrease by 1
                    # As long as user is still alive, the ice cream will fall again from the sky rebranded as a new ice cream
                    if self.lives != 1:
                        self.lives -= 1
                        self.imageNum = random.randint(0, len(self.imageList[self.skin])-1)
                        self.image = self.imageList[self.skin][self.imageNum]
                        self.pos = [random.randint(self.border[0], self.border[1]) , -100]    
                    else:
                        self.gameOver = True

            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
            self.rect.center = self.pos
                    
        else:
            # X and Y positions of the ice cream will correlate with the cone's X and Y
            self.pos.y = self.cone.pos.y - self.cone.rect.height - self.yDisplacement
            self.pos.x += self.cone.vel.x + 0.5 * self.cone.acc.x

            # Ice cream will stay within the borders
            if self.pos.x > self.border[1]:
                self.pos.x = self.border[1]
            if self.pos.x < self.border[0]:
                self.pos.x = self.border[0]

            self.rect.center = self.pos
    
    def is_collided_with(self) -> bool:
        '''
        Checks if the ice cream sprite collides with the cone

        Parameters
        ----------
        None

        Returns
        -------
        Bool:
            True if the ice cream sprite collides with the cone, False otherwise
        '''

        if self.rect.right <= self.cone.rect.right + 55 and self.rect.left >= self.cone.rect.left - 55:
            # Right side of the ice cream is less than or equal to the right side of the cone
            if self.rect.bottom <= (self.cone.rect.top + 40 - self.yDisplacement) and self.rect.bottom >= (self.cone.rect.top - self.yDisplacement): 
                # Bottom of the ice cream within 40px below the top of the cone/cream
                # Bottom of the ice cream is touching or below the top of the cone/cream
                
                if self.birdPoop:
                    # If birdpoop collides with the cone, instant gameover :(
                    self.falling = False
                    self.gameOver = True

                else:
                    # Stops the ice cream from falling off the screen after colliding with cone
                    self.falling = False
                    return True