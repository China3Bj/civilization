from  pygame import display
import pygame.display
from pygame.locals import *
import time
from base import *
import local.color as col


class Scene:
    def __init__(self,name='.',child=None):
        self.name=name
        self.children=[] if child is None else child
    def update(self,*args,**kwargs):
        for i in self.children:
            i.update(*args,**kwargs)
    def __getattr__(self, item):
        return self.children[item]

def printf(*args,**kwargs):
    try:
        typ=kwargs['type']
        del kwargs['type']
    except KeyError:
        typ="info"
    try:
        co=kwargs['color']
        del kwargs['color']
    except KeyError:
        co=(col.RESET,)
    try:
        sep=kwargs['sep']
        del kwargs['sep']
    except KeyError:
        sep=' '
    try:
        shown=kwargs['shown']
        del kwargs['shown']
    except KeyError:
        shown=col.BLUE
    g=time.strftime("%Y.%d.%m %X",time.localtime(time.time()))
    text=sep.join(map(str,args))
    text=col.changeColor(text,co)
    print(f'\033[95m[\033[96m{g}\033[95m] \033[{shown}m({typ})\033[0m',text,**kwargs)

def debug(*args,**kwargs):
    if config['program']['debug']:printf(*args,**kwargs,type='debug')


class MainGame:
    def __init__(self,*args,**kwargs):
        self.__args=args
        self.__kwargs=kwargs
        self.__screenInfo=pygame.display.list_modes()[0]
        if config['program']['debug']:
            printf("-"*10,"DEBUG VERSION","-"*10)
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
        # Game Init
        self.gameInit()

        self.running=True # running flag
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.gameQuit()
                elif event.type == KEYDOWN:
                    if event.key == K_F11:
                        # 切换全屏模式
                        debug('FULLSCREEN!')
                        pygame.display.toggle_fullscreen()
                    elif event.key==K_ESCAPE:
                        self.gameQuit()

            self.surface.fill('white')
            pygame.display.update()
            self.clock.tick(config['local']['FPS'])

        pygame.quit()

        if config['program']['debug']:
            printf("-"*10,"EXIT","-"*10)

    def gameQuit(self):
        # todo GameQuit
        debug('GAME QUIT FUNCTION')
        self.running=False

    def gameInit(self):
        # todo GameInit
        debug('GAME INIT FUNCTION')
        pygame.display.set_mode((config['window']['weight'],config['window']['height']),pygame.RESIZABLE)

    def gameError(self, defence):
        printf(defence,shown=col.RED,color=(col.LIGHT_RED,col.BOLD_UNDERLINE),type='error')
        showErr(lang.text.errorMessage, defence)
        debug('Runtime Error! ')
        os.kill(os.getpid(), -1)

if __name__=="__main__":
    MainGame()