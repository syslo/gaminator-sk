#  -*- coding: utf-8 -*-

from .thing import Vec
from .color import Farba
import pygame
import os

class SurfaceVec(Vec):

    def __init__(self, *args, **kwargs):
        self._maskuj = True
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
    def maskuj(self):
        return self._maskuj

    @maskuj.setter
    def maskuj(self, value):
        self._maskuj = value
        self._recalculate()

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
        self.miestoHore = self._shiftY - self._orez_hore
        self.miestoDole = h - self._shiftY - self._orez_dole
        self.miestoVlavo = self._shiftX - self._orez_vlavo
        self.miestoVpravo = w - self._shiftX - self._orez_vpravo
        if self.maskuj:
            self._mask = pygame.mask.from_surface(self._surface)
        else:
            self._mask = None

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

# Animovany obrazok.
# Ma dve zlozky -- typ a snimku.
# Defaultne sa kazdych `pomalost` krokov zvacsi snimla o `rychlost`.
# Da sa vyrobit s dlazdicoveho obrazku, typ je riadok a snimky su stlpce

class Animacia(SurfaceVec):
    def __init__(self, *args, **kwargs):
        self._frame_list = []
        self._typ = 0
        self._snimka = 0
        self.rychlost = 1
        self.pomalost = 1
        self._cakaj = 0
        super(Animacia, self).__init__(*args, **kwargs)
        self._set_surface(self._surfaces[self._typ][self._snimka])

    @property
    def typ(self):
        return self._typ

    @typ.setter
    def typ(self, value):
        self._typ = value % len(self._surfaces)
        self._set_surface(self._surfaces[self._typ][self._snimka])

    @property
    def snimka(self):
        return self._snimka

    @snimka.setter
    def snimka(self, value):
        self._snimka = value % len(self._surfaces[self._typ])
        self._set_surface(self._surfaces[self._typ][self._snimka])

    def vytvorZMriezky(self, sirka, vyska, *paths, **kwargs):
        path = os.path.join(*paths)
        mriezka = pygame.image.load(path)
        celasirka = mriezka.get_width()
        celavyska = mriezka.get_height()
        self._surfaces = []
        for riadok in range(celavyska//vyska):
            self._surfaces.append([])
            for stlpec in range(celasirka//sirka):
                surface = pygame.Surface((sirka, vyska),
                    flags=mriezka.get_flags())
                surface.blit(mriezka, (0,0),
                    (stlpec*sirka, riadok*vyska, sirka, vyska))
                self._surfaces[riadok].append(surface)

        if kwargs.get("splosti", False):
            surfaces = []
            map(surfaces.extend, self._surfaces)
            self._surfaces = [surfaces]

    def krok(self):
        self._cakaj = (self._cakaj + 1) % self.pomalost
        if self.rychlost and self._cakaj == 0:
            self.snimka += self.rychlost


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
