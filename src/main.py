'''
Leonardo Nieto
Pygame Hangman
Programming 11 Final Project
2024-01-19
'''
import pygame
import sys
import random
import time
import os

#Initialize pygame
pygame.init()
pygame.mixer.init()

#_____________INITIALIZATION / SETUP / CONSTANTS________________________________________________________________________________________________________________

clock = pygame.time.Clock()
WIDTH = 950
HEIGHT = WIDTH*3/4

# Window/Screen:
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman by Leonardo Nieto")

# Colors:
WHITE = (255,255,255)
BLACK = (0,0,0)

# Base paths for assets
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
AUDIO_DIR = os.path.join(ASSETS_DIR, 'audio')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

# Helper function to get asset paths
def get_image_path(subfolder, filename):
    return os.path.join(IMAGES_DIR, subfolder, filename)

def get_audio_path(subfolder, filename):
    return os.path.join(AUDIO_DIR, subfolder, filename)

def get_font_path(filename):
    return os.path.join(FONTS_DIR, filename)

def get_data_path(filename):
    return os.path.join(DATA_DIR, filename)

# Loading Screen at the beginning of the code:
Font = pygame.font.Font(get_font_path('PIXELADE.TTF'), 55)
text = Font.render("Loading...", True, WHITE)
text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT// 2))
WINDOW.fill((190, 130, 80))
WINDOW.blit(text, text_rect)
pygame.display.flip()

# Fonts:
RevealFont = pygame.font.Font(get_font_path('PIXELADE.TTF'), 65)
FontDifficulty = pygame.font.Font(get_font_path('PIXELADE.TTF'), 65)
InstructionsFont = pygame.font.Font(get_font_path('PIXELADE.TTF'), 40)
FullWordGuessFont = pygame.font.Font(get_font_path('PIXELADE.TTF'), 48)
CountdownFont = pygame.font.Font(get_font_path('PIXELADE.TTF'), 100)

# Load Images:
RevealSignPNG = pygame.image.load(get_image_path('ui', "RevealSignBoard.png"))
KeyboardSignPNG = pygame.image.load(get_image_path('ui', "KeyboardSignBoard.png"))
CountDownBlackOutPNG = pygame.image.load(get_image_path('ui', "CountDownBlackOut.png"))
FullWordGuessPopUpPNG = pygame.image.load(get_image_path('ui', "FullWordGuessPopUp.png"))

# Load Sound Effects and Music files:
mp3_BigButtonPressFX = pygame.mixer.Sound(get_audio_path('sfx', "BigButtonPressFX.mp3"))
mp3_CountDownSFX = pygame.mixer.Sound(get_audio_path('sfx', "CountDownSFX.mp3"))
mp3_WinFanfareFX = pygame.mixer.Sound(get_audio_path('music', "Indy's Fanfare.mp3"))
mp3_LooseLifeFX = pygame.mixer.Sound(get_audio_path('sfx', "LooseLifeFX.mp3"))
mp3_SmallButtonPressFX = pygame.mixer.Sound(get_audio_path('sfx', "LightSwitchFX.mp3"))
mp3_KeyboardTypingFX = pygame.mixer.Sound(get_audio_path('sfx', "KeyboardTypingFX.mp3"))
mp3_BlockedFX = pygame.mixer.Sound(get_audio_path('sfx', "BlockedFX.mp3"))


AlphabetList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
sInstructions = '''
Instructions:
1. Guess letters to uncover the hidden
 word.
2. Correct guesses reveal letters;
 incorrect guesses draw the hangman.
3. You can also guess the entire word.
4. The game ends when the word is 
guessed or the hangman is complete.
5. You have 7 incorrect guesses before
 the game ends.
6. Have fun and good luck!
'''


# Initialize global variables
iHighestScore = 1
bMusicOn = True
bSoundEffectsOn = True


#_____________CLASSES________________________________________________________________________________________________________________

class HangingMan:
    def __init__(self):
        self.x = -140
        self.y = 170
        self.image = []
        for x in range(0,8):
            self.image.append(pygame.image.load(get_image_path('hangman', f'Error1.{x}HangmanPictures.png')))


    def draw(self, errors):
        WINDOW.blit(self.image[errors], (self.x, self.y))

# Initialize HangmanMan class instance
GallowsPictures = HangingMan()



class TitleScreen: 
    def __init__(self, name):
        self.image = pygame.image.load(get_image_path('screens', f"{name}.png"))
        self.startTime = pygame.time.get_ticks()
        self.displayTime = 5000
        self.closeFlag = False
        self.showing = False
        self.buttons = []
        self.music = get_audio_path('music', "Indiana Jones Main Theme.mp3")

        #   resize images to fit screen:
        original_width, original_height = self.image.get_size()
        scale_factor_width = WIDTH / original_width
        scale_factor_height = HEIGHT / original_height
        scale_factor = min(scale_factor_width, scale_factor_height)

        self.scaled_image = pygame.transform.scale(self.image, (int(original_width * scale_factor), int(original_height * scale_factor)))
        self.image_rect = self.scaled_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        
    def fnResetScreen(self):
        for button in self.buttons:
            button.ResetButton()


    def draw(self):
        WINDOW.blit(self.scaled_image, self.image_rect)
        for button in self.buttons:
            button.draw()
        pygame.display.update()

    def Run(self):
        global bMusicOn
        global bSoundEffectsOn

        RunGame = True
        self.fnResetScreen()

        if bMusicOn: 
            fnPlayMusic(self.music)

        while RunGame == True:
            for button in self.buttons:
                button.clicked = False
                button.mouseover = False

            for event in pygame.event.get():  # Event Pump
                mousePos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    for button in self.buttons:
                        button.handle_event(event)

                if event.type == pygame.MOUSEBUTTONUP: #Manage events when ButtonUp for better interface experience
                    mousePos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.isClicked(mousePos):
                            if button == PlayButton:
                                fnPlaySoundEffects(mp3_BigButtonPressFX)  #transition between screens
                                RunGame = False

                            #Music/SoundEffects ON/OFF
                            elif button == MusicOFFButtonTitleScreen and MusicOFFButtonTitleScreen.show:
                                MusicONButtonTitleScreen.show, MusicONButtonTitleScreen.hide = True, False
                                button.show = False
                                button.hide = True
                                bMusicOn = True
                                fnPlayMusic(self.music)

                            elif button == MusicONButtonTitleScreen and MusicONButtonTitleScreen.show:
                                MusicOFFButtonTitleScreen.show, MusicOFFButtonTitleScreen.hide = True, False
                                button.show = False
                                button.hide = True
                                bMusicOn = False
                                pygame.mixer.music.stop()

                            elif button == SoundEffectsOFFButtonTitleScreen and SoundEffectsOFFButtonTitleScreen.show:
                                SoundEffectsONButtonTitleScreen.show, SoundEffectsONButtonTitleScreen.hide = True, False
                                button.show = False
                                button.hide = True
                                bSoundEffectsOn = True

                            elif button == SoundEffectsONButtonTitleScreen and SoundEffectsONButtonTitleScreen.show:
                                SoundEffectsOFFButtonTitleScreen.show, SoundEffectsOFFButtonTitleScreen.hide = True, False
                                button.show = False
                                button.hide = True
                                bSoundEffectsOn = False
                            break

            self.draw() 
            clock.tick(60)

        pygame.mixer.music.stop() #stop music when exit title screen
    


