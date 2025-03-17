import threading
import traceback
from  pygame import display
import pygame.display
from pygame.locals import *
from base import *
import local.color as col
import numba
import localFunction
from local.color import *


class Scene:
    def __init__(self,surface,texture,name='.',child=None):
        self.surface=surface
        self.texture=texture
        self.name=name
        self.children=[] if child is None else child
    def update(self,*args,**kwargs):
        for i in self.children:
            i.update(*args,**kwargs)
    def __getattr__(self, item):
        return self.children[item]

class WelcomeWindow(Scene):
    def __init__(self,surface,texture):
        button1=localFunction.ButtonPy(surface,texture,500,500,'Welcome',500,70,fontsize=50)
        super().__init__(surface,texture,'.welcome',[button1])

class MainGame:
    def __init__(self,*args,**kwargs):
        try:
            self.__args=args
            self.__kwargs=kwargs
            self.__screenInfo=pygame.display.list_modes()[0]
            if config['program']['debug']:
                printf("-"*10,"DEBUG VERSION","-"*10,color=(col.BLUE,))
                printf('CHECKING VERSION',color=(col.LIGHT_RED,))
                printf('pygameVer:', pygame.__version__,color=(col.UNDERLINE,))
                printf('numbaVer:', numba.__version__,color=(col.UNDERLINE,))
                if pygame.__version__!="2.6.1" or numba.__version__!="0.61.0":
                    self.gameError(lang.text.versionError)
                printf('Locale:', local)
                print()
                printf(f"ARGS INFO:\n__args: {self.__args}\n__kwargs: {self.__kwargs}",type='debug')
                debug(f"Screen Info: {self.__screenInfo}")

            self.surface=pygame.display.set_mode((config['window']['weight'],config['window']['height']))
            self.clock=pygame.time.Clock()
            self.tick=pygame.time.Clock()

            #const value
            self.real_size=(config['window']['weight'],config['window']['height'])
            self.assetsImg = None
            self.fullscreen=False
            self.welcomewindow=None
            self.welcomewindowActive=True
            # Game Init
            self.gameInit()

            self.running=True # running flag
            threading.Thread(target=self.gameTick).start()
            while self.running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.gameQuit()
                    elif event.type == KEYDOWN:
                        debug(f'KEY DOWN:{event.key}')
                        if event.key in keyPos.fullscreen:
                            # 切换全屏模式
                            debug('FULLSCREEN!'+str(self.fullscreen))
                            self.surface=pygame.display.set_mode(self.real_size if self.fullscreen else self.__screenInfo, pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE)
                            self.fullscreen^=1
                            pygame.display.toggle_fullscreen()
                        elif event.key==K_ESCAPE:
                            self.gameQuit()

                self.surface.fill('white')
                self.gameUpdate()
                pygame.display.update()
                self.clock.tick(config['local']['FPS'])

            pygame.quit()

            if config['program']['debug']:
                printf("-"*10,"EXIT","-"*10,color=(LIGHT_BLUE,))
        except:
            self.gameError(traceback.format_exc())

    def gameTick(self):
        while self.running:
            self.tick.tick(config['local']['TPS'])

    def gameUpdate(self):
        if self.welcomewindowActive:
            self.welcomewindow.update()

    def gameQuit(self):
        # todo GameQuit
        debug(col.changeColor('GAME QUIT FUNCTION',(col.GREEN,)))
        self.running=False

    def gameInit(self):
        # todo GameInit
        debug(col.changeColor('GAME INIT FUNCTION',(col.GREEN,)))
        loadFonts()
        pygame.display.set_mode(self.real_size,pygame.RESIZABLE)
        self.assetsImg=loadImg(assetsLink.texture)
        self.welcomewindow=WelcomeWindow(self.surface,self.assetsImg)
        debug('assetsInfo:'+str(self.assetsImg))

    def gameError(self, defence):
        printf(defence,shown=col.RED,color=(col.LIGHT_RED,col.BOLD_UNDERLINE),type='error')
        showErr(lang.text.errorMessage, defence)
        debug('Runtime Error! ',color=(col.LIGHT_RED,))
        os.kill(os.getpid(), -1)

if __name__=="__main__":
    MainGame()
    print('welcome_demo')