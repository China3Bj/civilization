from base import *
import pygame
import random
import sys

class FirstBlock:
    def __init__(self,surface):
        self.surface=surface
        self.pos=pygame.Vector2(0,0)
        self.step=pygame.Vector2(random.uniform(1.,8.),random.uniform(1.,8.))
        self.size=pygame.Vector2(50,50)
    def update(self):
        pygame.draw.rect(self.surface,'white', [self.pos,self.size])

        if not 0 < self.pos[0]:
            self.step[0] = max(-self.step[0], self.step[0])
        if not self.pos[0]+self.size[0] < config['window']['weight']:
            self.step[0] = min(-self.step[0], self.step[0])
        if not 0<self.pos[1]:
            self.step[1]=max(-self.step[1],self.step[1])
        if not self.pos[1]+self.size[1]<config['window']['height']:
            self.step[1]=min(-self.step[1],self.step[1])

        self.pos+=self.step

class MainGame:
    def __init__(self,*args,**kwargs):
        self.__args=args
        self.__kwargs=kwargs
        self.surface=pygame.display.set_mode((config['window']['weight'],config['window']['height']))
        self.clock=pygame.time.Clock()

        block=[FirstBlock(self.surface) for _ in range(20)]

        while True:
            self.surface.fill('black')
            for _ in block:
                _.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            pygame.display.update()
            self.clock.tick(config['local']['FPS'])

if __name__=="__main__":
    MainGame()