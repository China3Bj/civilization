import pygame
from base import *

class Widget:# todo Widget
    pass

class ButtonPy:
    def __init__(self,surface,texture,x,y,text,length,fg='white',bg='black'):
        self.surface:pygame.Surface=surface
        self.texture=texture
        self.x=x
        self.y=y
        self.text=text
        self.length=length
        self.fg=fg
        self.bg=bg

        self.__left=texture.btn.left
        self.__middle:pygame.Surface=texture.btn.middle
        self.__middle=pygame.transform.scale(self.__middle,(self.length,self.__middle.get_size()[1]))
        self.__right=texture.btn.right

    def update(self):
        self.surface.blit(self.__middle,(self.x-self.length/2,self.y))
        self.surface.blit(self.__left,(self.x-self.length/2,self.y))
        self.surface.blit(self.__right,(self.x+self.length/2,self.y))