class InstructionsScreen: 
    def __init__(self, name):
        self.startTime = pygame.time.get_ticks()
        self.presentFrameTime = pygame.time.get_ticks()
        self.transitionTime = 300
        self.buttons = []
        self.AllFrames = [
            pygame.image.load(get_image_path('screens', f"{name}1.1.png")), 
            pygame.image.load(get_image_path('screens', f"{name}1.2.png")), 
            pygame.image.load(get_image_path('screens', f"{name}1.3.png")), 
            pygame.image.load(get_image_path('screens', f"{name}1.4.png")), 
            pygame.image.load(get_image_path('screens', f"{name}1.5.png")), 
            pygame.image.load(get_image_path('screens', f"{name}1.6.png"))
        ]
        self.AllScaledFrames = []
        self.AllFramesScaledRectangles = []
        self.music = get_audio_path('music', "InstructionsScreen-Map.mp3")

        #   resize images to fit screen dimensions: 
        for image in self.AllFrames: 
            original_width, original_height = image.get_size()
            scale_factor_width = WIDTH / original_width
            scale_factor_height = HEIGHT / original_height
            scale_factor = min(scale_factor_width, scale_factor_height)

            scaled_image = pygame.transform.scale(image, (int(original_width * scale_factor), int(original_height * scale_factor)))
            image_rect = scaled_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

            self.AllScaledFrames.append(image)
            self.AllFramesScaledRectangles.append(image_rect)


    def fnResetScreen(self): 
        for button in self.buttons:
            button.ResetButton()


    def draw(self, iCurrentFrameNumber):
        CurrentFrame = (self.AllFrames[iCurrentFrameNumber]) 
        CurrentFrameRectangle = (self.AllFramesScaledRectangles[iCurrentFrameNumber])
        WINDOW.blit(CurrentFrame, CurrentFrameRectangle)
        for button in self.buttons:
            button.draw()

    
    def Run(self):
        self.fnResetScreen()

        RunGame = True
        iCurrentFrameNumber = 0 
        StartTransition = False
        Transition_1_Over = False
        Start_Transition_2 = False
        Transition_2_Over = False
        InitialYPositionOfCurrentLine = 45
        Y_PositionOfCurrentLine = InitialYPositionOfCurrentLine

        TimeWhenTransition_1_Over = None
        if bMusicOn: 
            fnPlayMusic(self.music)

        while RunGame == True:
            for button in self.buttons:
                button.clicked = False
                button.mouseover = False

            for event in pygame.event.get(): # Event Pump
                mousePos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if StartTransition == False:  #Manage Transitions (1 is zoom in, 2 is from instructions to difficulty selection)
                        fnPlaySoundEffects(mp3_SmallButtonPressFX)
                        self.startTime = pygame.time.get_ticks()
                        StartTransition = True
                    
                    if Transition_1_Over and not Start_Transition_2 and pygame.time.get_ticks() - TimeWhenTransition_1_Over > 100:
                        fnPlaySoundEffects(mp3_SmallButtonPressFX)
                        fTimeSinceTransition2 = pygame.time.get_ticks()
                        Start_Transition_2 = True                    
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if Transition_2_Over and pygame.time.get_ticks() - fTimeSinceTransition2 > 400 :
                        mousePos = pygame.mouse.get_pos()
                        for button in self.buttons:
                            if button.isClicked(mousePos):
                                fnPlaySoundEffects(mp3_BigButtonPressFX)
                                pygame.mixer.music.stop() #stop music when done
                                RunGame = False 
                                # Returns string depending on the difficulty selected
                                if button == EasyDifficultyButton: 
                                    return 'Easy'
                                elif button == MediumDifficultyButton:
                                    return 'Medium'
                                elif button == HardDifficultyButton:
                                    return 'Hard'


                if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    for button in self.buttons:
                        button.handle_event(event)
                    for button in self.buttons:
                        if button.MouseOver(mousePos) == True:
                            button.mouseover = True  

                                
            if StartTransition: #zoom in to the board
                if pygame.time.get_ticks() - self.presentFrameTime >= self.transitionTime and iCurrentFrameNumber < 5:
                    self.presentFrameTime = pygame.time.get_ticks()
                    iCurrentFrameNumber += 1 

                    if iCurrentFrameNumber == 5:    #draws text (typing animation)
                        self.draw(iCurrentFrameNumber)
                        fnPlaySoundEffects(mp3_KeyboardTypingFX)
                        for line in sInstructions.splitlines():
                            Y_PositionOfCurrentLine += 38
                            for char in range(len(line)+1):
                                time.sleep(.015)
                                TextSurfaceInstructions = InstructionsFont.render(line[:char], True, WHITE)
                                WINDOW.blit(TextSurfaceInstructions, (230, Y_PositionOfCurrentLine, 300, 300 ))                         
                                pygame.display.update()
                        Y_PositionOfCurrentLine = InitialYPositionOfCurrentLine       
                        Transition_1_Over = True
                        StartTransition = False
                        TimeWhenTransition_1_Over = pygame.time.get_ticks()
            

            self.draw(iCurrentFrameNumber) 

            if not StartTransition:  #draw click to continue
                TextSurfaceClickToContinue = Font.render('Click to continue ...', True, WHITE)
                WINDOW.blit(TextSurfaceClickToContinue, (550, 600, 200, 50 ))


            if Transition_1_Over and not Start_Transition_2:
                Y_PositionOfCurrentLine = InitialYPositionOfCurrentLine
                for line in sInstructions.splitlines():
                    Y_PositionOfCurrentLine += 38
                    TextSurfaceInstructions = InstructionsFont.render(line, True, WHITE)
                    WINDOW.blit(TextSurfaceInstructions, (225, Y_PositionOfCurrentLine, 300, 300 ))
                
                TextSurfaceClickToContinue = Font.render('Click to continue ...', True, WHITE)
                WINDOW.blit(TextSurfaceClickToContinue, (550, 600, 200, 50 ))


            if Start_Transition_2:   #draw difficulty buttons
                TextSurfaceInstructions = FontDifficulty.render('Select a difficulty:', True, WHITE)
                WINDOW.blit(TextSurfaceInstructions, (300, InitialYPositionOfCurrentLine+60, 300, 300 ))
                Transition_2_Over = True        
                for button in self.buttons:
                    button.show = True


            pygame.display.update() 
            clock.tick(60)

        pygame.mixer.music.stop() #stop music when exit screen 
    


