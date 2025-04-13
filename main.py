import threading
from pygame import *
from pygame import display
import pygame.display
from pygame.locals import *
from base import *
import local.color as col
import numba
import localFunction
from local.color import *
import ctypes
import argparse


class MainGame:
    def __init__(self, *args, **kwargs):
        """
        这个类是运行主类，执行主程序循环
        :param args:
        :param kwargs:
        """
        try:
            self.__args = args
            self.__kwargs = kwargs
            self.__screenInfo = pygame.display.list_modes()[0]

            # 设置进程为 DPI 感知模式（支持多显示器不同缩放比例）
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # 2 = 每显示器 DPI 感知

            def get_scaling_factor():
                # 获取当前显示器的 DPI 值
                hdc = ctypes.windll.user32.GetDC(0)
                dpi_x = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # 88 = LOGPIXELSX
                ctypes.windll.user32.ReleaseDC(0, hdc)

                # 计算缩放倍率（默认 96 DPI 为 100% 缩放）
                return round(dpi_x / 96, 2)

            self.dpiScl = get_scaling_factor()

            if debug_:
                printf("-" * 10, "DEBUG VERSION", "-" * 10, color=(col.BLUE,))
                printf('CHECKING VERSION', color=(col.LIGHT_RED,))
                printf('pygameVer:', pygame.__version__, color=(col.UNDERLINE,))
                printf('numbaVer:', numba.__version__, color=(col.UNDERLINE,))
                if pygame.__version__ != "2.6.1" or numba.__version__ != "0.61.0":
                    self.gameError(lang.text.versionError)
                printf('Locale:', local)
                print()
                printf(f"ARGS INFO:\n__args: {self.__args}\n__kwargs: {self.__kwargs}", type='debug')
                debug(f"Screen Info: {self.__screenInfo}")
                debug(f"DPI SCALE: {get_scaling_factor()}")  # 示例输出：1.25（125% 缩放）

            self.surface = pygame.display.set_mode((config['window']['weight'], config['window']['height']))
            self.clock = pygame.time.Clock()
            self.tick = pygame.time.Clock()

            #const value
            self.real_size = (config['window']['weight'] * self.dpiScl, config['window']['height'] * self.dpiScl)
            self.assetsImg = None
            self.fullscreen = False
            self.welcomewindow = None
            self.welcomewindowActive = True
            self.mousePos = Vector2(0, 0)
            self.mouseDown = False
            self.mouseKey = 0
            # Game Init
            self.gameInit()

            self.running = True  # running flag
            threading.Thread(target=self.gameTick).start()
            """
            主程序循环
            """
            while self.running:
                for event in pygame.event.get():
                    """
                    事件循环，用if不断遍历运行。
                    这里的`event.type`是`pygame.constants`中的值
                    """

                    if event.type == QUIT:
                        self.gameQuit()
                    elif event.type == KEYDOWN:
                        debug(f'KEY DOWN:{event.key}')
                        if event.key in keyPos.fullscreen:
                            # 切换全屏模式
                            debug('FULLSCREEN!' + str(self.fullscreen))
                            self.surface = pygame.display.set_mode(
                                self.real_size if self.fullscreen else self.__screenInfo,
                                pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE)
                            self.fullscreen ^= 1
                            pygame.display.toggle_fullscreen()
                        elif event.key == K_ESCAPE:
                            self.gameQuit()
                    elif event.type == MOUSEMOTION:
                        self.mousePos = Vector2(event.pos)
                    elif event.type == MOUSEBUTTONDOWN:
                        self.mouseDown = True
                        self.mouseKey = event.button
                    elif event.type == MOUSEBUTTONUP:
                        self.mouseDown = False
                        self.mouseKey = 0

                self.surface.fill('white')
                self.gameUpdate()
                pygame.display.update()
                self.clock.tick(config['local']['FPS'])

            """
            退出程序
            """
            pygame.quit()

            if debug_:
                printf("-" * 10, "EXIT", "-" * 10, color=(LIGHT_BLUE,))
        except:
            """
            运行时错误
            """
            self.gameError(traceback.format_exc())

    def gameTick(self):
        """
        游戏的“刻”(tick)运行。
         - 默认是20刻每秒。计量刻速度的单位是TPS(ticks per second)。
         - 正常游戏运行时AI处理信息的速度。
         - 也可以时游戏运行时组件(Widget)的反应速度。
        :return: None
        """
        while self.running:
            if self.welcomewindowActive:
                if self.mouseDown:
                    self.welcomewindow.tick(MOUSEBUTTONDOWN, self.mousePos, self.mouseKey)
                    self.welcomewindow.tick(MOUSEBUTTONUP, self.mousePos, self.mouseKey)
                else:
                    self.welcomewindow.tick(MOUSE_MOTION, self.mousePos)
            self.tick.tick(config['local']['TPS'])

    def gameUpdate(self):
        """
        游戏的帧数刷新
         - 与刻运行独立。
         - 不同电脑的帧数不同，方法的运行速度不同
        :return: None
        """
        if self.welcomewindowActive:
            self.welcomewindow.update()

    def gameQuit(self):
        """
        退出方法。可以用来保存文件会、或者输出log
        :return: `None`
        """
        # todo GameQuit
        debug(col.changeColor('GAME QUIT FUNCTION', (col.GREEN,)))
        self.running = False

    def gameInit(self):
        """
        游戏初始化方法
        :return: `None`
        """
        # todo GameInit
        debug(col.changeColor('GAME INIT FUNCTION', (col.GREEN,)))
        loadFonts()
        pygame.display.set_mode(self.real_size, pygame.RESIZABLE)
        self.assetsImg = loadImg(assetsLink.texture)
        self.welcomewindow = WelcomeWindow(self, self.assetsImg)
        debug('assetsInfo:' + str(self.assetsImg))

    def gameError(self, defence):
        """
        游戏错误退出方法
        :param defence: 错误信息
        :return: `None`
        """
        printf(defence, shown=col.RED, color=(col.LIGHT_RED, col.BOLD_UNDERLINE), type='error')
        showErr(lang.text.errorMessage, defence)
        debug('Runtime Error! ', color=(col.LIGHT_RED,))
        os.kill(os.getpid(), -1)


