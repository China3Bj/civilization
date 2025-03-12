import traceback
import locale
import numba
import os
import sys
import pygame
import tomllib
from tkinter import *
from tkinter.messagebox import *
import json

pygame.init()
erronBuffer= (b'\x00\x00\x00\x00\x00\x00\xff\x00\xff\xff\x00\xff\x00\x00\x00\x00\x00\x00\xff\x00\xff\xff\x00\xff\xff'
              b'\x00\xff\xff\x00\xff\x00\x00\x00\x00\x00\x00\xff\x00\xff\xff\x00\xff\x00\x00\x00\x00\x00\x00')

class AssetsDict(dict):
    def __init__(self,*args,**kwargs):
        self.from_=''
        if 'from_' in kwargs:
            self.from_=kwargs['from_']
        super().__init__(*args,**kwargs)
    def __getattr__(self, item):
        __g=self[item]
        if type(__g)==dict:
            __g=AssetsDict(__g,from_=self.from_+'.'+item)
        return __g
    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except:
            _a=self.from_+'.'+item
            return _a

class ConfigDict(dict):
    def __getattr__(self, item):
        __g=self[item]
        if type(__g)==dict:
            __g=ConfigDict(__g)
        return __g


def showErr(title,err):
    win=Tk()
    win.withdraw()
    showerror(title,err)

def setupLang(loc):
    loc=loc[0]
    di=list(os.walk('assets/lang'))[0][2]
    lan='en'
    for i in di:
        i=i.replace('.json','')
        if i==loc:
            lan=i
            break
        if  i[:2]==loc:
            lan=i[:2]
            break
    return lan

with open('config.toml', 'rb') as f:
    try:
        config=ConfigDict(tomllib.load(f))
        __ass=config['local']['assetsLink']


        local=locale.getdefaultlocale(locale.LC_ALL)#zh-CN
        lang=config['local']['lang']
        if lang=='auto':
            lang=setupLang(local)


        debug=config['program']['debug']
        with open(__ass, 'rb') as f2:
            assetsLink=AssetsDict(json.load(f2))
        try:
            with open(f'assets/lang/{lang}.json', 'rb') as f2:
                lang = AssetsDict(json.load(f2))
        except FileNotFoundError:
            traceback.print_exc()
            print("Var \"lang\" is not found!", file=sys.stderr)
            showErr('Runtime Error!', "Var \"lang\" is not found!")
            os.kill(os.getpid(), -1)
    except Exception:
        traceback.print_exc()
        print('Reading "config.toml" error!', file=sys.stderr)
        showErr('Runtime Error!', 'Reading "config.toml" error!')
        os.kill(os.getpid(), -1)

import ctypes

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

if debug:
    print('-'*15,"DEBUG",'-'*15)
    print('info: pygameVer:', pygame.__version__)
    print('info: numbaVer:',numba.__version__)
    print('info: Locale:',local)



    set_console_color(FOREGROUND_RED | FOREGROUND_INTENSITY)  # 设置为红色高亮文本
    print("这是一个红色的文本")
    set_console_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)  # 更改颜色为绿色高亮文本
    print("这是一个绿色的文本")

class PyButton:
    def __init__(self,surface:pygame.Surface,x,y,length):
        self.surface=surface
        self.x=x
        self.y=y
        self.length=length
        self.__leftImg=assetsLink.texture.btn.left
        self.__middleImg=assetsLink.texture.btn.middle
        self.__rightImg=assetsLink.texture.btn.right

    def update(self):
        self.surface.blit(self.__leftImg,(self.x,self.y))

if __name__=="__main__":
    pass