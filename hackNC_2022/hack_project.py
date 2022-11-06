"""College Clicker Game."""
import pygame
import math
import time
from pygame.sprite import Sprite
from pygame.rect import Rect
pygame.init()



# Color Library (RGB)
black = (0, 0, 0)
white = (255, 255, 255)
background = (207, 226, 245)
baby_blue = (137, 207, 240)
kinda_blue = (0, 111, 255)
magenta = (172, 0, 235)
red_255 = (255, 13, 13)
red_255_78 = (255, 78, 17)
orange_255 = (255, 142, 21)
orange_250 = (250, 183, 51)
green_172 = (172, 179, 52)
green_105 = (105, 179, 76)
gold = (226, 177, 60)

#music/sound 
music = pygame.mixer.music.load("backgroundmusic.mp3")
click_sound = pygame.mixer.Sound(("clicknoise.mp3"))
pygame.mixer.music.play(-1)


# size of game screen in pixels
size = width, height = 1000, 1000

# create screen + set its size
screen = pygame.display.set_mode(size)
# set title(?)
pygame.display.set_caption("College Clicker")
font = pygame.font.Font('font.ttf', 16)
title_font = pygame.font.Font('font.ttf', 40)

#Background 
background = pygame.image.load("classroom.png")
pygame.draw.rect(screen, white, [0, 800, 1000, 200])

### insert other preset variables [framerate + timer]


#Characters 
girlandguy = pygame.image.load('student.png')
girlandguyrect = girlandguy.get_rect()

# bottom buttons images
food_img = pygame.image.load('fries.png')
friends_img = pygame.image.load('banana.png')
study_img = pygame.image.load('book.png')
girl_img = pygame.image.load('girl.png')
male_img = pygame.image.load('male.png')
sleep_img = pygame.image.load('snooze1.png')


# initialize game variables 
max_amt = 18
happiness = max_amt
school_performance = max_amt
sleep = max_amt
day = 0

# char image variables 
characterlist = ["student.png", "girl.png", "male.png"]


def regular_decrease():
    global happiness
    happiness -= 1
    global school_performance
    school_performance -= 1
    global sleep
    sleep -= 1

def button_bar_change(happy, school, energy):
    global happiness
    happiness += happy
    if happiness > max_amt:
        happiness = max_amt
    global school_performance
    school_performance += school
    if school_performance > max_amt:
        school_performance = max_amt
    global sleep
    sleep += energy
    if sleep > max_amt:
        sleep = max_amt


def draw_rectangle(y_coord, amount, name):
    #display basic bar
    pygame.draw.rect(screen, white, [40, y_coord - 30, 220, 50])
    pygame.draw.rect(screen, black, [52, y_coord - 23, 196, 36])
    pygame.draw.rect(screen, white, [55, y_coord - 20, 190, 30])

    #display how full the bar is
    blocksnum = math.ceil(amount/(max_amt/6))
    y_corner = y_coord - 20
    colorslist = [red_255, red_255_78, orange_255, orange_250, green_172, green_105]
    coordslist = [[55, y_corner, 32, 30], [87, y_corner, 32, 30], [119, y_corner, 32, 30], [151, y_corner, 31, 30], [182, y_corner, 31, 30], [213, y_corner, 32, 30]]
    for a in range(0, blocksnum):
        pygame.draw.rect(screen, colorslist[a], coordslist[a])

    #display bar title 
    text = font.render(name, True, black)
    screen.blit(text, (40, y_coord - 50))

    


    
class Button(): #button class
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and click conditions
        if self.rect.collidepoint(pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                action = True

        # draws button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


girl = Button(200, 300, girl_img, .5)
boy = Button(600, 300, male_img, .5)

choosing = True
charnum = 0
while choosing:
    screen.fill(white)
    text = title_font.render("Choose your Student", True, black)
    screen.blit(text, (125, 150))

    gclicked = girl.draw(screen)
    bclicked = boy.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            choosing = False
            pygame.quit()
        if gclicked:
            charnum = 1
            choosing = False
        if bclicked:
            charnum = 2
            choosing = False
    pygame.display.flip()

char_select_time = time.time()

chosen_char_img = pygame.image.load(characterlist[charnum])
chosen_char = pygame.transform.scale(chosen_char_img, (int(chosen_char_img.get_width() * 0.5), int(chosen_char_img.get_height() * 0.5)))
chosen_char_rect = chosen_char.get_rect()
chosen_char_rect.topleft = (400, 235)
    

# create button instances
food_button = Button(150, 600, food_img, .22)
friends_button = Button(350, 600, friends_img, .15)
study_button = Button(620, 590, study_img, .38)
sleep_button = Button(770, 300, sleep_img, .34)

running = True
last_time = 0
game_over = False
game_time = -1
while running:
    #game over screen
    if happiness <= 0 or school_performance <= 0 or sleep <= 0:
        if game_over is False:
            game_time = pygame.time.get_ticks()
            game_over = True
        if pygame.time.get_ticks() - game_time >= 5000:
            running = False
        
        if happiness <= 0:
            death_cause = "sadness"
        elif school_performance <= 0:
            death_cause = "shame"
        else:
            death_cause = "fatigue"

        day_text = str(day) + " days"
        if day == 1:
            day_text = "1 day"

        screen.fill(black)
        game_over_text = title_font.render("Game Over", True, white)
        days_text = font.render("You lasted " + day_text, True, white)
        cause_of_death_text = font.render("You died of " + death_cause, True, white)
        goodbye_text = title_font.render("Goodbye", True, white)

        screen.blit(game_over_text, (300, 100))
        screen.blit(days_text, (350, 300))
        screen.blit(cause_of_death_text, (315, 400))
        screen.blit(goodbye_text, (340, 600))
        pygame.display.flip()
        continue

    #background loop
    screen.blit(background, (0,0))
    pygame.draw.rect(screen, gold, [145, 595, 710, 210])
    pygame.draw.rect(screen, white, [150, 600, 700, 200])
    #start and stop button 
    #start_button
    # button drawn
    foodclick = food_button.draw(screen)
    friendclick = friends_button.draw(screen)
    studyclick = study_button.draw(screen)
    sleepclick = sleep_button.draw(screen)
    
    #if the game is closed/somehow quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #while loop ends
            running = False

        # button clicked
        if foodclick:
            button_bar_change(0, 0, 2)
        if friendclick: 
            button_bar_change(4, -1, -1)
        if studyclick: 
            button_bar_change(-1, 4, -1)
        if sleepclick:
            button_bar_change(0, -2, 6)
            
    # decreases bars
    runtime = time.time() - char_select_time
    if math.floor(runtime) > last_time:
        regular_decrease()
        day = math.floor(runtime / 10)
        last_time += 1

    #display bars
    draw_rectangle(80, happiness, "Happiness") # initial one was +80 larger instead of +60 for fixing purposes
    draw_rectangle(160, school_performance, "School")
    draw_rectangle(240, sleep, "Energy")

    screen.blit(chosen_char, chosen_char_rect)

    days_counter_text = font.render("Days: " + str(day), True, white)
    screen.blit(days_counter_text, (870, 25))

    #idk what this is for tbh it's just at the end of the while loop
    pygame.display.flip()



#ends game
pygame.display.quit()
pygame.quit()

