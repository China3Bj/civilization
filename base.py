import traceback
import locale
import os
import sys
import pygame
import tomllib
from tkinter import *
from tkinter.messagebox import *
import json
import time
import ctypes
import local.color as col
from local.local import *

pygame.init()
erronBuffer = (b'\x00\x00\x00\x00\x00\x00\xff\x00\xff\xff\x00\xff\x00\x00\x00\x00\x00\x00\xff\x00\xff\xff\x00\xff\xff'
               b'\x00\xff\xff\x00\xff\x00\x00\x00\x00\x00\x00\xff\x00\xff\xff\x00\xff\x00\x00\x00\x00\x00\x00')


class AssetsDict(dict):
    def __init__(self, *args, **kwargs):
        """
        Assets字典，一般存储材质
        :param args:
        :param kwargs:
        """
        self.from_ = ''
        if 'from_' in kwargs:
            self.from_ = kwargs['from_']
            del kwargs['from_']
        super().__init__(*args, **kwargs)

    def __getattr__(self, item):
        __g = self[item]
        if type(__g) == dict:
            __g = AssetsDict(__g, from_=self.from_ + '.' + item)
        return __g

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except:
            _a = self.from_ + '.' + item
            return _a


class ConfigDict(dict):
    def __init__(self, *args, **kwargs):
        """
        配置字典，存储配置
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def __getattr__(self, item):
        __g = self[item]
        if type(__g) == dict:
            __g = ConfigDict(__g)
        return __g


def loadImg(assets: AssetsDict | str):
    if type(assets) == str:
        try:
            return pygame.image.load(assets)
        except:
            return assets
    else:
        new = AssetsDict()
        for index, items in assets.items():
            new[index] = loadImg(items)
        return new


def showErr(title, err):
    win = Tk()
    win.withdraw()
    showerror(title, err)


def setupLang(loc):
    loc = loc[0]
    di = list(os.walk('assets/lang'))[0][2]
    lan = 'en'
    for i in di:
        i = i.replace('.json', '')
        if i == loc:
            lan = i
            break
        if i[:2] == loc:
            lan = i[:2]
            break
    return lan


with open('config.toml', 'rb') as f:
    try:
        config = ConfigDict(tomllib.load(f))
        __ass = config['local']['assetsLink']

        local = locale.getdefaultlocale()  #zh-CN
        lang = config['local']['lang']
        if lang == 'auto':
            lang = setupLang(local)

        with open(__ass, 'rb') as f2:
            assetsLink = AssetsDict(json.load(f2))
        try:
            with open(f'assets/lang/{lang}.json', 'rb') as f2:
                lang = AssetsDict(json.load(f2))
        except FileNotFoundError:
            traceback.print_exc()
            print("Var \"lang\" is not found!", file=sys.stderr)
            showErr('Runtime Error!', "Var \"lang\" is not found!")
            os.kill(os.getpid(), -1)

        try:
            with open(assetsLink.keyPos, 'rb') as f2:
                keyPos = AssetsDict(json.load(f2))
        except FileNotFoundError:
            traceback.print_exc()
            print("Var \"KeyPos\" is not found!", file=sys.stderr)
            showErr('Runtime Error!', "Var \"KeyPos\" is not found!")
            os.kill(os.getpid(), -1)

        fonts = {}

    except Exception:
        traceback.print_exc()
        print('Reading "config.toml" error!', file=sys.stderr)
        showErr('Runtime Error!', 'Reading "config.toml" error!')
        os.kill(os.getpid(), -1)


def loadFonts():
    for _1, _2 in assetsLink.fonts.items():
        for i in range(20, 302, 1):
            fonts[_1 + "_" + str(i)] = pygame.font.Font(_2, i)


# 设置控制台文本颜色
STD_OUTPUT_HANDLE = -11
FOREGROUND_RED = 0x0004  # 文本颜色：红色
FOREGROUND_GREEN = 0x0002  # 文本颜色：绿色
FOREGROUND_BLUE = 0x0001  # 文本颜色：蓝色
FOREGROUND_INTENSITY = 0x0008  # 文本颜色：高亮


class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]


class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [
        ("dwSize", COORD),
        ("dwCursorPosition", COORD),
        ("wAttributes", ctypes.c_ushort),
        ("srWindow", ctypes.c_long),
        ("dwMaximumWindowSize", COORD)
    ]


def set_console_color(color):
    h = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    ctypes.windll.kernel32.GetConsoleScreenBufferInfo(h, ctypes.byref(csbi))
    # 设置新的文本和背景属性
    ctypes.windll.kernel32.SetConsoleTextAttribute(h, color)


def printf(*args, **kwargs):
    try:
        typ = kwargs['type']
        del kwargs['type']
    except KeyError:
        typ = "info"
    try:
        co = kwargs['color']
        del kwargs['color']
    except KeyError:
        co = (col.RESET,)
    try:
        sep = kwargs['sep']
        del kwargs['sep']
    except KeyError:
        sep = ' '
    try:
        shown = kwargs['shown']
        del kwargs['shown']
    except KeyError:
        shown = col.BLUE
    g = time.strftime("%Y.%d.%m %X", time.localtime(time.time()))
    text = sep.join(map(str, args))
    text = col.changeColor(text, co)
    print(f'\033[95m[\033[96m{g}\033[95m] \033[{shown}m({typ})\033[0m', text, **kwargs)

debug_=False
def debug(*args, **kwargs):
    if debug_: printf(*args, **kwargs, type='debug')


if __name__ == "__main__":
    pass
