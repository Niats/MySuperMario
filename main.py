#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Імпортуємо бібліотеку
import pygame
from pygame import *
from player import *
from blocks import *

#Оголошуємо змінні
WIN_WIDTH = 800 #Ширина вікна
WIN_HEIGHT = 640 #Висота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Групуємо ширну і висоту в одну змінну
BACKGROUND_COLOR = "#66ccff"

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
        
def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не рухається дальше лівої границі
    l = max(-(camera.width-WIN_WIDTH), l)   # Не рухається дальше правої границі
    t = max(-(camera.height-WIN_HEIGHT), t) # Не рухається дальше нижньої границі
    t = min(0, t)                           # Не рухається дальше верхньої границі

    return Rect(l, t, w, h)        


def main():
    pygame.init() # Ініціалізуємо PyGame
    screen = pygame.display.set_mode(DISPLAY) # Ствоюємо вікно
    pygame.display.set_caption("Super Mario") # Пишем в шапку
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Створення видимої поверхні, фон                       
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаємо поверхню суцільним кольором
    
    hero = Player(65,65) # створюємо героя по (x,y) координатам
    left = right = False # по замовчуванню - стояти
    up = False
    
    entities = pygame.sprite.Group() # Всі обєкти
    platforms = [] # те, в що ми будемо врізаться чи опиратися
    
    entities.add(hero)
           
    level = [
       "---------------------------------------------",
       "-                                           -",
       "-                                           -",
       "-                   ---                     -",
       "-                                           -",
       "---                                         -",
       "-                                           -",
       "-               ---         ---             -",
       "-                                           -",
       "----                                        -",
       "-                                           -",
       "-                           ----            -",
       "-                                           -",
       "-                                         ---",
       "-      ---                                  -",
       "-                                           -",
       "-                   ----                    -",
       "-                                           -",
       "-                                           -",
       "---------------------------------------------"]
       
    timer = pygame.time.Clock()
    x=y=0 # координати
    for row in level: # вся строка
        for col in row: # кожний символ
            if col == "-":
                pf = Platform(x,y)
                entities.add(pf)
                platforms.append(pf)

            x += PLATFORM_WIDTH #блоки платформи ставлятся на ширині блоків
        y += PLATFORM_HEIGHT    #то саме з висотою
        x = 0                   #на кожній новій строці начинаємо з нуля
    
    total_level_width  = len(level[0])*PLATFORM_WIDTH # Вираховуємо фактичну ширину рівня
    total_level_height = len(level)*PLATFORM_HEIGHT   # Висоту
    
    camera = Camera(camera_configure, total_level_width, total_level_height) 
    
    while 1: # Основний цикл програми
        timer.tick(60)
        for e in pygame.event.get(): # Обробляємо події
            if e.type == QUIT:
                raise SystemExit, "QUIT"
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True


            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        screen.blit(bg, (0,0))      # Кажну ітерацію потрібно все перемальовути


        camera.update(hero) # централізуємо камеру віповідно до героя
        hero.update(left, right, up,platforms) # рух
        #entities.draw(screen) # відображення
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        
        
        pygame.display.update()     # обновлення і вивід всіх змін на екран
        

if __name__ == "__main__":
    main()
