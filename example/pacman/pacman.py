import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', '..', 'src')))

from gaminator import *
from random import randint

MRIEZKA = 32

class Stena(Obrazok):
    def nastav(self):
        self.nastavSubor("stena.png")
        # chceme aby kolizie ignorovali obrazok
        self.maskuj = False

class Jedlo(Obrazok):
    def nastav(self):
        self.nastavSubor("cukrik.png")
        self.z = -1

class Cukrik(Obrazok):
    def nastav(self):
        self.nastavSubor("velkycukrik.png")
        self.z = -1

class Pacman(Animacia):
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

    def nastav(self):
        # nacita obrazky pre animacie
        self.vytvorZMriezky(MRIEZKA,MRIEZKA,"pacman.png")
        # raz za self.pomalost krokov sa zvysi snimka animacie
        self.pomalost = 4
        # rychlost animacie a zaroven rychlost chodze, 
        # idealne delitel cisla MRIEZKA pre plynulejsi pohyb
        self.rychlost = 2
        # smer ktorym je otoceny (0 = vpravo, 1 = dole, 2 = vlavo, 3 = hore)
        self.typ = 1
        # kolko pixelov pohybu mi ostava
        self.pohyb = 0
        # kvoli animacii chceme vediet, ci sa pacman snazi hybat
        self.stojim = True

    # skontroluje ci nenarazi do steny a ak nie, tak zacne pohyb
    def skusPohnut(self, smer):
        self.stojim = False
        self.typ = smer
        self.pohyb = MRIEZKA
        if self.narazilBySom(Stena, MRIEZKA*self.dx[smer], MRIEZKA*self.dy[smer]):
            self.pohyb = 0

    def krok(self):
        # otcovska trieda je Animacia, cize vdaka tomuto sa Pacman animuje
        super(Pacman, self).krok()
    
        if self.pohyb == 0:
            if self.svet.stlacene[pygame.K_UP]: 
                self.skusPohnut(3)
            if self.svet.stlacene[pygame.K_DOWN]:
                self.skusPohnut(1)
            if self.svet.stlacene[pygame.K_RIGHT]:
                self.skusPohnut(0)
            if self.svet.stlacene[pygame.K_LEFT]:
                self.skusPohnut(2)

        if self.pohyb > 0:
            # pacman sa pohne
            zmena = min(self.rychlost, self.pohyb)
            self.x += self.dx[self.typ]*zmena
            self.y += self.dy[self.typ]*zmena
            self.pohyb -= zmena
        elif self.stojim:
            # resetujeme animaciu
            self.typ = 1
            self.snimka = 0
        else:
            self.stojim = True

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
    # ako dlho ma byt zblednuty, ked Pacman zjedol Cukrik
    cas_zblednutia = 10

    def nastav(self):
        # nacita obrazky pre animacie
        self.vytvorZMriezky(MRIEZKA,MRIEZKA,"duch.png")
        # 0 = normalny, 1 = zblednuty
        self.typ = 0
        # ako dlho este budem zblednuty (v krokoch)
        self.bledost = 0
        # akym smerom som sa naposledy hybal
        self.smer = randint(0,3)
        # akej som farby (cislo od 0 po 3)
        self.snimka = randint(0,3)
        # rychlost pohybu v pixloch za krok
        # kolko pixelov pohybu mi ostava
        self.pohyb = 0
        # idealne delitel cisla MRIEZKA pre plynulejsi pohyb
        self.rychlost = 1

    # nasledovne konstanty ovplyvnuju pohyb ducha, cim vyssie skore,
    # tym vacsia pravdepodobnost, ze sa duch pohne danym smerom
    skore_rovno = 5 
    skore_vzad = 1
    skore_zaboc = 3
    # aky velky vplyv na vyber ma vzdialenost od Pacmana
    skore_vzdialenost = 2

    # nahodne si vyber smer, ktorym sa budes dalej hybat
    def zacniPohyb(self):
        skore = [0]*4
        skore[self.smer] += self.skore_rovno
        skore[(self.smer+2)%4] += self.skore_vzad
        skore[(self.smer+1)%4] += self.skore_zaboc
        skore[(self.smer-1)%4] += self.skore_zaboc

        for i in range(len(skore)):
            if self.narazilBySom(Stena, MRIEZKA*self.dx[i], MRIEZKA*self.dy[i]):
                skore[i] = 0
        celkove_skore = sum(skore)
        if celkove_skore > 0:
            vyber = randint(0, celkove_skore-1)
            smer = 0
            while vyber >= skore[smer]:
                vyber -= skore[smer]
                smer += 1
            self.smer = smer
            self.pohyb = MRIEZKA

    def krok(self):
        if self.pohyb <= 0:
            self.zacniPohyb()

        if self.pohyb > 0:
            # pacman sa pohne
            zmena = min(self.rychlost, self.pohyb)
            self.x += self.dx[self.smer]*zmena
            self.y += self.dy[self.smer]*zmena
            self.pohyb -= zmena

        self.bledost -= 1
        if self.bledost == 0:
            self.odbledni()

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
        # vykresli sa ako prve, lebo je najhlbsie
        self.z = -10000000

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
        self.level = open(subor, 'r').read().strip().split('\n')
        if not len(self.level):
            print "Prazny self.level!!"
            return
        self.riadky = len(self.level)
        self.stlpce = len(self.level[0])
        okno.sirka = self.riadky * self.mriezka
        okno.vyska = self.stlpce * self.mriezka
        for i in range(self.riadky):
            for j in range(self.stlpce):
                if self.level[i][j] in self.legenda:
                    vec = self.legenda[self.level[i][j]](self)
                    vec.y = i * self.mriezka + self.mriezka//2
                    vec.x = j * self.mriezka + self.mriezka//2

    def nastav(self):
        Pozadie(self)
        self.level = ['#']
        self.vytvorLevel('level1.txt')

hra.start(Hra())

