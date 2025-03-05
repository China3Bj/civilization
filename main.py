from base import *
import pygame
import random
import sys

class MainGame:
    def __init__(self,*args,**kwargs):
        self.__args=args
        self.__kwargs=kwargs
        self.mousePos = pygame.Vector2(0,0)
        self.mouseDown=0
        self.surface=pygame.display.set_mode((config['window']['weight'],config['window']['height']))
        self.clock=pygame.time.Clock()


        while True:
            self.surface.fill('black')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseUpdate(pygame.Vector2(*event.pos))
                    self.mouseDown=1
                if self.mouseDown and event.type==pygame.MOUSEMOTION:
                    self.mouseUpdate(pygame.Vector2(*event.pos))
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouseUpdate(pygame.Vector2(0,0))
                    self.mouseDown=0

            pygame.display.update()
            self.clock.tick(config['local']['FPS'])

    def mouseUpdate(self,pos):
        self.mousePos=pos


if __name__=="__main__":
    MainGame()