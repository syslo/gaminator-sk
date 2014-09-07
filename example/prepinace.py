import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'src')))

from gaminator import *

class Hrac(Vec):

    def nastav(self):
        self.miestoHore = 10
        self.miestoDole = 10
        self.miestoVpravo = 10
        self.miestoVlavo = 10
        self.x = 200
        self.y = 200

    def nakresli(self, kreslic):
        kreslic.elipsa((-10, -10), 21, 21)

    def krok(self):
        if self.svet.stlacene[pygame.K_UP]:
            self.y -= 2
        if self.svet.stlacene[pygame.K_DOWN]:
            self.y += 2
        if self.svet.stlacene[pygame.K_RIGHT]:
            self.x += 2
        if self.svet.stlacene[pygame.K_LEFT]:
            self.x -= 2


class Prepinac(Vec):

    def nastav(self):
        self.miestoHore = 10
        self.miestoDole = 10
        self.miestoVpravo = 10
        self.miestoVlavo = 10
        self.x = 200
        self.y = 200
        self.farba = Farba.CERVENA

    def nakresli(self, kreslic):
        kreslic.farba = self.farba
        kreslic.obdlznik((-10, -10), 21, 21)

    @priZrazke(Hrac)
    def prepni_sa(self, hrac):
        if self.farba == Farba.CERVENA:
            self._world.nastalaUdalost("modra")
        else:
            self._world.nastalaUdalost("cervena")
        hrac.x = 200
        hrac.y = 200

    @priUdalosti("cervena")
    def bud_cerveny(self):
        self.farba = Farba.CERVENA
        okno.nazov = "cervena"


    @priUdalosti("modra")
    def bud_modry(self):
        self.farba = Farba.MODRA.zmixuj(Farba.BIELA)
        okno.nazov = "modra"


class SuperPrepinac(Prepinac):

    def bud_modry(self):
        self.farba = Farba.MODRA
        self._world.nacasujUdalost(1000, "zlta")

    def nakresli(self, kreslic):
        kreslic.farba = self.farba
        kreslic.mnohouholnik([
            (-10, 0), (-4, -4), (0, -10), (4, -4),
            (10, 0), (4, 4), (0, 10), (-4, 4)
        ])

    @priUdalosti("zlta")
    def bud_zlty(self):
        self.farba = Farba.ZLTA


class Hra(Svet):

     def nastav(self):
         Hrac(self)

         p1 =Prepinac(self)
         p1.x += 50
         p2 = Prepinac(self)
         p2.x -= 50
         p3 = Prepinac(self)
         p3.y -= 50
         p4 = SuperPrepinac(self)
         p4.y += 50

hra.fps = 50
hra.start(Hra())

