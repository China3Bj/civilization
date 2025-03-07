import pygame
import tomllib
import numba
import json
print('numbaVer:',numba.__version__)
pygame.init()
print('pygameVer:',pygame.__version__)
erronBuffer= (b'\x00\x00\x00\x00\x00\x00\xff\x00\xff\xff\x00\xff\x00\x00\x00\x00\x00\x00\xff\x00\xff\xff\x00\xff\xff'
              b'\x00\xff\xff\x00\xff\x00\x00\x00\x00\x00\x00\xff\x00\xff\xff\x00\xff\x00\x00\x00\x00\x00\x00')

class AssetsDict(dict):
    def __getattr__(self, item):
        __g=self[item]
        if type(__g)==dict:
            __g=AssetsDict(__g)
        return __g
    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except:
            _a=pygame.image.frombytes(erronBuffer,(4,4),"RGB")
            return _a

class ConfigDict(dict):
    def __getattr__(self, item):
        __g=self[item]
        if type(__g)==dict:
            __g=ConfigDict(__g)
        return __g

with open('config.toml', 'rb') as f:
    try:
        config=ConfigDict(tomllib.load(f))
        __ass=config['local']['assetsLink']
        with open(__ass, 'rb') as f2:
            assetsLink=AssetsDict(json.load(f2))
            print(assetsLink)
    except:
        raise FileNotFoundError



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
    s=pygame.surface.Surface((100,100))
    PyButton(s,1,1,1)