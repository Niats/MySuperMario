#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pyganim
import os
import blocks
import monsters

MOVE_SPEED = 7
MOVE_EXTRA_SPEED = 2.5 # пришвидшення
WIDTH = 22
HEIGHT = 32
COLOR =  "#888888"
JUMP_POWER = 10
JUMP_EXTRA_POWER = 1  # дадаткова сила прижку
GRAVITY = 0.35 # Сила, яка буде героя тягнути в низ
ANIMATION_DELAY = 0.1 # швидкість зміни кадрів
ANIMATION_SUPER_SPEED_DELAY = 0.05 # швидкість зміни кадрів при пришвидшенні прижка
ICON_DIR = os.path.dirname(__file__) #  повний шлях до каталогу з файлами

ANIMATION_RIGHT = [('%s/mario/r1.png' % ICON_DIR),
            ('%s/mario/r2.png' % ICON_DIR),
            ('%s/mario/r3.png' % ICON_DIR),
            ('%s/mario/r4.png' % ICON_DIR),
            ('%s/mario/r5.png' % ICON_DIR)]
ANIMATION_LEFT = [('%s/mario/l1.png' % ICON_DIR),
            ('%s/mario/l2.png' % ICON_DIR),
            ('%s/mario/l3.png' % ICON_DIR),
            ('%s/mario/l4.png' % ICON_DIR),
            ('%s/mario/l5.png' % ICON_DIR)]
ANIMATION_JUMP_LEFT = [('%s/mario/jl.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/mario/jr.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/mario/j.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/mario/0.png' % ICON_DIR, 0.1)]

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   #швидкість переміщення. 0 - стоїть на місці
        self.startX = x # початкова позиція Х,якщо рівень буде переграватися
        self.startY = y
        self.yvel = 0 #швидкість вертикального переміщення
        self.onGround = False 
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямокутний обєкт
        self.image.set_colorkey(Color(COLOR)) # прозорий фон
#        Анімація руху в право
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRightSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimRightSuperSpeed.play()
#        Анімація руху в ліво     
        boltAnim = []
        boltAnimSuperSpeed = [] 
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.boltAnimLeftSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimLeftSuperSpeed.play()
        
        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0)) # по замовчуванню стояти
        
        self.boltAnimJumpLeft= pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()
        
        self.boltAnimJumpRight= pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()
        
        self.boltAnimJump= pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()
        self.winner = False
        

    def update(self, left, right, up, running, platforms):
        
        if up:
            if self.onGround: # пригати якщо можемо відштовхнутися від землі
                self.yvel = -JUMP_POWER
                if running and (left or right): # якщо є пришвидшення і ми рухаємося
                       self.yvel -= JUMP_EXTRA_POWER # то пригаємо вище
                self.image.fill(Color(COLOR))
                self.boltAnimJump.blit(self.image, (0, 0))
                       
        if left:
            self.xvel = -MOVE_SPEED # ліво = x- n
            self.image.fill(Color(COLOR))
            if running: # якщо пришвидшення
                self.xvel-=MOVE_EXTRA_SPEED # то передвигаемся быстрее
                if not up: # і якщо не пригаємо
                    self.boltAnimLeftSuperSpeed.blit(self.image, (0, 0)) #тоді відтворюємо швидку анімацію
            else: # якщо не біжимо
                if not up: # і не пригаємо
                    self.boltAnimLeft.blit(self.image, (0, 0)) # тоді відображаємо анімацію руху
            if up: # якщо пригаємо
                    self.boltAnimJumpLeft.blit(self.image, (0, 0)) # відтворюємо анімацію прижку
 
        if right:
            self.xvel = MOVE_SPEED # Вправо = x + n
            self.image.fill(Color(COLOR))
            if running:
                self.xvel+=MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimRightSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.boltAnimRight.blit(self.image, (0, 0)) 
            if up:
                    self.boltAnimJumpRight.blit(self.image, (0, 0))
 
         
        if not(left or right): # стоїмо коли не має вказівок іти
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))
            
        if not self.onGround:
            self.yvel +=  GRAVITY
            
        self.onGround = False;    
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel # переносимо своє положення на xvel
        self.collide(self.xvel, 0, platforms)
   
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p): # якщо є пересікання платформи з іграком
                if isinstance(p, blocks.BlockDie) or isinstance(p, monsters.Monster): # якщо перескакуємо - blocks.BlockDie чи Monster
                       self.die()# вмираємо
                elif isinstance(p, blocks.BlockTeleport):
                       self.teleporting(p.goX, p.goY)
                elif isinstance(p, blocks.Princess): # якщо торнулися принцеси
                       self.winner = True #перемогли!
                else:
                    if xvel > 0:                      # якщо рухається вправо
                        self.rect.right = p.rect.left # то не рухається вліво

                    if xvel < 0:                      
                        self.rect.left = p.rect.right 

                    if yvel > 0:                      # якщо подає вниз
                        self.rect.bottom = p.rect.top # то не падає в гору
                        self.onGround = True          # якщо стає на опору
                        self.yvel = 0                 # то енергія падіння пропадає

                    if yvel < 0:                      # якщо рухається вверх
                        self.rect.top = p.rect.bottom # то не рухається вниз
                        self.yvel = 0                 # тоді енергія прижка пропадає

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY
        
    def die(self):
        time.wait(500)
        self.teleporting(self.startX, self.startY) # переміщення на початкові координати