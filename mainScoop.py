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
import pygame, random, math, os, json
from pygame.locals import *

# Importing classes
from cone import Cone
from iceCream import IceCream


# Taken from Goodgis "Don't Touch My Presents" - https://github.com/Gooodgis/dont-touch-my-presents/blob/main/src/utils/tools.py
def sine(speed: float, time: int, how_far: float, overall_y: int) -> int:
    t = pygame.time.get_ticks() / 2 % time
    y = math.sin(t / speed) * how_far + overall_y
    return int(y)

class Text():
    def __init__(self, fontType, fontSize, pos, color, posType=None):
        self.font = pygame.font.Font(f"{fontType}.ttf", fontSize)
        self.fontType = fontType
        self.fontSize = fontSize
        self.pos = pos
        self.color = color
        self.postType = posType
    
    def draw(self, surface):
        surface.blit(self.text, self.text_rect)
    
    def update(self, textInput, pos=None, color=None, fontSize=None, posType=None):
        self.posType = posType
        if pos != None:
            self.pos = pos
        if color != None:
            self.color = color
        if fontSize != None:
            self.fontSize = fontSize

        self.font = pygame.font.Font(f"{self.fontType}.ttf", self.fontSize)
        self.text = self.font.render(str(textInput), 1, pygame.Color(self.color))
        if self.posType == "center":
            self.text_rect = self.text.get_rect(center=self.pos)
        else:
            self.text_rect = self.pos
    
class Button():
        def __init__(self, image, posIn, valueIn=False):
            #Setting initial values

            self.x = posIn[0]
            self.y = posIn[1]
            self.image = pygame.image.load(f"images/buttons/{image}.png").convert_alpha()
            self.rect = self.image.get_rect() #Using an image instead of just having solid color
            self.rect.center = posIn
            self.darkImg = self.image.copy()
            self.darkImg.fill((255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_MULT)
            
            self.value = valueIn
            
        def draw(self, surfaceIn, gameMode=None, mode=False):
            if gameMode == mode:
                surfaceIn.blit(self.darkImg, self.rect)
            else:
                surfaceIn.blit(self.image, self.rect)
        
        def update(self, pos):
            self.x = pos[0]
            self.y = pos[1]
            self.rect.center = pos

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
                # Source - https://youtu.be/9wiI5iio-fc?si=7fIT7lOZ9zC933Nf
                # Button SFX
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("audio/button.mp3"), maxtime=1000)
                return True
            else:
                return False
            
        def toggleValue(self): #Toggles the boolean as true or false
            self.value = not self.value

