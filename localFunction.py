from base import *


def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    if delta == 0:
        h = 0
    elif cmax == r:
        h = ((g - b) / delta) % 6
    elif cmax == g:
        h = ((b - r) / delta) + 2
    else:
        h = ((r - g) / delta) + 4

    h = h * 60
    if h < 0:
        h += 360

    if cmax == 0:
        s = 0
    else:
        s = delta / cmax

    v = cmax

    return h, s, v


def hsv_to_rgb(h, s, v):
    h = h % 360
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        r1, g1, b1 = c, x, 0
    elif 60 <= h < 120:
        r1, g1, b1 = x, c, 0
    elif 120 <= h < 180:
        r1, g1, b1 = 0, c, x
    elif 180 <= h < 240:
        r1, g1, b1 = 0, x, c
    elif 240 <= h < 300:
        r1, g1, b1 = x, 0, c
    else:
        r1, g1, b1 = c, 0, x

    r = (r1 + m) * 255
    g = (g1 + m) * 255
    b = (b1 + m) * 255

    return r, g, b


def mixin(col1:pygame.color.Color,col2:pygame.color.Color,perc):
    mixin1=rgb_to_hsv(col1.r,col1.g,col1.b)
    mixin2=rgb_to_hsv(col2.r,col2.g,col2.b)
    if mixin1[0]==0:
        mixin1=(list(mixin1))
        mixin1[0]=mixin2[0]
        mixin1=tuple(mixin1)
    now=hsv_to_rgb(*[
        (mixin1[i]*perc+mixin2[i]*(1-perc)) for i in range(3)
    ])
    return now

class Widget:# todo Widget
    pass

class ButtonPy:
    def __init__(self,surface,texture,x,y,text,length,weight=-1,fg='black',bg='gray',hovcolor='blue',activecolor='gray',fontsize=30):
        self.rect:pygame.rect.Rect|pygame.rect.RectType|None = None
        self.scale = 1
        self.transition=20#tick
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

        self.__bgNow=self.bg
        self.active=0
        self.hov=0
        self.__hovTime=-1
        self.__hovHave=0

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

    def tick(self,typ,*args):
        if typ==MOUSE_MOTION:
            col=False
            if self.rect is not None:
                col=self.rect.collidepoint(*args)
            if col:
                self.hov=col
                if self.__hovTime==-1 and not self.__hovHave:
                    self.__hovTime=self.transition
                    self.__bgNow=self.bg
                    self.__hovHave=1
                elif self.__hovTime<=0 and  self.__hovHave:
                    self.__bgNow=self.hovcolor
                    self.__hovTime=-1
                    self.__hovHave=1
                else:
                    self.__hovTime-=1
                    mixin1=pygame.color.Color(self.hovcolor)
                    mixin2=pygame.color.Color(self.bg)
                    self.__bgNow=mixin(mixin2,mixin1,(self.__hovTime/self.transition))
            else:
                self.hov = col
                if self.__hovTime == -1 and self.__hovHave:
                    self.__hovTime = self.transition
                    self.__bgNow = self.hovcolor
                    self.__hovHave = 0
                elif self.__hovTime <= 0 and not self.__hovHave:
                    self.__bgNow = self.bg
                    self.__hovTime = -1
                    self.__hovHave=0
                else:
                    self.__hovTime -= 1
                    mixin1 = pygame.color.Color(self.hovcolor)
                    mixin2 = pygame.color.Color(self.bg)
                    self.__bgNow = mixin(mixin2, mixin1, (1-self.__hovTime / self.transition))

    def update(self):

        a=self.font.render(self.text,1,self.fg)
        rect=a.get_size()

        self.rect=pygame.draw.rect(self.surface, self.__bgNow, ((self.pos.x - self.size.x / 2, self.pos.y),(self.size.x,self.__middle.get_size()[1])))
        self.surface.blit(a,(self.pos.x-rect[0]/2+self.__left.get_size()[0]/2,self.pos.y-rect[1]/2+self.__middle.get_size()[1]/2))
        self.surface.blit(self.__middle,(self.pos.x-self.size.x/2,self.pos.y))
        self.surface.blit(self.__left,(self.pos.x-self.size.x/2,self.pos.y))
        self.surface.blit(self.__right,(self.pos.x+self.size.x/2-self.__right.get_size()[0],self.pos.y))
