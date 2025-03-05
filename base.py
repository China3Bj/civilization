import pygame
import tomllib
import numba
print('numbaVer:',numba.__version__)
pygame.init()
print('pygameVer:',pygame.__version__)
__all__=['pygame','config','numba','tomllib']
with open('config.toml', 'rb') as f:
    try:
        config=tomllib.load(f)
    except:
        pass

