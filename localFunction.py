import pygame
from base import *

class Widget:# todo Widget
    pass

class ButtonPy:
    def __init__(self,surface,texture,x,y,text,length,weight=-1,fg='black',bg='gray',hovcolor='blue',activecolor='gray',fontsize=30):
        self.scale = 1
        self.surface:pygame.Surface=surface
        self.center=pygame.Vector2(self.surface.get_size())/2
        self.texture=texture
        self.pos=pygame.Vector2(x,y)
        self.text=text
        self.size=pygame.Vector2(length,weight)
        self.fg=fg
        self.bg=bg
        self.hovcolor=hovcolor
        self.activecolor=activecolor

        self.__left=texture.btn.left
        self.__middle:pygame.Surface=texture.btn.middle
        self.__middle=pygame.transform.scale(self.__middle,(self.size.x,self.__middle.get_size()[1]))
        self.__right=texture.btn.right
        if weight==-1:
            self.size.y=self.__middle.get_size()[1]
        else:
            self.__left=pygame.transform.scale(self.__left,(self.__left.get_size()[0],weight))
            self.__middle=pygame.transform.scale(self.__middle,(self.__middle.get_size()[0],weight))
            self.__right=pygame.transform.scale(self.__right,(self.__right.get_size()[0],weight))
        self.font:pygame.font.Font=fonts['arial_'+str(fontsize)]

    def setscale(self,scale,center):
        self.scale=scale
        self.center=pygame.Vector2(center)

    def tick(self):
        pass

    def update(self):

        a=self.font.render(self.text,1,self.fg)
        rect=a.get_size()

        pygame.draw.rect(self.surface, self.bg, ((self.pos.x - self.size.x / 2, self.pos.y),(self.size.x,self.__middle.get_size()[1])))
        self.surface.blit(a,(self.pos.x-rect[0]/2+self.__left.get_size()[0]/2,self.pos.y-rect[1]/2+self.__middle.get_size()[1]/2))
        self.surface.blit(self.__middle,(self.pos.x-self.size.x/2,self.pos.y))
        self.surface.blit(self.__left,(self.pos.x-self.size.x/2,self.pos.y))
        self.surface.blit(self.__right,(self.pos.x+self.size.x/2-self.__right.get_size()[0],self.pos.y))
