import pygame.color
from base import *


def mixin(col1: pygame.color.Color, col2: pygame.color.Color, perc,offset=5):
    """
    GRB色彩混合，如果色彩近似则忽略
    :param col1: 色彩1
    :param col2: 色彩2
    :param perc: 色彩混合百分比
    :param offset: 近似容忍阈值，默认为5
    :return: 混合后的色彩
    """
    mixin1 = (col1.r, col1.g, col1.b)
    mixin2 = (col2.r, col2.g, col2.b)
    if all(
            [
                abs(
                    mixin1[i]-mixin2[i]
                )<offset for i in range(3)
            ]
    ):
        return mixin1

    now = ([
        (mixin1[i] * perc + mixin2[i] * (1 - perc)) for i in range(3)
    ])
    return now


class Widget:  # todo Widget
    pass


class Scene:
    def __init__(self, master, texture=None, name='.', child=None):
        """
        场景类
        :param master: 父窗口
        :param texture: 材质
        :param name: 名称（默认为`"."`）
        :param child: 子窗口
        """
        self.master = master
        self.dpiscale = master.dpiScl
        self.surface = master.surface
        self.texture = texture
        self.name = name
        self.children = [] if child is None else child

    def update(self, *args, **kwargs):
        """刷新方法"""
        for i in self.children:
            i.update(*args, **kwargs)

    def tick(self, typ, *args):
        """刻方法"""
        for i in self.children:
            i.tick(typ, *args)

    def __getattr__(self, item):
        return self.children[item]


class ButtonPy:
    def __init__(self, master, texture, x, y, text, length, weight=-1, fg='black', bg='#dddddd', hovcolor='#2070a9',
                 activecolor='#606069', fontsize=30,command=None):
        """
        按钮类
        :param master: 父窗口
        :param texture: 按钮材质
        :param x: 坐标x
        :param y: 坐标y
        :param text: 文本
        :param length: 长度
        :param weight: 宽度
        :param fg: 前景色
        :param bg: 背景色
        :param hovcolor: 悬挂颜色
        :param activecolor: 执行颜色
        :param fontsize: 字体
        :param command: 执行命令
        """

        self.is_click = False
        self.__bgAlpha = 0
        self.rect: pygame.rect.Rect | pygame.rect.RectType | None = None
        self.scale = 1
        self.transition = 20  #tick
        self.surface: pygame.Surface = master.surface
        self.center = pygame.Vector2(self.surface.get_size()) / 2
        self.texture = texture
        self.pos = pygame.Vector2(x, y)
        self.text = text+"  "
        self.size = pygame.Vector2(length, weight)
        self.fg = fg
        self.bg = bg
        self.hovcolor = hovcolor
        self.activecolor = activecolor
        self.command=command

        self.__bgNow = self.bg
        self.active = 0
        self.hov = 0
        self.__hovTime = -1
        self.__hovHave = 0

        self.__left = texture.btn.left
        self.__middle: pygame.Surface = texture.btn.middle
        self.__middle = pygame.transform.scale(self.__middle, (self.size.x, self.__middle.get_size()[1]))
        self.__right = texture.btn.right
        if weight == -1:
            self.size.y = self.__middle.get_size()[1]
        else:
            self.__left = pygame.transform.scale(self.__left, (self.__left.get_size()[0], weight))
            self.__middle = pygame.transform.scale(self.__middle, (self.__middle.get_size()[0], weight))
            self.__right = pygame.transform.scale(self.__right, (self.__right.get_size()[0], weight))
        self.font: pygame.font.Font = fonts['arial_' + str(int(fontsize))]

    def setscale(self, scale, center):
        self.scale = scale
        self.center = pygame.Vector2(center)

    def tick(self, typ, *args):
        """
        刻循环
        :param typ: 刻循环类型
        :param args: 参数？
        :return: `None`
        """
        if typ == MOUSE_MOTION or typ == MOUSE_CLICK:
            col = False
            if self.rect is not None:
                col = self.rect.collidepoint(*args[0])
            if col:  # 如果碰撞
                self.__bgNow = mixin(pygame.color.Color(self.__bgNow),pygame.color.Color(self.hovcolor),0.5)
                self.__bgAlpha=self.__bgAlpha * 0.5 + 100
                if typ == MOUSE_CLICK:
                    self.__bgNow = mixin(pygame.color.Color(self.__bgNow),pygame.color.Color(self.activecolor),0.5)
                    if not self.is_click:self.is_click=True

                elif self.is_click:
                    self.is_click=False
                    if self.command is not None:
                        self.command()
            else:
                self.is_click=False
                self.__bgNow = mixin(pygame.color.Color(self.__bgNow),pygame.color.Color(self.bg),0.5)
                self.__bgAlpha=self.__bgAlpha * 0.5
            return
        self.is_click=False

    def update(self):
        """帧循环"""
        a = self.font.render(self.text, 1, self.fg)

        self.surface.blit(self.__middle, (self.pos.x - self.size.x / 2, self.pos.y))
        self.surface.blit(self.__left, (self.pos.x - self.size.x / 2, self.pos.y))
        self.surface.blit(self.__right, (self.pos.x + self.size.x / 2 - self.__right.get_size()[0], self.pos.y))

        rect=pygame.Surface((self.size.x, self.__middle.get_size()[1]))
        pygame.draw.rect(rect, self.__bgNow, (
            (0,0), (self.size.x, self.__middle.get_size()[1])))

        rect.set_alpha(self.__bgAlpha)
        self.rect=pygame.rect.Rect(((self.pos.x - self.size.x / 2, self.pos.y),(self.size.x, self.__middle.get_size()[1])))

        self.surface.blit(rect, (self.pos.x - self.size.x / 2, self.pos.y))


        rect = a.get_size()
        self.surface.blit(a, (self.pos.x - rect[0] / 2 + self.__left.get_size()[0] / 2,
                              self.pos.y - rect[1] / 2 + self.__middle.get_size()[1] / 2))


        #一堆石山代码


class LabelPy:
    def __init__(self, master, x, y, text, length, weight=-1, fg='black', bg=None, fontsize=30):
        """
        标签类
        :param master: 父窗口
        :param x: 坐标x
        :param y: 坐标y
        :param text: 文本
        :param length: 长度
        :param weight: 宽度
        :param fg: 前景色
        :param bg: 背景色
        :param fontsize: 字体
        """

        self.rect: pygame.rect.Rect | pygame.rect.RectType | None = None
        self.scale = 1
        self.transition = 20  #tick
        self.surface: pygame.Surface = master.surface
        self.center = pygame.Vector2(self.surface.get_size()) / 2
        self.pos = pygame.Vector2(x, y)
        self.text = text
        self.size = pygame.Vector2(length, weight)
        self.fg = fg
        self.bg = bg

        self.font: pygame.font.Font = fonts['arial_' + str(int(fontsize))]

    def setscale(self, scale, center):
        self.scale = scale
        self.center = pygame.Vector2(center)

    def tick(self, typ, *args):
        """
        刻循环
        :param typ: 刻循环类型(无)
        :param args:
        :return: `None`
        """
        return

    def update(self):
        """帧循环"""
        a = self.font.render(self.text, 1, self.fg)
        rect = a.get_size()

        if self.bg is not None:
            self.rect = pygame.draw.rect(self.surface, self.bg, (
                (self.pos.x - self.size.x / 2, self.pos.y), (self.size.x, self.size.y)))

        self.surface.blit(a, (self.pos.x - rect[0] / 2,
                              self.pos.y - rect[1] / 2 + self.size.y/2))
        #一堆石山代码