def main():
    #-----------------------------Setup------------------------------------------------------#
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    pygame.mixer.init() # Music pygame module
    surfaceSize = [960,540]   # Desired physical surface size, in pixels.
    
    clock = pygame.time.Clock()  #Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize))
    pygame.display.set_caption("Scoop Til' U Drop!")
    
    #-----------------------------Program Variable Initialization----------------------------#
    # Set up some data to describe a small circle and its color
    
    # Loading sound
    # Source - https://www.youtube.com/watch?v=S505bwxigRY 
    # Rustboro City (Pokemon Omega Ruby & Alpha Sapphire) by Chippy Bits
    mainAudio = pygame.mixer.Sound("audio/main.mp3")

    # Source - https://www.youtube.com/watch?v=eXH_-Ys3AUs
    # theme of a shop that sells things you dont want by Azali
    shopAudio = pygame.mixer.Sound("audio/shop.mp3")

    # Source - https://youtu.be/v9kuoBl85oY?si=qmLTjcXX5APwwn3O
    # Battle! - Put Some Love Into It by Pedro Silva
    game0Audio = pygame.mixer.Sound("audio/game0.mp3")

    # Source - https://youtu.be/dGF7HN1LL68?si=tGGBP4BgsSreWABx
    # Battle! - Greens by Pedro Silva
    game1Audio = pygame.mixer.Sound("audio/game1.mp3")

    pygame.mixer.Channel(0).play(mainAudio, -1) # Plays the song infinitely

    #Load an image
    sourceFileDir = os.path.dirname(os.path.abspath(__file__))

    iconImg = pygame.image.load(os.path.join(sourceFileDir, "images/cream/creamSkin1", "IceCream10.png"))
    pygame.display.set_icon(iconImg)

    coneImgs = []

    for i in range(0, 7):
        coneImgs.append(pygame.image.load(os.path.join(sourceFileDir, "images", "cones", f"cone{i}.png")))
        coneImgs[i] = pygame.transform.scale_by(coneImgs[i], 0.58).convert_alpha()

    # creamImgs = [skin pack #][cream #]
    # Skin packs
    # 0 - Default 
    # 1 - Rainbow
    # 2 - Red
    # 3 - Green
    # 4 - Blue
    # 5 - Purple
    # 6 - Oreo

    creamImgs = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]

    for i in range (len(creamImgs)):
        for j in range (len(creamImgs[i])):
            creamImgs[i][j] = pygame.image.load(os.path.join(sourceFileDir, "images", "cream", f"creamSkin{i}", f"IceCream{i}{j}.png"))
            creamImgs[i][j] = pygame.transform.scale_by(creamImgs[i][j], 0.58).convert_alpha()

    itemCreamImgs = []
    for i in range (0, 7):
        itemCreamImgs.append(pygame.image.load(os.path.join(sourceFileDir, "images", "inventory/creams", f"IceCream{i}.png")))

    itemConeImgs = []
    for i in range (0, 7):
        itemConeImgs.append(pygame.image.load(os.path.join(sourceFileDir, "images", "inventory/cones", f"cone{i}.png")))

    itemBgImgs = []
    for i in range (0, 9):
        itemBgImgs.append(pygame.image.load(os.path.join(sourceFileDir, "images", "inventory/backgrounds", f"bg{i}.png")))

    # Inventory 2D Array Format
    # 0 - Ice Cream Skins, default skin pack = 0
    # 1 - Cone Skins, default skin packs = 0 , 1
    # 2 - Background Skins, default bg skins = 0, 1
    
    data = {
        "inventory": [[0], [0, 1], [0, 1]],
        "sprinkleCurrency": 0,
        "highscore": 0,
        "P1 ice cream": 0,
        "P1 cone": 0,
        "P1 bg": 0,
        "P2 ice cream": 0,
        "P2 cone": 1,
        "P2 bg": 1
        }
    
    try:
        with open('data.json') as load_file:
            data = json.load(load_file)
    except:
        with open('data.json','w') as store_file:
            json.dump(data,store_file)

    inventory = data.get("inventory")
    sprinkleCurrency = data.get("sprinkleCurrency")
    highscore = data.get("highscore")

    creamSkinP1 = data.get("P1 ice cream")
    creamSkinP2 = data.get("P2 ice cream")

    coneSkinP1 = data.get("P1 cone")
    coneSkinP2 = data.get("P2 cone")

    bgP1 = data.get("P1 bg")
    bgP2 = data.get("P2 bg")

    sprinklesImg = pygame.image.load(os.path.join(sourceFileDir, "images", "sprinkles.png"))
    sprinklesImg = pygame.transform.scale_by(sprinklesImg, 0.58).convert_alpha()

    # Bg Images
    bgImgs = []
    for i in range(0, 9):
        bgImgs.append(pygame.image.load(os.path.join(sourceFileDir, "images", "bg", f"bg{i}.png")).convert_alpha())

    bgGameOver = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "gameover.png")).convert_alpha()
    bgGameOverMulti = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "gameoverMulti.png")).convert_alpha()

    bgPos1 = [0, 0]
    bgPos2 = [0, surfaceSize[1]]

    darkOverlay = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "darkOverlay.png")).convert_alpha()
    scoopTilUDropLogo = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "scoop til' u drop.png")).convert_alpha()
    gameSelectionOverlay = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "gameSelection.png")).convert_alpha()

    # Info
    infoOverlay = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "info.png")).convert_alpha()
    p1Img = pygame.image.load(os.path.join(sourceFileDir, "images", "info", "player1.png")).convert_alpha()
    p2Img = pygame.image.load(os.path.join(sourceFileDir, "images", "info", "player2.png")).convert_alpha()
    keyImgs = [pygame.image.load(os.path.join(sourceFileDir, "images", "info", "WASD.png")).convert_alpha(),
               pygame.image.load(os.path.join(sourceFileDir, "images", "info", "ARROWS.png")).convert_alpha(),
               pygame.image.load(os.path.join(sourceFileDir, "images", "info", "IJKL.png")).convert_alpha(),]
    p1Keys = 0 # Default keyboard settings set to WASD
    p2Keys = 1 # Default keyboard settings set to Arrow keys

    # Shop
    shopOverlay = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "shop.png")).convert_alpha()
    shopCreamOverlay = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "iceCreamBanner.png")).convert_alpha()
    shopConeOverlay = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "conesBanner.png")).convert_alpha()
    shopBackgroundsOverlay = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "backgroundBanner.png")).convert_alpha()
    inventoryOverlay = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "inventory.png")).convert_alpha()
    errorOverlay = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "errorOverlay.png")).convert_alpha()
    checkOverlay = pygame.image.load(os.path.join(sourceFileDir, "images", "inventory", "check.png")).convert_alpha()
    boxImg = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "box.png")).convert_alpha()
    boxOpenImg = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "boxOpen.png")).convert_alpha()

    # Gameplay
    singleplayerOverlay = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "singleplayerOverlay.png")).convert_alpha()
    multiplayerOverlay = pygame.image.load(os.path.join(sourceFileDir, "images", "bg", "multiplayerOverlay.png")).convert_alpha()

    currSprinkleCurrency = 0
    currSprinkleCurrencyP1 = 0
    currSprinkleCurrencyP2 = 0
    iceCreamScoreP1 = 0
    iceCreamScoreP2 = 0
    sprinkleCreamScoreP1 = 0
    sprinkleCreamScoreP2 = 0
    priceVal = 0
    priceError = False # If user tries to buy in the shop with insufficient funding, it will trigger to True
    boughtScene = "none"
    countdownNum = 400
    creamSpeed = 0.015
    sound = True

    creamP1Displacement = 0
    creamP1Speed = 0
    borderP1 = [0, surfaceSize[0]]

    creamP2Displacement = 0
    creamP2Speed = 0
    borderP2 = [surfaceSize[0]/2 + 50, surfaceSize[0]]

    lives = [1, 3, 5, -1]
    livesMode = lives[0]
    livesP1 = livesMode
    livesP2 = livesMode
    livesMultiplier = 0
    infMultiplier = 1

    speed = [-0.02, -0.05, -0.1]
    speedMode = speed[0]
    speedMultiplier = 0

    slippery = [0.7, 1.2, 1.8]
    slipperyMode = slippery[0]
    slipperyMultiplier = 0

    modes = [[1, 3, 5, -1], [-0.02, -0.05, -0.1], [0.7, 1.2, 1.8]]
    userSelectedModes = [livesMode, speedMode, slipperyMode]

    shopStates = ["ice cream", "cones", "backgrounds"]
    programState = "menu"
    infoPlayer = "p1"
    shopState = shopStates[0]
    inventoryState = shopStates[0]
    inventoryPlayer = "p1"
    prevMode = "singleplayer"

    # Texts
    scoreP1Text = Text("BaiJamjuree-Bold", 20, (34, 39), "black")
    sprinkleScoreP1Text = Text("BaiJamjuree-Bold", 20, (34, 106), "black")
    scoreP2Text = Text("BaiJamjuree-Bold", 20, (surfaceSize[0]/2+38, 32), "black", "center")
    sprinkleScoreP2text = Text("BaiJamjuree-Bold", 20, (surfaceSize[0]/2+38, 95), "black", "center")
    livesP1Text = Text("BaiJamjuree-Bold", 20, (920, 42), "white")
    livesP2Text = Text("BaiJamjuree-Bold", 20, (913, 32), "white", "center")
    countdownText = Text("Baijamjuree-Bold", 20, (surfaceSize[0]/2, surfaceSize[1]/2), "white")
    currSprinkleCurrencyText = Text("Baijamjuree-Bold", 30, (354, 405), "white")
    currSprinkleCurrencyP1Text = Text("Baijamjuree-Bold", 30, (354, 405), "white")
    currSprinkleCurrencyP2Text = Text("Baijamjuree-Bold", 30, (238, 378), "white")
    multiplierText = Text("Baijamjuree-Bold", 40, (828, 150), "white")
    totalSprinkleCurrencyText = Text("Baijamjuree-Bold", 40, (828, 275), "white")
    shopPriceText = Text("Baijamjuree-Bold", 40, (820, 320), "white")
    highscoreText = Text("Baijamjuree-Bold", 40, (820, 320), "white")

    # Buttons
    retryButton = Button("retryButton", (surfaceSize[0] - 122, surfaceSize[1] - 60))
    backButton = Button("backButton", (122, surfaceSize[1] - 60))
    playButton = Button("playButton", (surfaceSize[0]/2, 295))
    infoButton = Button("infoButton", (surfaceSize[0]/2, 295 + 95))
    shopButton = Button("shopButton", (surfaceSize[0]/2, 295 + 190))
    exitButton = Button("backButton", (surfaceSize[0]/2, 60))
    leftPlayerButton = Button("leftTriangle", (668, 213))
    rightPlayerButton = Button("rightTriangle", (888, 213))
    leftControlsButton = Button("leftTriangle", (668, 345))
    rightControlsButton = Button("rightTriangle", (888, 345))
    infoLeftPlayerButton = Button("leftTriangle", (53, 113))
    infoRightPlayerButton = Button("rightTriangle", (273, 113))
    okButton = Button("okButton", (483, 355))
    claimButton = Button("claimButton", (485, 480))
    soundButton = Button("sound", (940, 20))
    muteButton = Button("mute", (940, 20))

    # Game Selection Buttons
    goModeButton = Button("goButton", (surfaceSize[0] - 122, surfaceSize[1] - 60))
    lifeOneButton = Button("modes/1 Life", (143, 233))
    lifeThreeButton = Button("modes/3 Lives", (143, 233 + 44))
    lifeFiveButton = Button("modes/5 Lives", (143, 233 + 44*2))
    lifeInfButton = Button("modes/Inf Lives", (143, 233 + 44*3))
    normalButton = Button("modes/normal", (143 + 226, 238))
    fastButton = Button("modes/fast", (143 + 226, 238 + 63))
    slowButton = Button("modes/slow", (143 + 226, 238 + 63 + 63))
    slipperyIButton = Button("modes/slipperyI", (140 + 226*2, 238))
    slipperyIIButton = Button("modes/slipperyII", (140 + 226*2, 238 + 63))
    slipperyIIIButton = Button("modes/slipperyIII", (140 + 226*2, 238 + 63 + 63))
    singleplayerButton = Button("modes/singleplayer", (137 + 226*3, 238))
    multiplayerButton = Button("modes/multiplayer", (137 + 226*3, 238 + 67))

    gameModeButtons = [[lifeOneButton, lifeThreeButton, lifeFiveButton, lifeInfButton], [normalButton, fastButton, slowButton], [slipperyIButton, slipperyIIButton, slipperyIIIButton]]

    # Shop Buttons
    creamButton = Button("iceCreamButton", (117, 215))
    coneButton = Button("conesButton", (117, 289))
    bgButton = Button("bgButton", (117, 362))
    buyButton = Button("buyButton", (839, surfaceSize[1] - 60))
    inventoryButton = Button("inventoryButton", (804, 76))
    shopButtons = [creamButton, coneButton, bgButton]

    def scrollingBg(bgImg, mode=None):
        if mode == "multiplayer":
            mainSurface.blit(bgImg, (-surfaceSize[0]/2, bgPos1[1]))
            mainSurface.blit(bgImg, (-surfaceSize[0]/2, bgPos2[1]))
            mainSurface.blit(bgImgs[bgP2], (surfaceSize[0]/2, bgPos1[1]))
            mainSurface.blit(bgImgs[bgP2], (surfaceSize[0]/2, bgPos2[1]))
        else:
            mainSurface.blit(bgImg, bgPos1)
            mainSurface.blit(bgImg, bgPos2)

        if bgPos1[1] <= -surfaceSize[1]:
            bgPos1[1] = surfaceSize[1]
        if bgPos2[1] <= -surfaceSize[1]:
            bgPos2[1] = surfaceSize[1]
        
        bgPos1[1] -= 0.7
        bgPos2[1] -= 0.7
    
    #-----------------------------Main Program Loop---------------------------------------------#
    while True:       
        # print(f"BGpos1: {bgPos1}    BGpos2: {bgPos2}")
        #-----------------------------Event Handling-----------------------------------------#
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            data["inventory"] = inventory
            data["sprinkleCurrency"] = sprinkleCurrency
            data["highscore"] = highscore
            data["P1 ice cream"] = creamSkinP1
            data["P2 ice cream"] = creamSkinP2
            data["P1 cone"] = coneSkinP1
            data["P2 cone"] = coneSkinP2
            data["P1 bg"] = bgP1
            data["P2 bg"] = bgP2


            with open('data.json', 'w') as store_data:
               json.dump(data, store_data)

            break                   #   ... leave game loop
        
        if iceCreamScoreP1 + sprinkleCreamScoreP1 > highscore:
            highscore = iceCreamScoreP1 + sprinkleCreamScoreP1
        elif iceCreamScoreP2 + sprinkleCreamScoreP2 > highscore:
            highscore = iceCreamScoreP2 + sprinkleCreamScoreP2

        if programState == "menu":
            scrollingBg(bgImgs[bgP1])
            mainSurface.blit(darkOverlay, (0,0))
            playButton.draw(mainSurface)
            infoButton.draw(mainSurface)
            shopButton.draw(mainSurface)

            mainSurface.blit(scoopTilUDropLogo, (310, sine(200.0, 1280, 10.0, 50)))
            highscoreText.update(highscore, (785, sine(200.0, 1280, 10.0, 340)), "white", None, "center")
            highscoreText.draw(mainSurface)

            #Sound button - if sound is on, the image with speaker will show, otherwise it will show the mute speaker
            if sound:
                soundButton.draw(mainSurface)
            else:
                muteButton.draw(mainSurface)
            

            if ev.type == pygame.MOUSEBUTTONUP:
                if playButton.collidePoint(pygame.mouse.get_pos()): #mode selection
                    programState = "mode selection"
                if infoButton.collidePoint(pygame.mouse.get_pos()): #info state
                    programState = "info"
                if shopButton.collidePoint(pygame.mouse.get_pos()): #shop state
                    programState = "shop"
                    if sound:
                        pygame.mixer.Channel(0).play(shopAudio, -1)
                    else:
                        pygame.mixer.Channel(0).pause()                        

                if soundButton.collidePoint(pygame.mouse.get_pos()):
                    if sound:
                        pygame.mixer.Channel(0).pause()
                        sound = False
                    else:
                        pygame.mixer.Channel(0).unpause()
                        sound = True
        
        
        if programState == "mode selection":
            scrollingBg(bgImgs[bgP1])
            mainSurface.blit(gameSelectionOverlay, (0,0))
            backButton.draw(mainSurface)
            goModeButton.draw(mainSurface)

            if sound:
                soundButton.draw(mainSurface)
            else:
                muteButton.draw(mainSurface)

            singleplayerButton.draw(mainSurface, prevMode, "singleplayer")
            multiplayerButton.draw(mainSurface, prevMode, "multiplayer")

            userSelectedModes = [livesMode, speedMode, slipperyMode]
            for i in range(len(gameModeButtons)): # Runs length of 2D list, [lives, speed, slippery]
                for j in range(len(gameModeButtons[i])): # Runs amount of buttons in list ex. [lifeOne, lifeThree, lifeFive... etc.]
                    gameModeButtons[i][j].draw(mainSurface, userSelectedModes[i], modes[i][j])
                    # print(f"user modes: {userSelectedModes[i]}       modes: {modes[i][j]}")

            if prevMode == "singleplayer":
                borderP1 = [0, surfaceSize[0]]
            else:
                borderP1 = [0, surfaceSize[0]/2 - 50]

            if livesMode == lives[3]:    
                infMultiplier = 0
            else:
                infMultiplier = 1

            multiplier = round((1.0 + livesMultiplier + speedMultiplier + slipperyMultiplier)*infMultiplier, 2)
            
            multiplierText.update(f"x {multiplier}", (500, 450))
            multiplierText.draw(mainSurface)

            if ev.type == pygame.MOUSEBUTTONUP:
                if backButton.collidePoint(pygame.mouse.get_pos()): #Back button to menu state
                    programState = "menu"

                if goModeButton.collidePoint(pygame.mouse.get_pos()):
                    if sound:
                        if random.randint(0, 1) == 0:
                            pygame.mixer.Channel(0).play(game0Audio, -1)
                        else:
                            pygame.mixer.Channel(0).play(game1Audio, -1)
                    else:
                        pygame.mixer.Channel(0).pause() 

                    iceCreamScoreP1 = 0
                    iceCreamScoreP2 = 0
                    sprinkleCreamScoreP1 = 0
                    sprinkleCreamScoreP2 = 0
                    
                    if prevMode == "singleplayer":
                        scoreP1Text.update(iceCreamScoreP1, (41, 47), "black", 20, "center")
                        sprinkleScoreP1Text.update(sprinkleCreamScoreP1, (41, 115), "black", 20, "center")
                        livesP1 = livesMode
                        livesP1Text.update(livesP1, (920, 42), "white", 20, "center")
                        creamP1Displacement = 0
                        creamP1Speed = 0
                        coneP1 = Cone(coneImgs[coneSkinP1], [surfaceSize[0]/2, 400], borderP1, slipperyMode, speedMode, p1Keys)
                        creamsP1 = pygame.sprite.Group()
                        creamP1 = IceCream(creamImgs, creamSkinP1, sprinklesImg, [random.randint(borderP1[0], borderP1[1]), -2500], coneP1, creamP1Displacement, creamP1Speed, borderP1, livesP1)
                        creamsP1.add(creamP1)
                        programState = "singleplayer"

                    elif prevMode == "multiplayer":
                        # Setting up for player 1
                        scoreP1Text.update(iceCreamScoreP1, (42, 44), "black", 20, "center")
                        sprinkleScoreP1Text.update(sprinkleCreamScoreP1, (42, 107), "black", 20, "center")
                        livesP1 = livesMode
                        livesP1Text.update(livesP1, (surfaceSize[0]/2-49, 33), "white", 20, "center")
                        creamP1Displacement = 0
                        creamP1Speed = 0
                        coneP1 = Cone(coneImgs[coneSkinP1], [surfaceSize[0]/4, 400], borderP1, slipperyMode, speedMode, p1Keys)
                        creamsP1 = pygame.sprite.Group()
                        creamP1 = IceCream(creamImgs, creamSkinP1, sprinklesImg, [random.randint(borderP1[0], borderP1[1]), -2000], coneP1, creamP1Displacement, creamP1Speed, borderP1, livesP1)
                        creamsP1.add(creamP1)

                        # Setting up for player 2
                        scoreP2Text.update(iceCreamScoreP2, (surfaceSize[0]/2 + 45, 45), "black", 20, "center")
                        sprinkleScoreP2text.update(sprinkleCreamScoreP2, (surfaceSize[0]/2 + 45, 108), "black", 20, "center")
                        livesP2 = livesMode
                        livesP2Text.update(livesP1)
                        creamP2Displacement = 0
                        creamP2Speed = 0
                        coneP2 = Cone(coneImgs[coneSkinP2], [(surfaceSize[0]/4)*3, 400], borderP2, slipperyMode, speedMode, p2Keys)
                        creamsP2 = pygame.sprite.Group()
                        creamP2 = IceCream(creamImgs, creamSkinP2, sprinklesImg, [random.randint(borderP2[0], borderP2[1]), -2000], coneP2, creamP2Displacement, creamP2Speed, borderP2, livesP2)
                        creamsP2.add(creamP2)
                        programState = "multiplayer"

                # Game Modes:
                # Players

                if singleplayerButton.collidePoint(pygame.mouse.get_pos()):
                    prevMode = "singleplayer"
                if multiplayerButton.collidePoint(pygame.mouse.get_pos()):
                    prevMode = "multiplayer"

                if lifeOneButton.collidePoint(pygame.mouse.get_pos()):
                    livesMode = lives[0]
                    livesMultiplier = 0
                if lifeThreeButton.collidePoint(pygame.mouse.get_pos()):
                    livesMode = lives[1]
                    livesMultiplier = -0.2
                if lifeFiveButton.collidePoint(pygame.mouse.get_pos()):
                    livesMode = lives[2]
                    livesMultiplier = -0.4
                if lifeInfButton.collidePoint(pygame.mouse.get_pos()):
                    livesMode = lives[3]      

                # Speed
                if normalButton.collidePoint(pygame.mouse.get_pos()):
                    speedMode = speed[0]
                    speedMultiplier = 0
                if fastButton.collidePoint(pygame.mouse.get_pos()):
                    speedMode = speed[1]
                    speedMultiplier = 0.1
                if slowButton.collidePoint(pygame.mouse.get_pos()):
                    speedMode = speed[2]
                    speedMultiplier = 0.2
                
                # Slippery
                if slipperyIButton.collidePoint(pygame.mouse.get_pos()):
                    slipperyMode = slippery[0]
                    slipperyMultiplier = 0
                if slipperyIIButton.collidePoint(pygame.mouse.get_pos()):
                    slipperyMode = slippery[1]
                    slipperyMultiplier = 0.1
                if slipperyIIIButton.collidePoint(pygame.mouse.get_pos()):
                    slipperyMode = slippery[2]
                    slipperyMultiplier = 0.2

                if soundButton.collidePoint(pygame.mouse.get_pos()):
                    if sound:
                        pygame.mixer.Channel(0).pause()
                        sound = False
                    else:
                        pygame.mixer.Channel(0).unpause()
                        sound = True


        if programState == "info":
            scrollingBg(bgImgs[bgP1])
            mainSurface.blit(infoOverlay, (0, 0))
            if infoPlayer == "p1":
                mainSurface.blit(p1Img, (777 - 72, 218 - 22))
                mainSurface.blit(keyImgs[p1Keys], (keyImgs[p1Keys].get_rect(center = (777, 346))))
            else:
                mainSurface.blit(p2Img, (777 - 72, 218 - 22))
                mainSurface.blit(keyImgs[p2Keys], (keyImgs[p2Keys].get_rect(center = (777, 346))))

            # Drawing buttons
            backButton.draw(mainSurface)
            leftPlayerButton.draw(mainSurface)
            rightPlayerButton.draw(mainSurface)
            leftControlsButton.draw(mainSurface)
            rightControlsButton.draw(mainSurface)
            
            if sound:
                soundButton.draw(mainSurface)
            else:
                muteButton.draw(mainSurface)

            if ev.type == pygame.MOUSEBUTTONUP:
                if backButton.collidePoint(pygame.mouse.get_pos()): #Back button to menu state
                    programState = "menu"
                if leftPlayerButton.collidePoint(pygame.mouse.get_pos()) or rightPlayerButton.collidePoint(pygame.mouse.get_pos()): 
                    if infoPlayer == "p1":
                        infoPlayer = "p2"
                    else:
                        infoPlayer = "p1"
                if leftControlsButton.collidePoint(pygame.mouse.get_pos()) or rightControlsButton.collidePoint(pygame.mouse.get_pos()):
                        if infoPlayer == "p1":
                            p1Keys += 1
                            if p1Keys == p2Keys:
                                p1Keys += 1
                            
                            if p1Keys > 2:
                                if p2Keys != 0:
                                    p1Keys = 0 
                                else:
                                    p1Keys = 1
        
                        elif infoPlayer == "p2":
                            p2Keys += 1
                            if p2Keys == p1Keys:
                                p2Keys += 1
                            
                            if p2Keys > 2:
                                if p1Keys != 0:
                                    p2Keys = 0 
                                else:
                                    p2Keys = 1
                if soundButton.collidePoint(pygame.mouse.get_pos()):
                    if sound:
                        pygame.mixer.Channel(0).pause()
                        sound = False
                    else:
                        pygame.mixer.Channel(0).unpause()
                        sound = True
        

        if programState == "shop":
            scrollingBg(bgImgs[bgP1])

            if boughtScene == "none":
                mainSurface.blit(shopOverlay, (0, 0))
                totalSprinkleCurrencyText.update(sprinkleCurrency, (100, 39))
                totalSprinkleCurrencyText.draw(mainSurface)

                backButton.draw(mainSurface)
                buyButton.draw(mainSurface)

                inventoryButton.update((804, 76))
                inventoryButton.draw(mainSurface)

                if sound:
                    soundButton.draw(mainSurface)
                else:
                    muteButton.draw(mainSurface)

                for i in range(len(shopButtons)):
                    shopButtons[i].draw(mainSurface, shopState, shopStates[i])
                
                if shopState == "ice cream":
                    mainSurface.blit(shopCreamOverlay, (0, 0))
                    priceVal = 50
                    shopPriceText.update(priceVal)
                elif shopState == "cones":
                    mainSurface.blit(shopConeOverlay, (0, 0))
                    priceVal = 35
                    shopPriceText.update(priceVal)
                elif shopState == "backgrounds":
                    mainSurface.blit(shopBackgroundsOverlay, (0, 0))
                    priceVal = 35
                    shopPriceText.update(priceVal)

                shopPriceText.draw(mainSurface)

                if ev.type == pygame.MOUSEBUTTONUP:
                    if backButton.collidePoint(pygame.mouse.get_pos()): #Back button to menu state
                        programState = "menu"
                        if sound:
                            pygame.mixer.Channel(0).play(mainAudio, -1)
                        else:
                            pygame.mixer.Channel(0).pause()    

                    if inventoryButton.collidePoint(pygame.mouse.get_pos()): #Back button to menu state
                        programState = "inventory"

                    if creamButton.collidePoint(pygame.mouse.get_pos()):
                        shopState = "ice cream"
                        
                    if coneButton.collidePoint(pygame.mouse.get_pos()):
                        shopState = "cones"
                        
                    if bgButton.collidePoint(pygame.mouse.get_pos()):
                        shopState = "backgrounds"
                    
                    if okButton.collidePoint(pygame.mouse.get_pos()):
                        priceError = False
                    
                    if buyButton.collidePoint(pygame.mouse.get_pos()):
                        if sprinkleCurrency >= priceVal:
                            sprinkleCurrency -= priceVal
                            boughtScene = "unclaimed"
                        else:
                            priceError = True
                    
                    if soundButton.collidePoint(pygame.mouse.get_pos()):
                        if sound:
                            pygame.mixer.Channel(0).pause()
                            sound = False
                        else:
                            pygame.mixer.Channel(0).unpause()
                            sound = True

                if priceError == True:
                    mainSurface.blit(errorOverlay, (0, 0))
                    okButton.draw(mainSurface)

            elif boughtScene == "unclaimed":
                mainSurface.blit(darkOverlay, (0, 0))
                mainSurface.blit(boxImg, (0,0))
                claimButton.draw(mainSurface)

                if ev.type == pygame.MOUSEBUTTONUP:
                    if claimButton.collidePoint(pygame.mouse.get_pos()):
                        boughtScene = "claimed"
                        if shopState == "ice cream":
                            randCreamNum = random.randint(1, len(itemCreamImgs)-1)
                            if randCreamNum not in inventory[0]:
                                inventory[0].append(randCreamNum)
                        elif shopState == "cones":
                            randConeNum = random.randint(2, len(itemConeImgs)-1)
                            if randConeNum not in inventory[1]:
                                inventory[1].append(randConeNum)
                        elif shopState == "backgrounds":
                            randBgNum = random.randint(2, len(itemBgImgs)-1)
                            if randBgNum not in inventory[2]:
                                inventory[2].append(randBgNum)
                                    
            elif boughtScene == "claimed":
                mainSurface.blit(darkOverlay, (0, 0))
                mainSurface.blit(boxOpenImg, (0,0))
                if shopState == "ice cream":
                    mainSurface.blit(creamImgs[randCreamNum][0], (surfaceSize[0]/2 - creamP1.rect.width/2, sine(200.0, 1280, 10.0, surfaceSize[1]/2 - creamP1.rect.height/2)))
                elif shopState == "cones":
                    mainSurface.blit(coneImgs[randConeNum], (surfaceSize[0]/2 - coneP1.rect.width/2, sine(200.0, 1280, 10.0, surfaceSize[1]/2 - coneP1.rect.height/2)))
                elif shopState == "backgrounds":
                    mainSurface.blit(itemBgImgs[randBgNum], (surfaceSize[0]/2 - 30, sine(200.0, 1280, 10.0, surfaceSize[1]/2 - 30)))

                backButton.draw(mainSurface)
                inventoryButton.update((804, surfaceSize[1] - 60))
                inventoryButton.draw(mainSurface)

                if ev.type == pygame.MOUSEBUTTONUP:
                    if backButton.collidePoint(pygame.mouse.get_pos()): #Back button to shop state
                        boughtScene = "none"
                    if inventoryButton.collidePoint(pygame.mouse.get_pos()):
                        boughtScene = "none"
                        programState = "inventory"
                    
        if programState == "inventory":
            scrollingBg(bgImgs[bgP1])
            mainSurface.blit(inventoryOverlay, (0, 0))
            backButton.draw(mainSurface)
            infoLeftPlayerButton.draw(mainSurface)
            infoRightPlayerButton.draw(mainSurface)

            if sound:
                soundButton.draw(mainSurface)
            else:
                muteButton.draw(mainSurface)

            if inventoryPlayer == "p1":
                # Player 1 selected skins and inventory
                mainSurface.blit(p1Img, (93, 96))
                # Selected ice cream skin
                for i in range(len(creamImgs)):
                    if creamSkinP1 == i:
                        mainSurface.blit(itemCreamImgs[creamSkinP1], (218, 183))

                # Selected cone skin
                for i in range(len(coneImgs)):
                    if creamSkinP1 == i:
                        mainSurface.blit(itemConeImgs[coneSkinP1], (218, 263))
                
                # Selected bg skin
                for i in range(len(bgImgs)):
                    if creamSkinP1 == i:
                        mainSurface.blit(itemBgImgs[bgP1], (215, 329))
            else:
                # Player 2 selected skins and inventory
                mainSurface.blit(p2Img, (93, 96))
                # Selected ice cream skin
                for i in range(len(creamImgs)):
                    if creamSkinP2 == i:
                        mainSurface.blit(itemCreamImgs[creamSkinP2], (218, 183))

                # Selected cone skin
                for i in range(len(coneImgs)):
                    if creamSkinP2 == i:
                        mainSurface.blit(itemConeImgs[coneSkinP2], (218, 263))
                
                # Selected bg skin
                for i in range(len(bgImgs)):
                    if creamSkinP2 == i:
                        mainSurface.blit(itemBgImgs[bgP2], (215, 329))

            for i in range(len(shopButtons)):
                shopButtons[i].draw(mainSurface, inventoryState, shopStates[i])

            # 0 - Ice Cream Skins, default skin pack = 0
            # 1 - Cone Skins, default skin packs = 0 , 1
            # 2 - Background Skins, default bg skins = 0, 1
            if inventoryState == "ice cream":
                for i in range(len(inventory[0])):
                    if i < 5:
                        tempX = 329
                        tempY = 0
                        mainSurface.blit(itemCreamImgs[inventory[0][i]], (340 + 126*i, 196))
                    else:
                        tempX = -301
                        tempY = 126
                        mainSurface.blit(itemCreamImgs[inventory[0][i]], (-290 + 126*i, 196 + 126))

                    if inventoryPlayer == "p1":
                        if creamSkinP1 == inventory[0][i]:
                            mainSurface.blit(checkOverlay, (tempX + 126*i, 187 + tempY))
                    else:
                        if creamSkinP2 == inventory[0][i]:
                            mainSurface.blit(checkOverlay, (tempX + 126*i, 187 + tempY))

                    if ev.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pos()[0] > tempX + 126*i and pygame.mouse.get_pos()[0] < tempX + 126*i + 80 and pygame.mouse.get_pos()[1] > 187 + tempY and pygame.mouse.get_pos()[1] < 187 + tempY + 80:
                        if inventoryPlayer == "p1":
                            creamSkinP1 = inventory[0][i]
                        else:
                            creamSkinP2 = inventory[0][i]

            elif inventoryState == "cones":
                for i in range(len(inventory[1])):
                    if i < 5:
                        tempX = 329
                        tempY = 0
                        mainSurface.blit(itemConeImgs[inventory[1][i]], (342 + 126*i, 202))
                    else:
                        tempX = -301
                        tempY = 126
                        mainSurface.blit(itemConeImgs[inventory[1][i]], (-287 + 126*i, 202 + 126))
                    
                    if inventoryPlayer == "p1":
                        if coneSkinP1 == inventory[1][i]:
                            mainSurface.blit(checkOverlay, (tempX + 126*i, 187 + tempY))
                    else:
                        if coneSkinP2 == inventory[1][i]:
                            mainSurface.blit(checkOverlay, (tempX + 126*i, 187 + tempY))

                    if ev.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pos()[0] > tempX + 126*i and pygame.mouse.get_pos()[0] < tempX + 126*i + 80 and pygame.mouse.get_pos()[1] > 187 + tempY and pygame.mouse.get_pos()[1] < 187 + tempY + 80:
                        if inventoryPlayer == "p1":
                            coneSkinP1 = inventory[1][i]
                        else:
                            coneSkinP2 = inventory[1][i]

            elif inventoryState == "backgrounds":
                for i in range(len(inventory[2])):
                    if i < 5:
                        tempX = 329
                        tempY = 0
                        mainSurface.blit(itemBgImgs[inventory[2][i]], (337 + 126*i, 196))
                    else:
                        tempX = -301
                        tempY = 126
                        mainSurface.blit(itemBgImgs[inventory[2][i]], (-292 + 126*i, 196 + 126))
                    
                    if inventoryPlayer == "p1":
                        if bgP1 == inventory[2][i]:
                            mainSurface.blit(checkOverlay, (tempX + 126*i, 187 + tempY))
                    else:
                        if bgP2 == inventory[2][i]:
                            mainSurface.blit(checkOverlay, (tempX + 126*i, 187 + tempY))

                    if ev.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pos()[0] > tempX + 126*i and pygame.mouse.get_pos()[0] < tempX + 126*i + 80 and pygame.mouse.get_pos()[1] > 187 + tempY and pygame.mouse.get_pos()[1] < 187 + tempY + 80:
                        if inventoryPlayer == "p1":
                            bgP1 = inventory[2][i]
                        else:
                            bgP2 = inventory[2][i]

            if ev.type == pygame.MOUSEBUTTONUP:
                if backButton.collidePoint(pygame.mouse.get_pos()): #Back button to shop state
                    programState = "shop"
                
                if creamButton.collidePoint(pygame.mouse.get_pos()):
                    inventoryState = "ice cream"
                    
                if coneButton.collidePoint(pygame.mouse.get_pos()):
                    inventoryState = "cones"
                    
                if bgButton.collidePoint(pygame.mouse.get_pos()):
                    inventoryState = "backgrounds"
                
                if infoLeftPlayerButton.collidePoint(pygame.mouse.get_pos()) or infoRightPlayerButton.collidePoint(pygame.mouse.get_pos()): 
                    if inventoryPlayer == "p1":
                        inventoryPlayer = "p2"
                    else:
                        inventoryPlayer = "p1"
                
                if soundButton.collidePoint(pygame.mouse.get_pos()):
                    if sound:
                        pygame.mixer.Channel(0).pause()
                        sound = False
                    else:
                        pygame.mixer.Channel(0).unpause()
                        sound = True

        if programState == "singleplayer":
        #-----------------------------Program Logic---------------------------------------------#
        # Update your game objects and data structures here...


        #-----------------------------Drawing Everything-------------------------------------#
            scrollingBg(bgImgs[bgP1])
                
            coneP1.draw(mainSurface)
            coneP1.update(creamP1Displacement)
            for creamP1 in creamsP1:
                creamP1.draw(mainSurface)
                creamP1.update()

            livesP1 = creamP1.lives
            if creamP1.is_collided_with():
                if creamP1.sprinkleCream:
                    sprinkleCreamScoreP1 += 1
                else:
                    iceCreamScoreP1 += 1
                creamP1Displacement += 50
                creamP1Speed += creamSpeed
                coneP1.pos.y += 50
                print("Collision detected")
                creamP1 = IceCream(creamImgs, creamSkinP1, sprinklesImg, [random.randint(borderP1[0], borderP1[1]), -100], coneP1, creamP1Displacement, creamP1Speed, borderP1, livesP1)
                creamsP1.add(creamP1)

                scoreP1Text.update(iceCreamScoreP1, (41, 47), "black", 20, "center")
                sprinkleScoreP1Text.update(sprinkleCreamScoreP1, (41, 115), "black", 20, "center")
            # print(creamP1Displacement)

            mainSurface.blit(singleplayerOverlay, (0, 0))


            scoreP1Text.draw(mainSurface)
            sprinkleScoreP1Text.draw(mainSurface)
            livesP1Text.draw(mainSurface)

            if creamP1.gameOver == True:
                programState = "game over"
            
            
            if int(countdownNum/100) != 0:
                countdownNum -= 2
                mainSurface.blit(darkOverlay, (0,0))
                countdownText.update(f"Ready in: {int(countdownNum/100)}", None, None, 40, "center")
                countdownText.draw(mainSurface)
            
            # Checks if livesMode is third item in lives, which is infinite lives and leaves the lives text as blank
            if livesMode == lives[3]:
                livesP1Text.update("")
                exitButton.update([surfaceSize[0]/2, 60])
                exitButton.draw(mainSurface)
                if ev.type == pygame.MOUSEBUTTONUP:
                    if exitButton.collidePoint(pygame.mouse.get_pos()): #Back button to game over screen when user selects infinite lives
                        programState = "game over"
            else:
                livesP1Text.update(livesP1, None, None, None, "center")


        if programState == "multiplayer":

            scrollingBg(bgImgs[bgP1], "multiplayer")

            coneP1.draw(mainSurface)
            coneP1.update(creamP1Displacement)

            for creamP1 in creamsP1:
                creamP1.draw(mainSurface)
                creamP1.update()
            
            livesP1 = creamP1.lives
            if creamP1.is_collided_with():
                coneP1.pos.y += 50
                print("Collision detected")

                if creamP1.sprinkleCream:
                    sprinkleCreamScoreP1 += 1
                else:
                    iceCreamScoreP1 += 1

                creamP1Displacement += 50
                creamP1Speed += creamSpeed

                creamP1 = IceCream(creamImgs, creamSkinP1, sprinklesImg, [random.randint(borderP1[0], borderP1[1]), -100], coneP1, creamP1Displacement, creamP1Speed, borderP1, livesP1)
                creamsP1.add(creamP1)

                scoreP1Text.update(iceCreamScoreP1, (41, 47), "black", 20, "center")
                sprinkleScoreP1Text.update(sprinkleCreamScoreP1, (41, 110), "black", 20, "center")

            coneP2.draw(mainSurface)
            coneP2.update(creamP2Displacement)

            for creamP2 in creamsP2:
                creamP2.draw(mainSurface)
                creamP2.update()

            # print(creamP1Displacement)
            livesP2 = creamP2.lives
            if creamP2.is_collided_with():
                print("Collision detected")
                coneP2.pos.y += 50
                if creamP2.sprinkleCream:
                    sprinkleCreamScoreP2 += 1
                else:
                    iceCreamScoreP2 += 1

                creamP2Displacement += 50
                creamP2Speed += creamSpeed
                
                creamP2 = IceCream(creamImgs, creamSkinP2, sprinklesImg, [random.randint(borderP2[0], borderP2[1]), -100], coneP2, creamP2Displacement, creamP2Speed, borderP2, livesP2)
                creamsP2.add(creamP2)

                scoreP2Text.update(iceCreamScoreP2, (surfaceSize[0]/2 + 45, 45), "black", 20, "center")
                sprinkleScoreP2text.update(sprinkleCreamScoreP2, (surfaceSize[0]/2 + 45, 108), "black", 20, "center")
            
            mainSurface.blit(multiplayerOverlay, (0, 0))

            scoreP1Text.draw(mainSurface)
            sprinkleScoreP1Text.draw(mainSurface)
            livesP1Text.draw(mainSurface)

            scoreP2Text.draw(mainSurface)
            sprinkleScoreP2text.draw(mainSurface)
            livesP2Text.draw(mainSurface)

            if int(countdownNum/100) != 0:
                countdownNum -= 2
                countdownText.update(f"Ready in: {int(countdownNum/100)}", None, None, 40, "center")
                mainSurface.blit(darkOverlay, (0,0))
                countdownText.draw(mainSurface)

            if creamP1.gameOver == True and creamP2.gameOver == True:
                programState = "game over"
            elif creamP1.gameOver:
                mainSurface.blit(darkOverlay, (-surfaceSize[0]/2, 0))
            elif creamP2.gameOver:
                mainSurface.blit(darkOverlay, (surfaceSize[0]/2, 0))
            
            # Checks if livesMode is third item in lives, which is infinite lives and leaves the lives text as blank
            if livesMode == lives[3]:
                livesP1Text.update("")
                livesP2Text.update("")
                exitButton.update([surfaceSize[0]/4, 60])
                exitButton.draw(mainSurface)
                if ev.type == pygame.MOUSEBUTTONUP:
                    if exitButton.collidePoint(pygame.mouse.get_pos()): #Back button to game over screen when user selects infinite lives
                        programState = "game over"
            else:
                if creamP1.gameOver:
                    livesP1Text.update("0", None, None, None, "center")
                else:
                    livesP1Text.update(livesP1, None, None, None, "center")

                if creamP2.gameOver:
                    livesP2Text.update("0", None, None, None, "center")
                else:
                    livesP2Text.update(livesP2, None, None, None, "center")
            # pygame.draw.line(mainSurface, "light blue", (0, (540/4)*3), (960, (540/4)*3), width = 2)
            # pygame.draw.line(mainSurface, "light blue", (surfaceSize[0]/2, (540/4)*3), (surfaceSize[0]/2, surfaceSize[1]), width = 2)
        
        if programState == "game over":
            scrollingBg(bgImgs[bgP1])

            if prevMode == "singleplayer":
                currSprinkleCurrency = round((iceCreamScoreP1 + 3*sprinkleCreamScoreP1)*(multiplier))
                mainSurface.blit(bgGameOver, (0,0))
                scoreP1Text.update(iceCreamScoreP1, (127, 300), "white", 30)
                scoreP1Text.draw(mainSurface)
                sprinkleScoreP1Text.update(sprinkleCreamScoreP1, (362, 300), "white", 30)
                sprinkleScoreP1Text.draw(mainSurface)
                currSprinkleCurrencyText.update(currSprinkleCurrency, (599, 300))
                currSprinkleCurrencyText.draw(mainSurface)

                totalSprinkleCurrencyText.update(sprinkleCurrency + currSprinkleCurrency, (828, 275), None, None, "center")
                totalSprinkleCurrencyText.draw(mainSurface)

            else:
                currSprinkleCurrencyP1 = round((iceCreamScoreP1 + 3*sprinkleCreamScoreP1)*multiplier)
                currSprinkleCurrencyP2 = round((iceCreamScoreP2 + 3*sprinkleCreamScoreP2)*multiplier)
                currSprinkleCurrency = round(currSprinkleCurrencyP1 + currSprinkleCurrencyP2)
                mainSurface.blit(bgGameOverMulti, (0,0))

                scoreP1Text.update(iceCreamScoreP1, (238, 246), "white", 30)
                scoreP1Text.draw(mainSurface)
                sprinkleScoreP1Text.update(sprinkleCreamScoreP1, (426, 246), "white", 30)
                sprinkleScoreP1Text.draw(mainSurface)
                currSprinkleCurrencyP1Text.update(currSprinkleCurrencyP1, (617, 246))
                currSprinkleCurrencyP1Text.draw(mainSurface)

                scoreP2Text.update(iceCreamScoreP2, (238, 378), "white", 30)
                scoreP2Text.draw(mainSurface)
                sprinkleScoreP2text.update(sprinkleCreamScoreP2, (426, 378), "white", 30)
                sprinkleScoreP2text.draw(mainSurface)
                currSprinkleCurrencyP2Text.update(currSprinkleCurrencyP2, (617, 378))
                currSprinkleCurrencyP2Text.draw(mainSurface)

                currSprinkleCurrencyText.update(round(currSprinkleCurrency/2), (549, 470))
                currSprinkleCurrencyText.draw(mainSurface)

                totalSprinkleCurrencyText.update(sprinkleCurrency + round(currSprinkleCurrency/2), (828, 275), None, None, "center")
                totalSprinkleCurrencyText.draw(mainSurface)


            multiplierText.update(f"x {multiplier}", (828, 150), None, None, "center")
            multiplierText.draw(mainSurface)

            retryButton.draw(mainSurface)
            backButton.draw(mainSurface)

            if sound:
                soundButton.draw(mainSurface)
            else:
                muteButton.draw(mainSurface)

            if ev.type == pygame.MOUSEBUTTONUP:
                countdownNum = 400

                for cream in creamsP1:
                        cream.kill()

                if prevMode == "multiplayer":
                    for cream in creamsP2:
                        cream.kill()

                if backButton.collidePoint(pygame.mouse.get_pos()): #Back button to menu state
                    if sound:
                            pygame.mixer.Channel(0).play(mainAudio, -1)
                    else:
                        pygame.mixer.Channel(0).pause() 
                            
                    iceCreamScoreP1 = 0
                    sprinkleCreamScoreP1 = 0
                    iceCreamScoreP2 = 0
                    sprinkleCreamScoreP2 = 0

                    if prevMode == "singleplayer":
                        sprinkleCurrency += currSprinkleCurrency
                    else:
                        sprinkleCurrency += round(currSprinkleCurrency/2)

                    programState = "menu"

                if retryButton.collidePoint(pygame.mouse.get_pos()):
                    if sound:
                        if random.randint(0, 1) == 0:
                            pygame.mixer.Channel(0).play(game0Audio, -1)
                        else:
                            pygame.mixer.Channel(0).play(game1Audio, -1)
                    else:
                        pygame.mixer.Channel(0).pause() 

                    iceCreamScoreP1 = 0
                    sprinkleCreamScoreP1 = 0
                    iceCreamScoreP2 = 0
                    sprinkleCreamScoreP2 = 0

                    if prevMode == "singleplayer":
                        sprinkleCurrency += currSprinkleCurrency
                    else:
                        sprinkleCurrency += round(currSprinkleCurrency/2)

                    if prevMode == "singleplayer":
                        scoreP1Text.update(iceCreamScoreP1, (41, 47), "black", 20, "center")
                        sprinkleScoreP1Text.update(sprinkleCreamScoreP1, (41, 115), "black", 20, "center")
                        livesP1Text.update(livesP1, (920, 42), "white", 20, "center")
                        livesP1 = livesMode
                        creamP1Displacement = 0
                        creamP1Speed = 0
                        coneP1 = Cone(coneImgs[coneSkinP1], [surfaceSize[0]/2, 400], borderP1, slipperyMode, speedMode, p1Keys)
                        creamsP1 = pygame.sprite.Group()
                        creamP1 = IceCream(creamImgs, creamSkinP1, sprinklesImg, [random.randint(borderP1[0], borderP1[1]), -2000], coneP1, creamP1Displacement, creamP1Speed, borderP1, livesP1)
                        creamsP1.add(creamP1)
                        programState = "singleplayer"

                    elif prevMode == "multiplayer":
                        # Setting up for player 1
                        scoreP1Text.update(iceCreamScoreP1, (41, 47), "black", 20, "center")
                        sprinkleScoreP1Text.update(sprinkleCreamScoreP1, (41, 110), "black", 20, "center")
                        livesP1Text.update(livesP1, (surfaceSize[0]/2-49, 33), "white", 20, "center")
                        livesP1 = livesMode
                        creamP1Displacement = 0
                        creamP1Speed = 0
                        coneP1 = Cone(coneImgs[coneSkinP1], [surfaceSize[0]/4, 400], borderP1, slipperyMode, speedMode, p1Keys)
                        creamsP1 = pygame.sprite.Group()
                        creamP1 = IceCream(creamImgs, creamSkinP1, sprinklesImg, [random.randint(borderP1[0], borderP1[1]), -2000], coneP1, creamP1Displacement, creamP1Speed, borderP1, livesP1)
                        creamsP1.add(creamP1)

                        # Setting up for player 2
                        scoreP2Text.update(iceCreamScoreP2, (surfaceSize[0]/2 + 45, 45), "black", 20, "center")
                        sprinkleScoreP2text.update(sprinkleCreamScoreP2, (surfaceSize[0]/2 + 45, 108), "black", 20, "center")
                        livesP2 = livesMode
                        creamP2Displacement = 0
                        creamP2Speed = 0
                        coneP2 = Cone(coneImgs[coneSkinP2], [(surfaceSize[0]/4)*3, 400], borderP2, slipperyMode, speedMode, p2Keys)
                        creamsP2 = pygame.sprite.Group()
                        creamP2 = IceCream(creamImgs, creamSkinP2, sprinklesImg, [random.randint(borderP2[0], borderP2[1]), -2000], coneP2, creamP2Displacement, creamP2Speed, borderP2, livesP2)
                        creamsP2.add(creamP2)
                        programState = "multiplayer"

                if soundButton.collidePoint(pygame.mouse.get_pos()):
                    if sound:
                        pygame.mixer.Channel(0).pause()
                        sound = False
                    else:
                        pygame.mixer.Channel(0).unpause()
                        sound = True

        pygame.display.flip()
        
        clock.tick(60) #Force frame rate to be slower


    pygame.quit()     # Once we leave the loop, close the window.

main()