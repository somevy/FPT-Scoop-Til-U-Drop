#-----------------------------------------------------------------------------
# Name:        Scoop Til' U Drop (mainScoop.py)
# Purpose:     The game’s simple, scoop falling ice cream from the sky into your cone, 
#              but be careful of unsuspecting bird poop that might disguise itself as ice cream. 
#              You have one life, scoop wisely and get sprinkle currency!
# Author:      Vicky L
# Created:     08-May-2024
# Updated:     XX-XXXX-XXXX
#-----------------------------------------------------------------------------
# I think this project deserves a level XXXXXX because ...
#
# Features Added:
#   ...
#   ...
#   ...
#-----------------------------------------------------------------------------
import pygame, random, math, os

# Importing classes
from cone import Cone
from iceCream import IceCream

# Taken from Goodgis "Don't Touch My Presents" - https://github.com/Gooodgis/dont-touch-my-presents
def sine(speed: float, time: int, how_far: float, overall_y: int) -> int:
    t = pygame.time.get_ticks() / 2 % time
    y = math.sin(t / speed) * how_far + overall_y
    return int(y)

class Text():
    def __init__(self, fontType, fontSize, pos, color):
        self.font = pygame.font.Font(f"{fontType}.ttf", fontSize)
        self.fontType = fontType
        self.fontSize = fontSize
        self.pos = pos
        self.color = color
    
    def draw(self, surface):
        surface.blit(self.text, self.text_rect)
    
    def update(self, textInput, pos=None, color=None, fontSize=None, posType=None):
        if pos != None:
            self.pos = pos
        if color != None:
            self.color = color
        if fontSize != None:
            self.fontSize = fontSize

        self.font = pygame.font.Font(f"{self.fontType}.ttf", self.fontSize)
        self.text = self.font.render(str(textInput), 1, pygame.Color(self.color))
        if posType == "center":
            self.text_rect = self.text.get_rect(center=self.pos)
        else:
            self.text_rect = self.pos
    
class Button():
        def __init__(self, image, posIn, valueIn=False):
            #Setting initial values

            self.x = posIn[0]
            self.y = posIn[1]
            self.image = image
            self.rect = self.image.get_rect() #Using an image instead of just having solid color
            self.rect.center = posIn
            self.hoverColor = pygame.Color(0,0,0)
            
            self.value = valueIn
            
        def draw(self, surfaceIn):
            surfaceIn.blit(self.image, self.rect)
            
        def collidePoint(self, pointIn):
            #Not necessary, but to make the algorithm easier for ya'll to see
            rectX = self.rect[0]
            rectY = self.rect[1]
            rectWidth = self.rect[2]
            rectHeight = self.rect[3]
            
            xIn = pointIn[0] #Mouse X pointer
            yIn = pointIn[1] #Mouse Y pointer
            
            #Checking if mouse's X is in between left and right side of button, and mouse's Y between bottom and top side of button
            if (xIn > rectX and xIn < rectX + rectWidth and yIn > rectY and yIn < rectY + rectHeight):
                # #Source - https://pixabay.com/sound-effects/button-124476/
                # pygame.mixer.Channel(2).play(pygame.mixer.Sound('sound/button.mp3'), maxtime=600)
                return True
            else:
                return False
            
        def toggleValue(self): #Toggles the boolean as true or false
            self.value = not self.value