class GameScreen:
    def __init__(self, name, Difficulty):
        self.image = pygame.image.load(get_image_path('screens', f"{name}.png"))
        self.startTime = pygame.time.get_ticks()
        self.buttons = []
        self.difficulty = Difficulty
        self.music = get_audio_path('music', "GameplayDesperateSituation.mp3")
        self.sAnswer = ''
        self.LettersToGuess = []
        self.LettersGuessed = []
        self.iScore = 1000
        self.sReveal = ''
        self.RevealFont = RevealFont
        self.iRevealYPosition = 134
        self.iErrors = 0

        #   resize image to fit screen dimensions: 
        original_width, original_height = self.image.get_size()
        scale_factor_width = WIDTH / original_width
        scale_factor_height = HEIGHT / original_height
        scale_factor = min(scale_factor_width, scale_factor_height)

        self.scaled_image = pygame.transform.scale(self.image, (int(original_width * scale_factor), int(original_height * scale_factor)))
        self.image_rect = self.scaled_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))


    def fnResetScreen(self): 
        self.startTime = pygame.time.get_ticks()
        self.sAnswer = ''
        self.LettersToGuess.clear() 
        self.LettersGuessed.clear() 
        self.iScore = 1000
        self.sReveal = ''
        self.RevealFont = RevealFont
        self.GuessingFullWord = False
        self.iRevealYPosition = 134
        self.iErrors = 0
        for button in self.buttons:
            button.ResetButton()
        

    def fnDefineNewAnswer(self):
        with open(get_data_path("Dictionary.txt"), "r") as file:
            words = file.read().split("\n")
        self.sAnswer = random.choice(words)

        if self.difficulty == 'Easy': # more than 10 characters long
            self.iRevealYPosition = 165
            self.RevealFont = pygame.font.Font(get_font_path('PIXELADE.TTF'), 45)
            while len(self.sAnswer) < 10 or len(self.sAnswer) > 13: 
                self.sAnswer = random.choice(words)
        
        elif self.difficulty == 'Medium': # 7-9 characters long
            self.iRevealYPosition = 144
            while len(self.sAnswer) > 9 or len(self.sAnswer) < 7: 
                self.sAnswer = random.choice(words)

        elif self.difficulty == 'Hard': # 1-6 characters long
            self.iRevealYPosition = 134
            self.RevealFont = pygame.font.Font(get_font_path('PIXELADE.TTF'), 85)
            while len(self.sAnswer) > 6: 
                self.sAnswer = random.choice(words)

        for char in self.sAnswer: 
            if char not in self.LettersToGuess: 
                self.LettersToGuess.append(char) 

        # print(f'the new word is {self.sAnswer}') <-- UNCOMMENT FOR CHEATING
                

    def fnFormatReveal(self):
        self.sReveal = ''
        for char in self.sAnswer: 
            if char in self.LettersGuessed: 
                self.sReveal += char + ' ' 
            else:
                self.sReveal += '_ ' 


    def fnCheckWin(self):
        #returns true if someone won
        if self.sReveal.replace(' ', '') == self.sAnswer:
            return True

    def draw(self):
        WINDOW.blit(self.scaled_image, self.image_rect)
        WINDOW.blit(RevealSignPNG, (0, 87))
        WINDOW.blit(KeyboardSignPNG, (420, 88))

        TextSurfaceReveal = self.RevealFont.render((self.sReveal), True, BLACK) # Draw Reveal
        # Calculate the x-coordinate to center the Reveal at x=245
        text_width = TextSurfaceReveal.get_width()
        x_centered = 245 - text_width // 2 
        WINDOW.blit(TextSurfaceReveal, (x_centered, self.iRevealYPosition))

        TextSurfaceErrors = Font.render((f"Lives: {str(8 - self.iErrors)}"), True, WHITE) # Draw lives
        WINDOW.blit(TextSurfaceErrors, (150, 0))

        TextSurfaceScore = Font.render((f"Score: {str(self.iScore)}"), True, WHITE) # Draw Score
        WINDOW.blit(TextSurfaceScore, (610, 0))

        GallowsPictures.draw(self.iErrors)   # Draw HangingMan
        
        for button in self.buttons: # Draw all buttons
            button.draw()

        if self.GuessingFullWord:  # Draw special menu for when guessing full word
            WINDOW.blit(FullWordGuessPopUpPNG, (70, 150))

            #Draw instructions in different lines
            TextSurfaceFullWordGuessInstructions = FullWordGuessFont.render(("Guess a word and press Enter to submit."), True, WHITE) 
            WINDOW.blit(TextSurfaceFullWordGuessInstructions, (158, 200))
            TextSurfaceFullWordGuessInstructions2 = FullWordGuessFont.render(("A correct answer will earn you +100 points,"), True, WHITE) 
            WINDOW.blit(TextSurfaceFullWordGuessInstructions2, (135, 240))
            TextSurfaceFullWordGuessInstructions = FullWordGuessFont.render(("but an incorrect answer will result in"), True, WHITE) 
            WINDOW.blit(TextSurfaceFullWordGuessInstructions, (180, 280))
            TextSurfaceFullWordGuessInstructions2 = FullWordGuessFont.render(("an automatic loss."), True, WHITE) 
            WINDOW.blit(TextSurfaceFullWordGuessInstructions2, (345, 320))

            # Center and format the reveal with blank spaces
            TextSurfaceFullWordGuessInputAndSpaces = Font.render(self.FullWordGuessString + '_'*(len(self.sAnswer) -len(self.FullWordGuessString)), True, BLACK)
            text_width = TextSurfaceFullWordGuessInputAndSpaces.get_width()
            x_centered = WIDTH//2 - text_width // 2  
            TextSurfaceFullWordGuessInput = Font.render(self.FullWordGuessString, True, WHITE) 
            text_width = TextSurfaceFullWordGuessInput.get_width()
            WINDOW.blit(TextSurfaceFullWordGuessInput, (x_centered, 420))
            TextSurfaceFullWordGuessInput = FontDifficulty.render('_'*(len(self.sAnswer) -len(self.FullWordGuessString) ), True, WHITE) 
            WINDOW.blit(TextSurfaceFullWordGuessInput, (x_centered + text_width, 420))

        pygame.display.update()
        

    def fnDrawInCountdown(self, sCountdown):
        WINDOW.blit(self.scaled_image, self.image_rect)
        GallowsPictures.draw(self.iErrors)

        WINDOW.blit(CountDownBlackOutPNG, (0,0))  # Dark background to 'blur'

        # Center the countdown text
        TextSurfaceCountdown = CountdownFont.render(str(sCountdown), True, WHITE) 
        text_width, text_height = TextSurfaceCountdown.get_size()
        x_centered = WIDTH//2 - text_width // 2 
        WINDOW.blit(TextSurfaceCountdown, (x_centered, HEIGHT//2 - 40))

        pygame.display.update()


    def fnCountErrors(self):
        # Counts errors and updates 'self.iErrors'
        self.iErrors = 0 
        for char in self.LettersGuessed:
            if char not in self.sAnswer:
                self.iErrors += 1


    def fnCalculateScore(self):
        #Formula to calculate Score: (considering mistakes and time)
        self.iScore = int(1000 - (self.iErrors*100) - (pygame.time.get_ticks()- self.startTime)*.00261)


    def fnCountdown(self):
        # Manages countdown loop
        Run = True
        fnPlaySoundEffects(mp3_CountDownSFX)
        while Run:
            sCountdown = '3'
            fCountdownTime = (pygame.time.get_ticks()- self.startTime)*.001
            if fCountdownTime > 3.5:
                Run = False
            elif fCountdownTime > 3.1:
                sCountdown = 'Go!'
            elif fCountdownTime > 2.1:
                sCountdown = '1'
            elif fCountdownTime > 1.1:
                sCountdown = '2'
            else:
                sCountdown = '3'
            
            self.fnDrawInCountdown(sCountdown)


    def Run(self, difficulty):
        global bMusicOn
        global bSoundEffectsOn
        RunGame = True
        self.difficulty = difficulty
        self.FullWordGuessString = ''

        self.fnResetScreen()
        self.fnDefineNewAnswer()
        self.fnFormatReveal()
        self.fnCountdown()

        if bMusicOn: 
            fnPlayMusic(self.music)

        self.startTime = pygame.time.get_ticks()
        while RunGame == True:
            for button in self.buttons:
                button.clicked = False
                button.mouseover = False

            for event in pygame.event.get(): # Huge event pump
                if event.type == pygame.QUIT:
                    #RunGame = True
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mousePos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.isClicked(mousePos):
                            # Keyboard Buttons
                            if button.purpose == 'Keyboard' and not button.hide and not self.GuessingFullWord:
                                button.hide = True
                                for key, value in KeyboardButtonsDictionary.items():
                                    if value == button:
                                        letter = key.lower()
                                        self.LettersGuessed.append(letter)
                                self.fnFormatReveal()                
                                self.fnCountErrors()
                                self.fnCalculateScore()

                            # Music/SoundFX ON/OFF
                            elif button == MusicOFFButtonGameScreen and MusicOFFButtonGameScreen.show:
                                MusicONButtonGameScreen.show, MusicONButtonGameScreen.hide = True, False
                                button.show = False
                                button.hide = True
                                bMusicOn = True
                                fnPlayMusic(self.music)
                            elif button == MusicONButtonGameScreen and MusicONButtonGameScreen.show:
                                MusicOFFButtonGameScreen.show, MusicOFFButtonGameScreen.hide = True, False
                                button.show = False
                                button.hide = True
                                bMusicOn = False
                                pygame.mixer.music.stop()

                            elif button == SoundEffectsOFFButtonGameScreen and SoundEffectsOFFButtonGameScreen.show:
                                SoundEffectsONButtonGameScreen.show, SoundEffectsONButtonGameScreen.hide = True, False
                                button.show = False
                                button.hide = True
                                bSoundEffectsOn = True
                            elif button == SoundEffectsONButtonGameScreen and SoundEffectsONButtonGameScreen.show:
                                SoundEffectsOFFButtonGameScreen.show, SoundEffectsOFFButtonGameScreen.hide = True, False
                                button.show = False
                                button.hide = True
                                bSoundEffectsOn = False

                            elif button == FullWordGuessButton:
                                self.FullWordGuessString = ''
                                self.GuessingFullWord = not self.GuessingFullWord
                            break

                elif event.type == pygame.KEYDOWN:  # Takes in input from keyboard
                    if not self.GuessingFullWord:   # Normal keyboard input
                        letter = str(event.unicode).upper()
                        if letter.isalpha() and letter.lower() not in self.LettersGuessed:
                            fnPlaySoundEffects(mp3_SmallButtonPressFX)
                            button = KeyboardButtonsDictionary[letter]
                            button.hide = True
                            self.LettersGuessed.append(letter.lower())
                            self.fnFormatReveal()                
                            self.fnCountErrors()
                            self.fnCalculateScore()
                        elif letter.lower() in self.LettersGuessed:
                            fnPlaySoundEffects(mp3_BlockedFX)

                    else:     #Keyboard input while guessing full word
                        if event.key == pygame.K_RETURN:
                            self.GuessingFullWord = False  # Stop recording when Enter is pressed
                            if self.FullWordGuessString.lower() == self.sAnswer:
                                return (self.iScore+100, self.sAnswer)
                            else:
                                return (0, self.sAnswer)
                            
                        elif event.key == pygame.K_BACKSPACE:
                            self.FullWordGuessString = self.FullWordGuessString[:-1]  # Remove the last character when Backspace is pressed
                        elif event.key == pygame.K_SPACE and len(self.FullWordGuessString) < len(self.sAnswer):
                            self.FullWordGuessString += '_'
                        elif event.unicode.isalpha() and len(self.FullWordGuessString) < len(self.sAnswer):
                            self.FullWordGuessString += event.unicode  # Append the character to the user input string


                if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    for button in self.buttons:
                        if button.purpose != "Keyboard" or not self.GuessingFullWord:
                            button.handle_event(event)
                            
            
            self.fnCalculateScore()
             

            if self.iErrors > 7 or self.iScore < 1:
                RunGame = False
                return (0, self.sAnswer)

            if self.fnCheckWin(): # Check Win
                RunGame = False
                pygame.mixer.music.stop()
                self.fnCountErrors()
                self.fnCalculateScore()
                return (self.iScore, self.sAnswer)

            self.draw() #draw everything (gallows, reveal, errors, and screen and full word guess menu)
            clock.tick(20) # conservative clock tick due to higher processing demands

        pygame.mixer.music.stop()  



class VictoryScreen: 
    def __init__(self):
        global iHighestScore
        self.image = pygame.image.load(get_image_path('screens', "VictoryScreen.png"))
        self.buttons = []
        self.font = CountdownFont
        self.BigText = ''
        self.mediumText = '' 
        self.additionaltext = ''
        self.mediumTextFont = InstructionsFont

       #   resize images to fit screen dimensions: 
        original_width, original_height = self.image.get_size()
        scale_factor_width = WIDTH / original_width
        scale_factor_height = HEIGHT / original_height
        scale_factor = min(scale_factor_width, scale_factor_height)

        self.scaled_image = pygame.transform.scale(self.image, (int(original_width * scale_factor), int(original_height * scale_factor)))
        self.image_rect = self.scaled_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def fnResetScreen(self):
        self.font = CountdownFont
        self.BigText = ''
        self.mediumText ='' 
        self.additionaltext = ''

        for button in self.buttons:
            button.ResetButton()


    def draw(self):
        WINDOW.blit(self.scaled_image, self.image_rect)  # draw image

        TextSurface = CountdownFont.render(self.BigText, True, WHITE) #draw Win/lose big message
        WINDOW.blit(TextSurface, (320, 150))

        TextSurface = self.mediumTextFont.render(self.mediumText, True, WHITE) # draw second line
        WINDOW.blit(TextSurface, (335, 250))

        TextSurface = InstructionsFont.render(self.additionaltext, True, WHITE) # draw third line
        WINDOW.blit(TextSurface, (320, 300))
    
        for button in self.buttons: # draw buttons
            button.draw()


    def Run(self, score, sAnswer):
        global iHighestScore
        RunGame = True

        self.fnResetScreen()

        # Create custom text depending on the score
        if score > 0: 
            fnPlaySoundEffects(mp3_WinFanfareFX)
            self.music = get_audio_path('music', "VictoryScreen-Indy and Sophia's Kiss.mp3")
            self.BigText = 'YOU WIN!'
            self.mediumText = f"Your score was: {score}"
        else :
            self.music = get_audio_path('music', "LooseScreen-Ominous Feeling.mp3")
            self.BigText = "YOU LOSE!"
            self.mediumText = f"The word was: {sAnswer}"
            if len(sAnswer) > 11:
                self.mediumTextFont = pygame.font.Font(get_font_path('PIXELADE.TTF'), 35)

        if score > iHighestScore:
            self.additionaltext = "You've set a new high score!"
            iHighestScore = score

        if bMusicOn: 
            fnPlayMusic(self.music)

        while RunGame == True:
            for button in self.buttons:
                button.clicked = False
                button.mouseover = False

            for event in pygame.event.get():   # event pump
                mousePos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mousePos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.isClicked(mousePos):
                            pygame.mixer.music.stop() #stop music when done
                            fnPlaySoundEffects(mp3_BigButtonPressFX)  #transition between screens
                            RunGame = False
                            if button == PlayAgainButton:
                                return True  #returns true to play again
                            elif button == BackToMenuButton:
                                return False   #returns false for back to menu

                if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    for button in self.buttons:
                        button.handle_event(event)
                  
            self.draw() 

            pygame.display.update()
            clock.tick(60)

        pygame.mixer.music.stop() #stop music when done


# Initialize Screens classes instances

TitleScreen_Hangman = TitleScreen('TitleScreen_Hangman')
Instructions_Screen = InstructionsScreen('InstructionsBoard')
GamePlay_Screen = GameScreen('GameScreen', 'Easy')
Victory_Screen = VictoryScreen()



class Button:
    Buttons = []
    def __init__(self, x, y, width, height, text, BelongingScreen, purpose, show, button_image_normal, button_image_hovered, button_image_pressed, textcolor, SoundEffect, font =pygame.font.Font(get_font_path('PIXELADE.TTF'), 55) ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.pressed = False
        self.belongingscreen = BelongingScreen
        self.purpose = purpose 
        self.original_Show = show
        self.show = show
        self.mouseover = False
        self.state = "normal"
        self.originalimage = button_image_normal
        self.textcolor = textcolor
        self.hide = False
        self.SoundEffect = SoundEffect

        # resize images to match the inputted rectangles dimensions
        self.original_width, self.original_height = self.originalimage.get_size()
        self.scale_factor_width = width / self.original_width
        self.scale_factor_height = height / self.original_height
        scale_factor = min(self.scale_factor_width, self.scale_factor_height)

        self.image_normal =  pygame.transform.scale(button_image_normal, (int(self.original_width * scale_factor), int(self.original_height * scale_factor)))
        self.image_hovered = pygame.transform.scale(button_image_hovered, (int(self.original_width * scale_factor), int(self.original_height * scale_factor)))
        self.image_pressed = pygame.transform.scale(button_image_pressed, (int(self.original_width * scale_factor), int(self.original_height * scale_factor)))
    
        self.belongingscreen.buttons.append(self)

        Button.Buttons.append(self)
    
    def ResetButton(self):
        self.pressed = False
        self.mouseover = False
        self.state = "normal"
        self.hide = False

        if self.purpose == 'MusicOn':
            if bMusicOn:
                self.show = True
                self.hide = False
            elif not bMusicOn:
                self.show = False
                self.hide = True
        elif self.purpose == 'MusicOff':
            if bMusicOn:
                self.show = False
                self.hide = True
            elif not bMusicOn:
                self.show = True
                self.hide = False

        elif self.purpose == 'SoundEffectsOn':
            if bSoundEffectsOn:
                self.show = True
                self.hide = False
            elif not bSoundEffectsOn:
                self.show = False
                self.hide = True
        elif self.purpose == 'SoundEffectsOff':
            if bSoundEffectsOn:
                self.show = False
                self.hide = True
            elif not bSoundEffectsOn:
                self.show = True
                self.hide = False

        else:     
            self.show = self.original_Show
            self.hide = False


    def MouseOver(self, mousePos):
        return self.rect.collidepoint(mousePos)


    def isClicked(self, mousePos):
        if not self.show:
            return False
        return self.rect.collidepoint(mousePos)


    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.update_state(event.pos, self.pressed)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.pressed = True
            self.update_state(event.pos, self.pressed)
            if self.isClicked(event.pos):
                fnPlaySoundEffects(self.SoundEffect)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False
            self.update_state(event.pos, pressed=False)

            
    def update_state(self, mouse_pos, pressed=False):
        if self.rect.collidepoint(mouse_pos):
            if pressed:
                self.state = "pressed" #first time it changes state to pressed
            elif self.state == "pressed":
                self.state = "hovered"
            else:
                self.state = "hovered"
        else:
            self.state = "normal"


    def draw(self):
        if self.show: # draw the correct state 
            if self.hide:
                WINDOW.blit(self.image_pressed, self.rect)
            elif self.state == "pressed":
                WINDOW.blit(self.image_pressed, self.rect)
            elif self.state == "hovered":
                WINDOW.blit(self.image_hovered, self.rect)
            else:
                WINDOW.blit(self.image_normal, self.rect)

            TextSurface = self.font.render(self.text, True, self.textcolor)
            TextRect = TextSurface.get_rect(center = self.rect.center)

            WINDOW.blit(TextSurface, TextRect)
        
# Create Keyboard Buttons Dictionaries
KeyboardLockPNGImagesDictionary = {}
KeyboardPressPNGImagesDictionary = {} #hovered
KeyboardReleasePNGImagesDictionary = {} # pressed
KeyboardButtonsDictionary = {}

# define keyboard variables
KeyBoardButtonsSizeHeight = 60
KeyboardLettersXPosition = 480
KeyboardLettersYPosition = 105
iImageYPosition = KeyboardLettersYPosition


# Load images and Initialize BUTTONS: -------------------------------------------------------------------------------------------------------------
# Arguments for buttons:  Button __init__(self, x, y, width, height, text, BelongingScreen, purpose, show, button_image_normal, button_image_hovered, button_image_pressed)

for letter in AlphabetList: #creates buttons for the keyboard
    n = AlphabetList.index(letter)
    if n == 0 or n == 7 or n == 14 or n ==21:
        iImageXPosition = KeyboardLettersXPosition
        iImageYPosition += KeyBoardButtonsSizeHeight + 20
        if n == 21:
            iImageXPosition += 50

    letter = letter.upper()
    KeyboardLockPNGImagesDictionary[letter] = pygame.image.load(get_image_path('buttons', f"Normal{letter}.png"))
    width, height = KeyboardLockPNGImagesDictionary[letter].get_width(), KeyboardLockPNGImagesDictionary[letter].get_height()
    ImageAspectRatio = width/height

    KeyboardPressPNGImagesDictionary[letter] = pygame.image.load(get_image_path('buttons', f"Hover{letter}.png"))
    KeyboardReleasePNGImagesDictionary[letter] = pygame.image.load(get_image_path('buttons', f"Press{letter}.png"))
    KeyboardButtonsDictionary[letter] = Button(iImageXPosition , iImageYPosition, ImageAspectRatio*KeyBoardButtonsSizeHeight, KeyBoardButtonsSizeHeight, '', GamePlay_Screen, 'Keyboard', True, KeyboardLockPNGImagesDictionary[letter], KeyboardPressPNGImagesDictionary[letter], KeyboardReleasePNGImagesDictionary[letter], BLACK, mp3_SmallButtonPressFX)   

    iImageXPosition += ImageAspectRatio*KeyBoardButtonsSizeHeight + 20 # move each letter 20 apart from each other


PNGPlayButtonLock = pygame.image.load(get_image_path('buttons', "play01.png"))
PNGPlayButtonPress = pygame.image.load(get_image_path('buttons', "play02.png"))
PNGPlayButtonRelease = pygame.image.load(get_image_path('buttons', "play03.png"))
PlayButton = Button(WIDTH//2 - 240//2 , 520, 240, 95, '', TitleScreen_Hangman, 'Play', True, PNGPlayButtonLock, PNGPlayButtonPress, PNGPlayButtonRelease, BLACK, mp3_SmallButtonPressFX)


# Music/SoundFX Buttons/variables/images:
MusicAndSoundButtonsSize = 100 #width For title screen buttons
MusicAndSoundButtonsSizeGameScreen = 80 #width for game screen buttons
MusicONButtonRatio = 1.14136126 #height over width
MusicOFFButtonRatio = 1.09549072 #height / width

PNGMusicONButtonLock = pygame.image.load(get_image_path('buttons', "MusicButtonON.png"))
PNGMusicONButtonPress = pygame.image.load(get_image_path('buttons', "MusicButtonON-Hovered.png"))
PNGMusicONButtonRelease = pygame.image.load(get_image_path('buttons', "MusicButtonON-Clicked.png"))
PNGMusicOFFButtonLock = pygame.image.load(get_image_path('buttons', "MusicButtonOFF.png"))
PNGMusicOFFButtonPress = pygame.image.load(get_image_path('buttons', "MusicButtonOFF-Hovered.png"))
PNGMusicOFFButtonRelease = pygame.image.load(get_image_path('buttons', "MusicButtonOFF-Clicked.png"))
# Button __init__(self, x, y, width, height, text, BelongingScreen, purpose, show, button_image_normal, button_image_hovered, button_image_pressed)
MusicONButtonTitleScreen = Button(770, 550, MusicAndSoundButtonsSize  , MusicAndSoundButtonsSize*MusicONButtonRatio, '', TitleScreen_Hangman, 'MusicOn', True, PNGMusicONButtonLock, PNGMusicONButtonPress, PNGMusicONButtonRelease, BLACK, mp3_SmallButtonPressFX)
MusicOFFButtonTitleScreen = Button(770, 550, MusicAndSoundButtonsSize  , MusicAndSoundButtonsSize*MusicOFFButtonRatio, '', TitleScreen_Hangman, 'MusicOff', False,PNGMusicOFFButtonLock, PNGMusicOFFButtonPress, PNGMusicOFFButtonRelease, BLACK, mp3_SmallButtonPressFX)
MusicONButtonGameScreen = Button(720, 600, MusicAndSoundButtonsSizeGameScreen  , MusicAndSoundButtonsSizeGameScreen*MusicONButtonRatio, '', GamePlay_Screen, 'MusicOn', True, PNGMusicONButtonLock, PNGMusicONButtonPress, PNGMusicONButtonRelease, BLACK, mp3_SmallButtonPressFX)
MusicOFFButtonGameScreen = Button(720, 600, MusicAndSoundButtonsSizeGameScreen  , MusicAndSoundButtonsSizeGameScreen*MusicOFFButtonRatio, '', GamePlay_Screen, 'MusicOff', False,PNGMusicOFFButtonLock, PNGMusicOFFButtonPress, PNGMusicOFFButtonRelease, BLACK, mp3_SmallButtonPressFX)


PNGSoundEffectsONButtonLock = pygame.image.load(get_image_path('buttons', "SoundEffectsButtonON.png"))
PNGSoundEffectsONButtonPress = pygame.image.load(get_image_path('buttons', "SoundEffectsButtonON-Hovered.png"))
PNGSoundEffectsONButtonRelease = pygame.image.load(get_image_path('buttons', "SoundEffectsButtonON-Clicked.png"))
PNGSoundEffectsOFFButtonLock = pygame.image.load(get_image_path('buttons', "SoundEffectsButtonOFF.png"))
PNGSoundEffectsOFFButtonPress = pygame.image.load(get_image_path('buttons', "SoundEffectsButtonOFF-Hovered.png"))
PNGSoundEffectsOFFButtonRelease = pygame.image.load(get_image_path('buttons', "SoundEffectsButtonOFF-Clicked.png"))

SoundEffectsONButtonTitleScreen = Button(85, 550, MusicAndSoundButtonsSize  , MusicAndSoundButtonsSize*MusicONButtonRatio, '', TitleScreen_Hangman, 'SoundEffectsOn', True, PNGSoundEffectsONButtonLock, PNGSoundEffectsONButtonPress, PNGSoundEffectsONButtonRelease, BLACK, mp3_SmallButtonPressFX)
SoundEffectsOFFButtonTitleScreen = Button(85, 550, MusicAndSoundButtonsSize  , MusicAndSoundButtonsSize*MusicOFFButtonRatio, '', TitleScreen_Hangman, 'SoundEffectsOff', False,PNGSoundEffectsOFFButtonLock, PNGSoundEffectsOFFButtonPress, PNGSoundEffectsOFFButtonRelease, BLACK, mp3_SmallButtonPressFX)
SoundEffectsONButtonGameScreen = Button(150, 600, MusicAndSoundButtonsSizeGameScreen  , MusicAndSoundButtonsSizeGameScreen*MusicONButtonRatio, '', GamePlay_Screen, 'SoundEffectsOn', True, PNGSoundEffectsONButtonLock, PNGSoundEffectsONButtonPress, PNGSoundEffectsONButtonRelease, BLACK, mp3_SmallButtonPressFX)
SoundEffectsOFFButtonGameScreen = Button(150, 600, MusicAndSoundButtonsSizeGameScreen  , MusicAndSoundButtonsSizeGameScreen*MusicOFFButtonRatio, '', GamePlay_Screen, 'SoundEffectsOff', False,PNGSoundEffectsOFFButtonLock, PNGSoundEffectsOFFButtonPress, PNGSoundEffectsOFFButtonRelease, BLACK, mp3_SmallButtonPressFX)


# More buttons: 
PNGFullWordGuessButtonLock = pygame.image.load(get_image_path('buttons', "FullWordGuessButtonNormal.png"))
PNGFullWordGuessButtonPress = pygame.image.load(get_image_path('buttons', "FullWordGuessButtonHovered.png"))
PNGFullWordGuessButtonRelease = pygame.image.load(get_image_path('buttons', "FullWordGuessButtonPressed.png"))
FullWordGuessButton = Button(250, 600,  450 , 90 , 'Full Word Guess', GamePlay_Screen, 'FullWordGuess', True, PNGFullWordGuessButtonLock, PNGFullWordGuessButtonPress,PNGFullWordGuessButtonRelease, WHITE, mp3_SmallButtonPressFX)

PNGDifficultySelectionButtonLock = pygame.image.load(get_image_path('buttons', "UI_Flat_Select_01a1.png"))
PNGDifficultySelectionButtonPress = pygame.image.load(get_image_path('buttons', "UI_Flat_Select_01a2.png"))
PNGDifficultySelectionButtonRelease = pygame.image.load(get_image_path('buttons', "UI_Flat_Select_01a3.png"))

EasyDifficultyButton = Button(WIDTH//2 - 100//2 - 170 , 300, 120, 120, 'Easy', Instructions_Screen, 'DifficultyLevel', False, PNGDifficultySelectionButtonLock, PNGDifficultySelectionButtonPress, PNGDifficultySelectionButtonRelease, WHITE, mp3_SmallButtonPressFX)
MediumDifficultyButton = Button(WIDTH//2 - 100//2 , 300, 120, 120, 'Medium', Instructions_Screen, 'DifficultyLevel', False, PNGDifficultySelectionButtonLock, PNGDifficultySelectionButtonPress, PNGDifficultySelectionButtonRelease, WHITE, mp3_SmallButtonPressFX)
HardDifficultyButton = Button(WIDTH//2 - 100//2 + 170 , 300, 120, 120, 'Hard', Instructions_Screen, 'DifficultyLevel', False, PNGDifficultySelectionButtonLock, PNGDifficultySelectionButtonPress, PNGDifficultySelectionButtonRelease, WHITE, mp3_SmallButtonPressFX)
    
PNGPlayVictoryScreenLock = pygame.image.load(get_image_path('buttons', "VictoryScreenButtonNormal.png"))
PNGPlayVictoryScreenPress = pygame.image.load(get_image_path('buttons', "VictoryScreenButtonHovered.png"))
PNGPlayVictoryScreenRelease = pygame.image.load(get_image_path('buttons', "VictoryScreenButtonPressed.png"))

PlayAgainButton = Button(705 , 187, 181, 67, 'Play again', Victory_Screen, 'PlayAgain', True, PNGPlayVictoryScreenLock, PNGPlayVictoryScreenPress, PNGPlayVictoryScreenRelease, WHITE, mp3_SmallButtonPressFX, InstructionsFont)
BackToMenuButton = Button(705 , 259, 181, 67, 'Back to Menu', Victory_Screen, 'BackToMenu', True, PNGPlayVictoryScreenLock, PNGPlayVictoryScreenPress, PNGPlayVictoryScreenRelease, WHITE, mp3_SmallButtonPressFX, pygame.font.Font(get_font_path('PIXELADE.TTF'), 35) )



#_____________FUNCTIONS________________________________________________________________________________________________________________

def fnPlayMusic(SoundFile):
    # Takes in soundfile name (string) argument and plays the song indefinitely
    if bMusicOn: 
        pygame.mixer.music.load(SoundFile)
        pygame.mixer.music.play(-1)

def fnPlaySoundEffects(SoundFile):
    # Takes in soundfile argument (loaded) and plays it once
    if bSoundEffectsOn: 
        SoundFile.play()


def TitleAndInstructions():
    # Plays the title and instructions screens and returns string of difficulty
    TitleScreen_Hangman.Run()
    return Instructions_Screen.Run()

def GameAndVictory(Difficulty):
    # takes in string of difficulty and runs the game with that difficulty indefinitely. If player returns to title screen, returns false.
    iScore, sAnswer = GamePlay_Screen.Run(Difficulty)
    while Victory_Screen.Run(iScore, sAnswer):
        iScore, sAnswer = GamePlay_Screen.Run(Difficulty)
    return False


def RunFullGame():
    # Runs game indefinitely until window is exited.
    Run = True
    Difficulty = TitleAndInstructions()
    while Run:
        if GameAndVictory(Difficulty) == False:
            Difficulty = TitleAndInstructions()



#_____________MAIN________________________________________________________________________________________________________________

if __name__ == "__main__":
    RunFullGame()
