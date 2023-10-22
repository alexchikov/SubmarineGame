import pygame as pg
import random as rnd
from sys import exit
from math import e, log
from pygame.locals import *

pg.init()
pg.display.set_caption('Submarine game')

WIDTH, HEIGHT = 800, 200
FPS = 60

SHARK_X = 900
SHARK_Y = rnd.randint(1,150)

SPEED = 0.0
SPEED_INCREASE = 0.0
SCORE = 1

screen = pg.display.set_mode(size=(WIDTH, HEIGHT))
clock = pg.time.Clock()
sprites = pg.sprite.Group()

surface = pg.image.load('./images/Background.png')
background = pg.transform.scale(surface, size=(WIDTH, HEIGHT))

class Star(pg.sprite.Sprite):
    def __init__(self, x, y, size: tuple=(50,50)) -> None:
        pg.sprite.Sprite.__init__(self, sprites)
        self.star_surface = pg.image.load('./images/Star.png')
        self.image = pg.transform.scale(self.star_surface, size)
        self.rect = self.image.get_rect(center=(x,y))
    
    def update(self):
        self.speed = log(SCORE, e)*1.5
        self.check()
        
    def check(self):
        if self.rect.x < -76:
            self.rect.x = 810
            self.rect.y = rnd.randint(1,150)
        else:
            self.rect.x -= self.speed
            
class Shark(pg.sprite.Sprite):
    def __init__(self, x, y, size: tuple=(100,60)) -> None:
        pg.sprite.Sprite.__init__(self, sprites)
        self.shark_surface = pg.image.load('./images/Shark.png')
        self.image = pg.transform.scale(self.shark_surface, size)
        self.rect = self.image.get_rect(center=(x,y))
    
    def update(self):
        self.speed = log(SCORE, e)*1.5
        if self.rect.x < -76:
            self.rect.x = 810
            self.rect.y = rnd.randint(1,150)
        else:
            self.rect.x -= self.speed
        
class Submarine(pg.sprite.Sprite):
    def __init__(self, x, y, size: tuple=(100,75)) -> None:
        pg.sprite.Sprite.__init__(self, sprites)
        self.submarine_surface  = pg.image.load('./images/Submarine.png')
        self.submarine = pg.transform.scale(self.submarine_surface, size=size)
        self.image = pg.transform.flip(surface=self.submarine, flip_x=1, flip_y=0).convert_alpha()
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = SPEED
    
    def check(self):
        if self.rect.y >= 125:
            self.rect.y=125
        if self.rect.y <= 0:
            self.rect.y=0
    
    def update(self):
        self.check()
        self.rect.y += self.speed
        
def render_score():
    global score_text
    score_font = pg.font.Font('./font/ARCADECLASSIC.TTF', 34)
    score_text = score_font.render(f'Score {SCORE//10}', False, 'Red')

submarine = Submarine(70, 50)
shark = Shark(SHARK_X, SHARK_Y)
star = Star(800, rnd.randint(1, 120))
sprites.add(submarine, shark, star)

while True:
    screen.fill('Black')
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                submarine.speed += (SPEED_INCREASE + 4.0)
            elif event.key == pg.K_UP:
                submarine.speed -= (SPEED_INCREASE + 4.0)
        elif event.type == pg.KEYUP:
            submarine.speed = 0
        
    if pg.sprite.collide_rect(submarine, shark):
        exit()
    
    if pg.sprite.collide_rect(submarine, star):
        SCORE += 100
        star.rect.x = 810
        star.rect.y = rnd.randint(1,120)
        SPEED_INCREASE += 0.2
    
    render_score()
    
    sprites.update()
    
    screen.blit(background, (0, 0))
    screen.blit(submarine.image, submarine.rect)
    screen.blit(shark.image, shark.rect)
    screen.blit(star.image, star.rect)
    screen.blit(score_text, (0,0,))
    
    SCORE += 1
    
    pg.display.update()
    clock.tick(FPS)