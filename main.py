from base import *
import pygame
import random
import sys

class MainGame:
    def __init__(self,*args,**kwargs):
        self.__args=args
        self.__kwargs=kwargs
        self.surface=pygame.display.set_mode((config['window']['weight'],config['window']['height']))
        self.clock=pygame.time.Clock()

        self.welcomeActive=True
        a=PyButton(self.surface,100,100,100)

        while True:
            self.surface.fill('black')

            if self.welcomeActive:
                a.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            pygame.display.update()
            self.clock.tick(config['local']['FPS'])

if __name__=="__main__":
    MainGame()