class WelcomeWindow(localFunction.Scene):
    def __init__(self, master, texture):
        """
        欢迎窗口
        :param master: 父窗口
        :param texture: 材质, * 虽然我不知道怎么用~ *
        """
        self.dpiscale = master.dpiScl
        button1 = localFunction.ButtonPy(master, texture, 250 * self.dpiscale, 250 * self.dpiscale, 'Hello World',
                                         250 * self.dpiscale, 45 * self.dpiscale, fontsize=30 * self.dpiscale,command=lambda :print('Hello World'))
        super().__init__(master, texture, '.welcome', [button1])

def main():
    """
    Main Function of all the Modules
    :return: `None`
    """
    global debug_
    p = argparse.ArgumentParser(description="MainGame")
    p.add_argument('--debug', action='store_true', help="调试模式")
    p.add_argument('-c', '--code', help=col.changeColor(
        "???\\84\\? ?\\104\\?\\101\\\u0084\\32\\\\67\\ ??\u0084**(\x78@ \\111\\ ?\\100\\  \033\033 \\101\\?\\102\\????\\32\\???"
        "\\67\\? "
        "?\077\\104\\\\101\\??\30 ?\077 \\97\\\\116\\  \145???s\\105\\\\110\\\\103\\dd ??\\33\\??  \\33\\??? "
        "?? \\33\\",
        (col.RED, col.BOLD, col.UNDERLINE)))
    args_ = p.parse_args()
    debug_ = args_.debug
    MainGame()

if __name__ == "__main__":
    main()
