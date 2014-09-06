import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', '..', 'src')))

from gaminator import *
from random import randint

MRIEZKA = 32

class Stena(Obrazok):
    def nastav(self):
        self.nastavSubor("stena.png")
        self.maskuj = False

class Jedlo(Obrazok):
    def nastav(self):
        self.nastavSubor("cukrik.png")

class Cukrik(Obrazok):
    def nastav(self):
        self.nastavSubor("velkycukrik.png")

class Pacman(Animacia):
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

    def nastav(self):
        self.vytvorZMriezky(MRIEZKA,MRIEZKA,"pacman.png")
        self.pomalost = 3
        self.rychlost = 1
        self.typ = 1
        self.pohyb = 0

    def krok(self):
        super(Pacman, self).krok()
        if self.pohyb == 0:
            if self.svet.stlacene[pygame.K_UP]:
                self.typ = 3
                self.pohyb = MRIEZKA
            if self.svet.stlacene[pygame.K_DOWN]:
                self.typ = 1
                self.pohyb = MRIEZKA
            if self.svet.stlacene[pygame.K_RIGHT]:
                self.typ = 0
                self.pohyb = MRIEZKA
            if self.svet.stlacene[pygame.K_LEFT]:
                self.typ = 2
                self.pohyb = MRIEZKA

        if self.pohyb > 0:
            zmena = min(self.rychlost, self.pohyb)
            self.x += self.dx[self.typ]*zmena
            self.y += self.dy[self.typ]*zmena
            self.pohyb -= zmena
        else:
            self.typ = 1
            self.snimka = 0

    @priZrazke(Jedlo)
    def zjedene(self, jedlo):
        jedlo.znic()

    @priZrazke(Cukrik)
    def boost(self, cukrik):
        cukrik.znic()
        self.svet.nastalaUdalost("Boost")

class Duch(Animacia):
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    cas_zblednutia = 10

    def zmenSmer(self):
        stary_smer = self.smer
        while (stary_smer == self.smer
            or (stary_smer == (self.smer+2) % 2 and randint(0,1))
        ):
            self.smer = randint(0,3)


    def nastav(self):
        self.vytvorZMriezky(MRIEZKA,MRIEZKA,"duch.png")
        self.typ = 0
        self.bledost = 0
        self.smer = randint(0,3)
        self.snimka = randint(0,3)
        self.maskuj = False

    def krok(self):
        self.pred_x = self.x
        self.pred_y = self.y
        if (self.x % MRIEZKA == MRIEZKA//2 and
            self.y % MRIEZKA == MRIEZKA//2 and
            randint(0,3) == 0):
            self.zmenSmer()

        self.bledost -= 1
        if self.bledost == 0:
            self.odbledni()
        self.x += self.dx[self.smer]
        self.y += self.dy[self.smer]

    @priZrazke(Stena)
    def narazil(self, stena):
        self.x = self.pred_x
        self.y = self.pred_y
        self.zmenSmer()

    @priUdalosti("Boost")
    def zbledni(self):
        self.bledost = hra.fps * self.cas_zblednutia
        self.typ = 1

    def odbledni(self):
        self.typ = 0

class Pozadie(Vec):
    def nastav(self):
        self.farba = Farba.CIERNA
        self.x = 0
        self.y = 0
        self.z = -10000

    def nakresli(self, kreslic):
        kreslic.farba = self.farba
        kreslic.obdlznik((0, 0), okno.sirka, okno.vyska)

class Hra(Svet):
    mriezka = 32
    legenda = {
        '#':Stena,
        '.':Jedlo,
        'o':Cukrik,
        'D':Duch,
        'P':Pacman,
    }

    def vytvorLevel(self, subor):
        level = open(subor, 'r').read().strip().split('\n')
        if not len(level):
            print "Prazny level!!"
            return
        self.riadky = len(level)
        self.stlpce = len(level[0])
        okno.sirka = self.riadky * self.mriezka
        okno.vyska = self.stlpce * self.mriezka
        for i in range(self.riadky):
            for j in range(self.stlpce):
                vec = self.legenda[level[i][j]](self)
                vec.y = i * self.mriezka + self.mriezka//2
                vec.x = j * self.mriezka + self.mriezka//2

    def nastav(self):
        Pozadie(self)
        self.vytvorLevel('level1.txt')

hra.start(Hra())

