#  -*- coding: utf-8 -*-

from .thing import Vec
from .color import Farba
import pygame
import os

class SurfaceVec(Vec):

    def __init__(self, *args, **kwargs):
        self._orez_hore = 0
        self._orez_dole = 0
        self._orez_vpravo = 0
        self._orez_vlavo = 0
        self._zarovnajX = 0.5
        self._zarovnajY = 0.5
        self._shiftX = 0
        self._shiftY = 0
        self._surface = pygame.Surface((0, 0))
        super(SurfaceVec, self).__init__(*args, **kwargs)

    @property
    def orez_hore(self):
        return self._orez_hore

    @orez_hore.setter
    def orez_hore(self, value):
        self._orez_hore = value
        self._recalculate()

    @property
    def orez_dole(self):
        return self._orez_dole

    @orez_dole.setter
    def orez_dole(self, value):
        self._orez_dole = value
        self._recalculate()

    @property
    def orez_vpravo(self):
        return self._orez_vpravo

    @orez_vpravo.setter
    def orez_vpravo(self, value):
        self._orez_vpravo = value
        self._recalculate()

    @property
    def orez_vlavo(self):
        return self._orez_vlavo

    @orez_vlavo.setter
    def orez_vlavo(self, value):
        self._orez_vlavo = value
        self._recalculate()

    @property
    def zarovnajX(self):
        return self._zarovnajX

    @zarovnajX.setter
    def zarovnajX(self, value):
        self._zarovnajX = value
        self._recalculate()

    @property
    def zarovnajY(self):
        return self._zarovnajY

    @zarovnajY.setter
    def zarovnajY(self, value):
        self._zarovnajY = value
        self._recalculate()

    def _recalculate(self):
        w = self._surface.get_width()
        h = self._surface.get_height()
        self._shiftX = int(self._zarovnajX*w)
        self._shiftY = int(self._zarovnajY*h)
        self.miesto_hore = self._shiftY - self._orez_hore
        self.miesto_dole = h - self._shiftY - self._orez_dole
        self.miesto_vlavo = self._shiftX - self._orez_vlavo
        self.miesto_vpravo = w - self._shiftX - self._orez_vpravo

    def _set_surface(self, surface):
        self._surface = surface
        self._recalculate()

    def nakresli(self, kreslic):
        kreslic._surface.blit(self._surface,
                              (self.x-self._shiftX, self.y-self._shiftY))


class Obrazok(SurfaceVec):

    def nastavSubor(self, *paths):
        path = os.path.join(*paths)
        self._set_surface(pygame.image.load(path))


class Text(SurfaceVec):

    def __init__(self, *args, **kwargs):
        self._text = "TEXT"
        self._farba = Farba.CIERNA
        self._velkost = 12
        super(Text, self).__init__(*args, **kwargs)

    def aktualizuj(self, text=None, farba=None, velkost=None):
        if text is not None:
            self._text = text
        if farba is not None:
            self._farba = farba
        if velkost is not None:
            self._velkost = velkost
        font = pygame.font.SysFont(None, self._velkost)
        self._set_surface(font.render(self._text, True, self._farba))