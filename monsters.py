#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pyganim
import os

MONSTER_WIDTH = 100
MONSTER_HEIGHT = 100
MONSTER_COLOR = "#1a1a00"
ICON_DIR = os.path.dirname(__file__)


ANIMATION_MONSTERHORYSONTAL = [('%s/monsters/fire1.png' % ICON_DIR),
                      ('%s/monsters/fire2.png' % ICON_DIR )]

class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft,maxLengthUp):
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.startX = x # початкові координати
        self.startY = y
        self.maxLengthLeft = maxLengthLeft # максимальний лях в одн сторону
        self.maxLengthUp= maxLengthUp # по вертикалі
        self.xvel = left # рух по горизонталі, 0 - стоїть
        self.yvel = up # скорость движения по вертикали, 0 - не рухається
        boltAnim = []
        for anim in ANIMATION_MONSTERHORYSONTAL:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()
         
    def update(self, platforms): # по принципу героя
                    
        self.image.fill(Color(MONSTER_COLOR))
        self.boltAnim.blit(self.image, (0, 0))
       
        self.rect.y += self.yvel
        self.rect.x += self.xvel
 
        self.collide(platforms)
        
        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel =-self.xvel  # якщо пролетів до кінця то рухативсь назад
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel 

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p: # якщо з кимось стовнувся
               self.xvel = - self.xvel # то рухаємося назад
               self.yvel = - self.yvel