def main():
    #-----------------------------Setup------------------------------------------------------#
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    surfaceSize = [960,540]   # Desired physical surface size, in pixels.
    
    clock = pygame.time.Clock()  #Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize))

    #-----------------------------Program Variable Initialization----------------------------#
    # Set up some data to describe a small circle and its color
    
    #Load an image
    sourceFileDir = os.path.dirname(os.path.abspath(__file__))

    coneImgs = [
        pygame.image.load(os.path.join(sourceFileDir, "images", "cones", "cone0.png")),
        pygame.image.load(os.path.join(sourceFileDir, "images", "cones", "cone1.png")),
        pygame.image.load(os.path.join(sourceFileDir, "images", "cones", "cone2.png")),
        pygame.image.load(os.path.join(sourceFileDir, "images", "cones", "cone3.png")),
    ]

    for i in range (0, len(coneImgs)):
        coneImgs[i] = pygame.transform.scale_by(coneImgs[i], 0.58)

    creamImgs = [
        pygame.image.load(os.path.join(sourceFileDir, "images", "cream", "IceCream0.png")),
        pygame.image.load(os.path.join(sourceFileDir, "images", "cream", "IceCream1.png")),
        pygame.image.load(os.path.join(sourceFileDir, "images", "cream", "IceCream2.png")),
        pygame.image.load(os.path.join(sourceFileDir, "images", "cream", "IceCream3.png")),
        pygame.image.load(os.path.join(sourceFileDir, "images", "cream", "IceCream4.png")),
        pygame.image.load(os.path.join(sourceFileDir, "images", "cream", "IceCream5.png")),
    ]

    for i in range (0, len(creamImgs)):
        creamImgs[i] = pygame.transform.scale_by(creamImgs[i], 0.58)

    sprinklesImg = pygame.image.load(os.path.join(sourceFileDir, "images", "sprinkles.png"))
    sprinklesImg = pygame.transform.scale_by(sprinklesImg, 0.58)

    # Button Images
    retryButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "retryButton.png"))
    backButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "backButton.png"))
    infoButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "infoButton.png"))
    playButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "playButton.png"))
    shopButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "shopButton.png"))
    goButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "goButton.png"))

    # Button Mode Images
    lifeOneButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "modes", "1 Life.png"))
    lifeThreeButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "modes", "3 Lives.png"))
    lifeFiveButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "modes", "5 Lives.png"))
    lifeInfButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "modes", "Inf Lives.png"))
    fastButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "modes", "fast.png"))
    slowButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "modes", "slow.png"))
    normalButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "modes", "normal.png"))
    slipperyIButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "modes", "slipperyI.png"))
    slipperyIIButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "modes", "slipperyII.png"))
    slipperyIIIButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "modes", "slipperyIII.png"))
    singleplayerButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "modes", "singleplayer.png"))
    multiplayerButImg = pygame.image.load(os.path.join(sourceFileDir, "images", "buttons", "modes", "multiplayer.png"))

    # Bg Images
    bgBlue = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "bg1.png"))
    bgRed = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "bg2.png"))
    bgGameoever = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "gameover.png"))
    bgP1 = bgBlue
    bgP2 = bgRed
    bgPos1 = [0, 0]
    bgPos2 = [0, surfaceSize[1]]

    darkOverlay = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "darkOverlay.png"))
    gameSelectionOverlay = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "gameSelection.png"))
    scoopTilUDropLogo = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "scoop til' u drop.png"))

    singleplayerOverlay = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "singleplayerOverlay.png"))

    sprinkleCurrency = 0
    currSprinkleCurrency = 0
    multiplier = 0
    iceCreamScore = 0
    sprinkleCreamScore = 0
    countdownNum = 400

    creamP1Displacement = 0
    creamP1Speed = 0
    creamP2Displacement = 0
    creamP2Speed = 0

    livesOne = 1
    livesThree = 3
    livesFive = 5
    livesTen = 10
    livesInf = -1
    livesMode = livesOne
    livesP1 = livesMode
    livesP2 = livesMode
    livesMultiplier = 0

    slipperyI = 1
    slipperyII = 1.2
    slipperyIII = 1.5
    slipperyMode = slipperyII
    slipperyMultiplier = 0

    speedNorm = -0.05
    speedFast = -0.02
    speedSlow = -0.1
    speedMode = speedNorm
    speedMultiplier = 0

    programState = "menu"
    prevMode = "singleplayer"

    # Texts
    scoreText = Text("BaiJamjuree-Bold", 20, (34, 39), "black")
    sprinkleScoreText = Text("BaiJamjuree-Bold", 20, (34, 106), "black")
    livesP1Text = Text("BaiJamjuree-Bold", 20, (920, 42), "white")
    countdownText = Text("Baijamjuree-Bold", 20, (surfaceSize[0]/2, surfaceSize[1]/2), "white")
    currSprinkleCurrencyText = Text("Baijamjuree-Bold", 30, (354, 405), "white")
    multiplierText = Text("Baijamjuree-Bold", 40, (828, 150), "white")
    totalSprinkleCurrencyText = Text("Baijamjuree-Bold", 40, (828, 275), "white")

    # Buttons
    retryButton = Button(retryButImg, (surfaceSize[0] - 122, surfaceSize[1] - 60))
    backButton = Button(backButImg, (122, surfaceSize[1] - 60))
    playButton = Button(playButImg, (surfaceSize[0]/2, 295))
    infoButton = Button(infoButImg, (surfaceSize[0]/2, 295 + 95))
    shopButton = Button(shopButImg, (surfaceSize[0]/2, 295 + 190))

    # Game Selection Buttons
    goModeButton = Button(goButImg, (surfaceSize[0] - 122, surfaceSize[1] - 60))
    lifeOneButton = Button(lifeOneButImg, (143, 233))
    lifeThreeButton = Button(lifeThreeButImg, (143, 233 + 44))
    lifeFiveButton = Button(lifeFiveButImg, (143, 233 + 44*2))
    lifeInfButton = Button(lifeInfButImg, (143, 233 + 44*3))
    normalButton = Button(normalButImg, (143 + 226, 238))
    fastButton = Button(fastButImg, (143 + 226, 238 + 63))
    slowButton = Button(slowButImg, (143 + 226, 238 + 63 + 63))
    slipperyIButton = Button(slipperyIButImg, (140 + 226*2, 238))
    slipperyIIButton = Button(slipperyIIButImg, (140 + 226*2, 238 + 63))
    slipperyIIIButton = Button(slipperyIIIButImg, (140 + 226*2, 238 + 63 + 63))
    singleplayerButton = Button(singleplayerButImg, (137 + 226*3, 238))
    multiplayerButton = Button(multiplayerButImg, (137 + 226*3, 238 + 67))

    gameModeButtons = [goModeButton, lifeOneButton, lifeThreeButton, lifeFiveButton, lifeInfButton, normalButton, fastButton, slowButton, slipperyIButton, slipperyIIButton, slipperyIIIButton, multiplayerButton, singleplayerButton]

    coneP1 = Cone(coneImgs[0], [surfaceSize[0]/2, 400], 0, surfaceSize[0], "p1", slipperyMode, speedMode)
    creamsP1 = pygame.sprite.Group()
    creamP1 = IceCream(creamImgs, sprinklesImg, [random.randint(0, 960), -2000], coneP1, creamP1Displacement, creamP1Speed, 0, surfaceSize[0], livesP1)
    creamsP1.add(creamP1)

    coneP2 = Cone(coneImgs[1], [(surfaceSize[0]/4)*3, 400], surfaceSize[0]/2, surfaceSize[0], "p2", slipperyMode, speedMode)
    creamsP2 = pygame.sprite.Group()
    creamP2 = IceCream(creamImgs, sprinklesImg, [random.randint((surfaceSize[0]/2) + 60, surfaceSize[0]), -2000], coneP2, creamP2Displacement, creamP2Speed, surfaceSize[0]/2 + 60, surfaceSize[0], livesP2)
    creamsP2.add(creamP2)

    def scrollingBg(bgImg, mode=None):
        if mode == "multiplayer":
            mainSurface.blit(bgImg, (-surfaceSize[0]/2, bgPos1[1]))
            mainSurface.blit(bgImg, (-surfaceSize[0]/2, bgPos2[1]))
            mainSurface.blit(bgP2, (surfaceSize[0]/2, bgPos1[1]))
            mainSurface.blit(bgP2, (surfaceSize[0]/2, bgPos2[1]))
        else:
            mainSurface.blit(bgImg, bgPos1)
            mainSurface.blit(bgImg, bgPos2)

        if bgPos1[1] <= -surfaceSize[1]:
            bgPos1[1] = surfaceSize[1]
        if bgPos2[1] <= -surfaceSize[1]:
            bgPos2[1] = surfaceSize[1]
        
        bgPos1[1] -= 0.7
        bgPos2[1] -= 0.7
    
    # def resetSingleplayer():
    #     scoreText.update(iceCreamScore, (34, 39), "black", 20)
    #     sprinkleScoreText.update(sprinkleCreamScore, (34, 106), "black", 20)
    #     livesP1 = livesMode
    #     creamP1Displacement = 0
    #     creamP1Speed = 0
    #     coneP1 = Cone(coneImgs[0], [surfaceSize[0]/2, 400], 0, surfaceSize[0], "p1", slipperyMode, speedMode)
    #     creamsP1 = pygame.sprite.Group()
    #     creamP1 = IceCream(creamImgs, sprinklesImg, [random.randint(0, 960), -2000], coneP1, creamP1Displacement, creamP1Speed, 0, surfaceSize[0], livesP1)
    #     creamsP1.add(creamP1)

    # def resetMultiplayer():
    #     # Setting up for player 1
    #     creamP1Displacement = 0
    #     creamP1Speed = 0
    #     coneP1 = Cone(coneImgs[0], [surfaceSize[0]/4, 400], 0, surfaceSize[0]/2, "p1", slipperyMode, speedMode)
    #     creamsP1 = pygame.sprite.Group()
    #     creamP1 = IceCream(creamImgs, sprinklesImg, [random.randint(0, surfaceSize[0]/2 - 60), -2000], coneP1, creamP1Displacement, creamP1Speed, 0, surfaceSize[0]/2 - 60, livesP1)
    #     creamsP1.add(creamP1)

    #     # Setting up for player 2
    #     creamP2Displacement = 0
    #     creamP2Speed = 0
    #     coneP2 = Cone(coneImgs[1], [(surfaceSize[0]/4)*3, 400], surfaceSize[0]/2, surfaceSize[0], "p2", slipperyMode, speedMode)
    #     creamsP2 = pygame.sprite.Group()
    #     creamP2 = IceCream(creamImgs, sprinklesImg, [random.randint((surfaceSize[0]/2) + 60, surfaceSize[0]), -2000], coneP2, creamP2Displacement, creamP2Speed, surfaceSize[0]/2 + 60, surfaceSize[0], livesP2)
    #     creamsP2.add(creamP2)

    #-----------------------------Main Program Loop---------------------------------------------#
    while True:       
        # print(f"BGpos1: {bgPos1}    BGpos2: {bgPos2}")
        #-----------------------------Event Handling-----------------------------------------#
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop

        if programState == "menu":
            scrollingBg(bgP1)
            mainSurface.blit(darkOverlay, (0,0))
            playButton.draw(mainSurface)
            infoButton.draw(mainSurface)
            shopButton.draw(mainSurface)

            mainSurface.blit(scoopTilUDropLogo, (310, sine(200.0, 1280, 10.0, 50)))
            

            if ev.type == pygame.MOUSEBUTTONUP:
                if playButton.collidePoint(pygame.mouse.get_pos()): #mode selection
                    programState = "mode selection"
                if infoButton.collidePoint(pygame.mouse.get_pos()): #info state
                    programState = "info"
                if shopButton.collidePoint(pygame.mouse.get_pos()): #shop state
                    programState = "shop"
        
        if programState == "mode selection":
            scrollingBg(bgP1)
            mainSurface.blit(gameSelectionOverlay, (0,0))
            backButton.draw(mainSurface)

            for button in gameModeButtons:
                button.draw(mainSurface)

            if livesMode == livesInf:
                multiplier = 0
            else:
                multiplier = livesMultiplier + speedMultiplier + slipperyMultiplier
            
            multiplierText.update(f"x {1 + multiplier}", (500, 450))
            multiplierText.draw(mainSurface)

            if ev.type == pygame.MOUSEBUTTONUP:
                if backButton.collidePoint(pygame.mouse.get_pos()): #Back button to menu state
                    programState = "menu"

                if goModeButton.collidePoint(pygame.mouse.get_pos()):
                    iceCreamScore = 0
                    sprinkleCreamScore = 0
                    sprinkleCurrency += currSprinkleCurrency
                    if prevMode == "singleplayer":
                        scoreText.update(iceCreamScore, (34, 39), "black", 20)
                        sprinkleScoreText.update(sprinkleCreamScore, (34, 106), "black", 20)
                        livesP1 = livesMode
                        creamP1Displacement = 0
                        creamP1Speed = 0
                        coneP1 = Cone(coneImgs[0], [surfaceSize[0]/2, 400], 0, surfaceSize[0], "p1", slipperyMode, speedMode)
                        creamsP1 = pygame.sprite.Group()
                        creamP1 = IceCream(creamImgs, sprinklesImg, [random.randint(0, 960), -2000], coneP1, creamP1Displacement, creamP1Speed, 0, surfaceSize[0], livesP1)
                        creamsP1.add(creamP1)
                        programState = "singleplayer"

                    elif prevMode == "multiplayer":
                        # Setting up for player 1
                        livesP1 = livesMode
                        creamP1Displacement = 0
                        creamP1Speed = 0
                        coneP1 = Cone(coneImgs[0], [surfaceSize[0]/4, 400], 0, surfaceSize[0]/2, "p1", slipperyMode, speedMode)
                        creamsP1 = pygame.sprite.Group()
                        creamP1 = IceCream(creamImgs, sprinklesImg, [random.randint(0, surfaceSize[0]/2 - 60), -2000], coneP1, creamP1Displacement, creamP1Speed, 0, surfaceSize[0]/2 - 60, livesP1)
                        creamsP1.add(creamP1)

                        # Setting up for player 2
                        livesP2 = livesMode
                        creamP2Displacement = 0
                        creamP2Speed = 0
                        coneP2 = Cone(coneImgs[1], [(surfaceSize[0]/4)*3, 400], surfaceSize[0]/2, surfaceSize[0], "p2", slipperyMode, speedMode)
                        creamsP2 = pygame.sprite.Group()
                        creamP2 = IceCream(creamImgs, sprinklesImg, [random.randint((surfaceSize[0]/2) + 60, surfaceSize[0]), -2000], coneP2, creamP2Displacement, creamP2Speed, surfaceSize[0]/2 + 60, surfaceSize[0], livesP2)
                        creamsP2.add(creamP2)
                        programState = "multiplayer"

                # Game Modes:
                # Players
                if singleplayerButton.collidePoint(pygame.mouse.get_pos()):
                    prevMode = "singleplayer"
                if multiplayerButton.collidePoint(pygame.mouse.get_pos()):
                    prevMode = "multiplayer"
                
                # Lives
                if lifeOneButton.collidePoint(pygame.mouse.get_pos()):
                    livesMode = livesOne
                    livesMultiplier = 0.2
                if lifeThreeButton.collidePoint(pygame.mouse.get_pos()):
                    livesMode = livesThree
                    livesMultiplier = 0
                if lifeFiveButton.collidePoint(pygame.mouse.get_pos()):
                    livesMode = livesFive
                    livesMultiplier = -0.2
                if lifeInfButton.collidePoint(pygame.mouse.get_pos()):
                    livesMode = livesInf          

                # Speed
                if normalButton.collidePoint(pygame.mouse.get_pos()):
                    speedMode = speedNorm
                    speedMultiplier = 0
                if fastButton.collidePoint(pygame.mouse.get_pos()):
                    speedMode = speedFast
                    speedMultiplier = 0.2
                if slowButton.collidePoint(pygame.mouse.get_pos()):
                    speedMode = speedSlow
                    speedMultiplier = 0.2
                
                # Slippery
                if slipperyIButton.collidePoint(pygame.mouse.get_pos()):
                    slipperyMode = slipperyI
                    slipperyMultiplier = 0.2
                if slipperyIIButton.collidePoint(pygame.mouse.get_pos()):
                    slipperyMode = slipperyII
                    slipperyMultiplier = 0
                if slipperyIIIButton.collidePoint(pygame.mouse.get_pos()):
                    slipperyMode = slipperyIII
                    slipperyMultiplier = 0.2


        if programState == "info":
            scrollingBg(bgP1)
            backButton.draw(mainSurface)
            if ev.type == pygame.MOUSEBUTTONUP:
                if backButton.collidePoint(pygame.mouse.get_pos()): #Back button to menu state
                    programState = "menu"
        
        if programState == "shop":
            scrollingBg(bgP1)
            backButton.draw(mainSurface)
            if ev.type == pygame.MOUSEBUTTONUP:
                if backButton.collidePoint(pygame.mouse.get_pos()): #Back button to menu state
                    programState = "menu"

        if programState == "singleplayer":
        #-----------------------------Program Logic---------------------------------------------#
        # Update your game objects and data structures here...


        #-----------------------------Drawing Everything-------------------------------------#
        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
            scrollingBg(bgP1)

            if int(countdownNum/100) != 0:
                countdownNum -= 1
                countdownText.update(f"Ready in: {int(countdownNum/100)}", None, None, 40, "center")
                countdownText.draw(mainSurface)
                
            coneP1.draw(mainSurface)
            coneP1.update(creamP1Displacement)
            for creamP1 in creamsP1:
                creamP1.draw(mainSurface)
                creamP1.update()

            livesP1 = creamP1.lives
            if creamP1.is_collided_with():
                if creamP1.sprinkleCream:
                    sprinkleCreamScore += 1
                else:
                    iceCreamScore += 1
                creamP1Displacement += 50
                creamP1Speed += 0.025
                print("Collision detected")
                creamP1 = IceCream(creamImgs, sprinklesImg, [random.randint(0, 960), -100], coneP1, creamP1Displacement, creamP1Speed, 0, surfaceSize[0], livesP1)
                creamsP1.add(creamP1)

                scoreText.update(iceCreamScore)
                sprinkleScoreText.update(sprinkleCreamScore)
            # print(creamP1Displacement)

            mainSurface.blit(singleplayerOverlay, (0, 0))

            if livesMode == livesInf:
                livesP1Text.update("")
            else:
                livesP1Text.update(livesP1, None, None, None, "center")

            scoreText.draw(mainSurface)
            sprinkleScoreText.draw(mainSurface)
            livesP1Text.draw(mainSurface)


            if creamP1.gameOver == True:
                programState = "game over"

        if programState == "multiplayer":
            if creamP1.gameOver == True and creamP2.gameOver == True:
                programState = "game over"

            scrollingBg(bgP1, "multiplayer", creamP1.gameOver, creamP2.gameOver)

            coneP1.draw(mainSurface)
            coneP1.update(creamP1Displacement)

            for creamP1 in creamsP1:
                creamP1.draw(mainSurface)
                creamP1.update()
            
            if creamP1.is_collided_with():
                iceCreamScore += 1
                creamP1Displacement += 50
                creamP1Speed += 0.015
                print("Collision detected")
                creamP1 = IceCream(creamImgs, sprinklesImg, [random.randint(0, surfaceSize[0]/2 - 50) , -100], coneP1, creamP1Displacement, creamP1Speed, 0, surfaceSize[0]/2, livesP1)
                creamsP1.add(creamP1)

            coneP2.draw(mainSurface)
            coneP2.update(creamP2Displacement)

            for creamP2 in creamsP2:
                creamP2.draw(mainSurface)
                creamP2.update()

            # print(creamP1Displacement)
            
            if creamP2.is_collided_with():
                iceCreamScore += 1
                creamP2Displacement += 50
                creamP2Speed += 0.015
                print("Collision detected")
                creamP2 = IceCream(creamImgs, sprinklesImg, [random.randint((surfaceSize[0]/2) + 50, surfaceSize[0]), -100], coneP2, creamP2Displacement, creamP2Speed, surfaceSize[0]/2, surfaceSize[0], livesP2)
                creamsP2.add(creamP2)
            scoreText.update(f"Score: {iceCreamScore}")
            scoreText.draw(mainSurface)
            
            pygame.draw.line(mainSurface, "light blue", (0, (540/4)*3), (960, (540/4)*3), width = 2)
            pygame.draw.line(mainSurface, "light blue", (surfaceSize[0]/2, (540/4)*3), (surfaceSize[0]/2, surfaceSize[1]), width = 2)
        
        if programState == "game over":
            scrollingBg(bgP1)
            currSprinkleCurrency = int(iceCreamScore + 3*sprinkleCreamScore)*(1 + multiplier)

            mainSurface.blit(bgGameoever, (0,0))

            scoreText.update(iceCreamScore, (354, 246), "white", 30)
            scoreText.draw(mainSurface)

            sprinkleScoreText.update(sprinkleCreamScore, (574, 246), "white", 30)
            sprinkleScoreText.draw(mainSurface)

            currSprinkleCurrencyText.update(int(iceCreamScore + 3*sprinkleCreamScore)*(1 + multiplier))
            currSprinkleCurrencyText.draw(mainSurface)

            multiplierText.update(f"x {1 + multiplier}", (828, 150), None, None, "center")
            multiplierText.draw(mainSurface)

            totalSprinkleCurrencyText.update(sprinkleCurrency + currSprinkleCurrency, None, None, None, "center")
            totalSprinkleCurrencyText.draw(mainSurface)

            retryButton.draw(mainSurface)
            backButton.draw(mainSurface)

            if ev.type == pygame.MOUSEBUTTONUP:
                countdownNum = 400
                if backButton.collidePoint(pygame.mouse.get_pos()): #Back button to menu state
                    iceCreamScore = 0
                    sprinkleCreamScore = 0
                    sprinkleCurrency += currSprinkleCurrency
                    programState = "menu"

                    for creamP1 in creamsP1:
                        creamP1.kill()
                    if prevMode == "multiplayer":
                        for creamP2 in creamsP2:
                            creamP2.kill()

                if retryButton.collidePoint(pygame.mouse.get_pos()):
                    iceCreamScore = 0
                    sprinkleCreamScore = 0
                    sprinkleCurrency += currSprinkleCurrency
                    if prevMode == "singleplayer":
                        scoreText.update(iceCreamScore, (34, 39), "black", 20)
                        sprinkleScoreText.update(sprinkleCreamScore, (34, 106), "black", 20)
                        livesP1 = livesMode
                        creamP1Displacement = 0
                        creamP1Speed = 0
                        coneP1 = Cone(coneImgs[0], [surfaceSize[0]/2, 400], 0, surfaceSize[0], "p1", slipperyMode, speedMode)
                        creamsP1 = pygame.sprite.Group()
                        creamP1 = IceCream(creamImgs, sprinklesImg, [random.randint(0, 960), -2000], coneP1, creamP1Displacement, creamP1Speed, 0, surfaceSize[0], livesP1)
                        creamsP1.add(creamP1)
                        programState = "singleplayer"

                    elif prevMode == "multiplayer":
                        # Setting up for player 1
                        livesP1 = livesMode
                        creamP1Displacement = 0
                        creamP1Speed = 0
                        coneP1 = Cone(coneImgs[0], [surfaceSize[0]/4, 400], 0, surfaceSize[0]/2, "p1", slipperyMode, speedMode)
                        creamsP1 = pygame.sprite.Group()
                        creamP1 = IceCream(creamImgs, sprinklesImg, [random.randint(0, surfaceSize[0]/2 - 60), -2000], coneP1, creamP1Displacement, creamP1Speed, 0, surfaceSize[0]/2 - 60, livesP1)
                        creamsP1.add(creamP1)

                        # Setting up for player 2
                        livesP2 = livesMode
                        creamP2Displacement = 0
                        creamP2Speed = 0
                        coneP2 = Cone(coneImgs[1], [(surfaceSize[0]/4)*3, 400], surfaceSize[0]/2, surfaceSize[0], "p2", slipperyMode, speedMode)
                        creamsP2 = pygame.sprite.Group()
                        creamP2 = IceCream(creamImgs, sprinklesImg, [random.randint((surfaceSize[0]/2) + 60, surfaceSize[0]), -2000], coneP2, creamP2Displacement, creamP2Speed, surfaceSize[0]/2 + 60, surfaceSize[0], livesP2)
                        creamsP2.add(creamP2)
                        programState = "multiplayer"

        pygame.display.flip()
        
        clock.tick(60) #Force frame rate to be slower


    pygame.quit()     # Once we leave the loop, close the window.

main()