#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Імпортуємо бібліотеку
import pygame
from pygame import *
from player import *
from blocks import *
from monsters import *

#Оголошуємо змінні
WIN_WIDTH = 800 #Ширина вікна
WIN_HEIGHT = 500 # Висота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Групуємо ширну і висоту в одну змінну
BACKGROUND_COLOR = "#000000"

FILE_DIR = os.path.dirname(__file__)

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
    t = min(0, t)                            # Не рухається дальше верхньої границі

    return Rect(l, t, w, h) 


def loadLevel():
    global playerX, playerY #обявляємо глобальні премінні, це координати героя

    levelFile = open('%s/levels/1.txt' % FILE_DIR)
    line = " "
    commands = []
    while line[0] != "/": # завершення файлу
        line = levelFile.readline() # прядково
        if line[0] == "[": # початок рівня
            while line[0] != "]": # кінець рівня
                line = levelFile.readline()
                if line[0] != "]": #якщо не має
                    endLine = line.find("|") # то шукаємо символ кінця рядка
                    level.append(line[0: endLine]) # добавляємо рівень в рядок відпочатку до символу "|"
                    
        if line[0] != "": # якщо рядок не пустий
         commands = line.split() # розбиваємо його на окремі команди
         if len(commands) > 1: #якщо к-ть команд > 1, то шукаємо їх
            if commands[0] == "player": # якщо перша - player
                playerX= int(commands[1]) # то записуємо координати героя
                playerY = int(commands[2])
            if commands[0] == "portal": # якщо перша команда portal, то створюємо
                tp = BlockTeleport(int(commands[1]),int(commands[2]),int(commands[3]),int(commands[4]))
                entities.add(tp)
                platforms.append(tp)
                animatedEntities.add(tp)
            if commands[0] == "monster": # якщо команда monster, то створюємо монстра
                mn = Monster(int(commands[1]),int(commands[2]),int(commands[3]),int(commands[4]),int(commands[5]),int(commands[6]))
                entities.add(mn)
                platforms.append(mn)
                monsters.add(mn)

def main():
    loadLevel()
    pygame.init() # Ініціалізуємо PyGame
    screen = pygame.display.set_mode(DISPLAY) # Ствоюємо вікно
    pygame.display.set_caption("Super Mario Boy") # Пишем в шапку
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Створення видимої поверхні, фон
                                        
    bg.fill(Color(BACKGROUND_COLOR))   # Заливаємо поверхню суцільним кольором 
        
    left = right = False # по замовчуванню - стояти
    up = False
    running = False
     
    hero = Player(playerX,playerY) # створюємо героя по (x,y) координатам
    entities.add(hero)
           
    timer = pygame.time.Clock()
    x=y=0 # координати
    for row in level: # весь рядок
        for col in row: # кожний символ
            if col == "-":
                pf = Platform(x,y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x,y)
                entities.add(bd)
                platforms.append(bd)
            if col == "P":
                pr = Princess(x,y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)
   
            x += PLATFORM_WIDTH #блоки платформи ставлятся на ширині блоків
        y += PLATFORM_HEIGHT    #то саме з висотою
        x = 0                   #на кожній новій строці начинаємо з нуля
    
    total_level_width  = len(level[0])*PLATFORM_WIDTH # Вираховуємо фактичну ширину рівня уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # Висоту
    
    camera = Camera(camera_configure, total_level_width, total_level_height) 
    
    while not hero.winner: # Основний цикл програми
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
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False

        screen.blit(bg, (0,0))      # Кожну ітерацію потрібно все перемальовути 

        animatedEntities.update() 
        monsters.update(platforms) 
        camera.update(hero)  # централізуємо камеру віповідно до героя
        hero.update(left, right, up, running, platforms) 
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()       # обновлення і вивід всіх змін на екран
        
level = []
entities = pygame.sprite.Group() # всі обєкти
animatedEntities = pygame.sprite.Group() 
monsters = pygame.sprite.Group() 
platforms = [] 
if __name__ == "__main__":
    main()
