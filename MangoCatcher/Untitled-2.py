# Frozen Jam by tgfcoder https://twitter.com/tgfcoder licensed under CC-BY-3

import pygame
import os
import random
import time

pygame.init()
pygame.font.init()
pygame.mixer.init()

test_list = [250, 500, 750, 1000] #Potential intervals to drop mangos (in milliseconds)
WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #Draw window for game
pygame.display.set_caption("Tuffy Catches Mangoes") #Title of window

#RGB COLOR CODES----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
Tuffy = (255, 255, 0)

SCORE_FONT = pygame.font.SysFont('comicsans', 40)
LIFE_FONT =  pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)


FPS = 60
VEL = 3
BULLET_VEL = 3
tuffy_Width, tuffy_Height = 192, 192
MANGO_WIDTH, MANGO_HEIGHT = 80, 80
catch = pygame.USEREVENT + 1
miss = pygame.USEREVENT +2
spawn = pygame.USEREVENT +3

TUFFY_ART = pygame.image.load( #Load elephant image
    os.path.join('Assets', 'Tuffy01.png'))
TUFFY = pygame.transform.scale( #Change elephant  size
    TUFFY_ART, (tuffy_Width, tuffy_Height))
MANGO_IMAGE = pygame.image.load( #Load the mango
    os.path.join('Assets', 'mango01.png'))
MANGO = pygame.transform.scale( #Take the loaded mango and scale it
    MANGO_IMAGE, (MANGO_WIDTH, MANGO_HEIGHT))
SPACE = pygame.transform.scale(pygame.image.load( #Background
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

#*********DISPLAY*********#
def draw_window( Tuffy,  falling_mangos, score, life):
    WIN.blit(SPACE, (0, 0))
    score_text = SCORE_FONT.render( "SCORE: " + str(score), 1, WHITE)
    life_text = LIFE_FONT.render ("LIFE: " + str(life), 1, RED)
    WIN.blit(score_text, (10, 10))
    WIN.blit(life_text, (10, 45))
    WIN.blit(TUFFY, (Tuffy.x, Tuffy.y))
    for bullet in falling_mangos:
        WIN.blit(MANGO, (bullet.x, bullet.y))
    pygame.display.update()

#**********MOVEMENT**********#
def handle_tuffy_movement(keys_pressed, Tuffy):
    if keys_pressed[pygame.K_LSHIFT] and keys_pressed[pygame.K_LEFT] and Tuffy.x - VEL > 0: # LEFT DASH
        Tuffy.x -= 1.25*VEL
    if keys_pressed[pygame.K_LSHIFT] and keys_pressed[pygame.K_RIGHT] and Tuffy.x + VEL + Tuffy.width < 900: # RIGHT DASH
        Tuffy.x += 1.25*VEL
    if keys_pressed[pygame.K_LEFT] and Tuffy.x - VEL > 0:  # LEFT
        Tuffy.x -= VEL     
    if keys_pressed[pygame.K_RIGHT] and Tuffy.x + VEL  < 900:  # RIGHT
        Tuffy.x += VEL

#*********FRUIT*********#
def handle_mangos(falling_mangos, Tuffy):
    for bullet in falling_mangos:
        bullet.y += BULLET_VEL
        if Tuffy.colliderect(bullet): #WE CATCH IT
            pygame.event.post(pygame.event.Event(catch))
            falling_mangos.remove(bullet)
        elif bullet.y > 750: #WE DONT CATCH
            pygame.event.post(pygame.event.Event(miss))
            falling_mangos.remove(bullet) 

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    Tuffy = pygame.Rect(354, 708, tuffy_Width, tuffy_Height)
    falling_mangos = []
    score = 0
    life = 13
    clock = pygame.time.Clock()
    start_ticks=pygame.time.get_ticks()
    pygame.time.set_timer(spawn , random.choice(test_list))
    while True:

        for event in pygame.event.get():
            if event.type == spawn:
                mango = pygame.Rect(random.randint(0, 820), -100, 80, 40)
                falling_mangos.append(mango)
                
                break
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
         
            if event.type == catch:
                score += 1
            
            if event.type == miss:
                life -= 1
    
        keys_pressed = pygame.key.get_pressed()
        handle_tuffy_movement(keys_pressed, Tuffy)
       

        handle_mangos(falling_mangos, Tuffy)

        draw_window(Tuffy, falling_mangos,
                     score, life)

    main()

if __name__ == "__main__":
    main()
