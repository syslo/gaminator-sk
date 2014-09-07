import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', '..', 'src')))

from gaminator import *
from random import randint
from collections import deque

MRIEZKA = 32
NEKONECNO = 1023456789

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
    
    # kolko zkore dostane za co
    skore_jedlo = 1
    skore_cukrik = 2
    skore_duch = 10

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
        self.svet.aktualizujVzdialenosti(self)
        if self.svet.pocet(Jedlo) == 0:
            hra.skore += 1
    
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
        hra.skore += self.skore_jedlo

    @priZrazke(Cukrik)
    def boost(self, cukrik):
        cukrik.znic()
        hra.skore += self.skore_cukrik
        self.svet.nastalaUdalost("Boost")
    
    @priUdalosti("Pacman zomrel")
    def zomri(self):
        self.pohyb = 0
        self.stojim = True 
        hra.skore = 0
        self.x, self.y = self.vznik_x, self.vznik_y

class Duch(Animacia):
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    # ako dlho ma byt zblednuty, ked Pacman zjedol Cukrik
    cas_zblednutia = 12
    cas_blikania = 1
    pocet_inst = 0

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
        self.snimka = Duch.pocet_inst
        Duch.pocet_inst += 1
        # rychlost pohybu v pixloch za krok
        # kolko pixelov pohybu mi ostava
        self.pohyb = 0
        # idealne delitel cisla MRIEZKA pre plynulejsi pohyb
        self.rychlost = 1
   
        self.svet.aktualizujVzdialenosti(self)

    # nasledovne konstanty ovplyvnuju pohyb ducha, cim vyssie skore,
    # tym vacsia pravdepodobnost, ze sa duch pohne danym smerom
    skore_rovno = 7 
    skore_vzad = 3
    skore_zaboc = 5
    # aky velky vplyv na vyber ma vzdialenost od Pacmana
    # (normalne, bledy)
    skore_vzd = (2, -2)
    skore_inyduch = -5

    # nahodne si vyber smer, ktorym sa budes dalej hybat
    def zacniPohyb(self):
        skore = [0]*4
        skore[self.smer] += self.skore_rovno
        skore[(self.smer+2)%4] += self.skore_vzad
        skore[(self.smer+1)%4] += self.skore_zaboc
        skore[(self.smer-1)%4] += self.skore_zaboc
        vzd = self.svet.vzdialenost(self.x, self.y)

        for i in range(len(skore)):
            skore[i] += ((vzd - 
                self.svet.vzdialenost(self.x + MRIEZKA*self.dx[i],
                                      self.y + MRIEZKA*self.dy[i]) ) * 
                self.skore_vzd[self.bledost > 0])
            if self.narazilBySom(Duch, MRIEZKA*self.dx[i], MRIEZKA*self.dy[i]):
                skore[i] += self.skore_inyduch
            if self.narazilBySom(Stena, MRIEZKA*self.dx[i], MRIEZKA*self.dy[i]):
                skore[i] = 0
            if skore[i] < 0:
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
        if (self.bledost > 0 and
            self.bledost < hra.fps * self.cas_blikania and
            self.bledost % 8 == 0):
            self.typ = 1-self.typ
        if self.bledost == 0:
            self.odbledni()

    @priUdalosti("Boost")
    def zbledni(self):
        self.bledost = hra.fps * self.cas_zblednutia
        self.typ = 1

    def odbledni(self):
        self.typ = 0

    @priZrazke(Pacman)
    def suboj(self, pacman):
        if self.bledost > 0:
            hra.skore += pacman.skore_duch
            self.zomri()
        else:
            self.svet.nastalaUdalost("Pacman zomrel")
    
    @priUdalosti("Pacman zomrel")
    def zomri(self):
        self.pohyb = 0
        self.bledost = 0
        self.typ = 0
        self.x, self.y = self.vznik_x, self.vznik_y

class Skore(Text):
    def nastav(self):
        self.aktualizuj('Skore: ', Farba.ZELENA, 30)

    def krok(self):
        self.aktualizuj('Skore: %s' % hra.skore)
    
class Pozadie(Vec):
    def nastav(self):
        self.farba = Farba.CIERNA
        self.x = 0
        self.y = 0
        # vykresli sa ako prve, lebo je najhlbsie
        self.z = -NEKONECNO

    def nakresli(self, kreslic):
        kreslic.farba = self.farba
        kreslic.obdlznik((0, 0), okno.sirka, okno.vyska)

class Hra(Svet):
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    mriezka = 32
    legenda = {
        '#':Stena,
        '.':Jedlo,
        'O':Cukrik,
        'D':Duch,
        'P':Pacman,
        'o':Skore,
    }

    # aktualizuje tepelnu mapu, podla pacmana
    def aktualizujVzdialenosti(self, pacman):
        self.vzd = [[NEKONECNO for policko in riadok] for riadok in self.level]
        fronta = deque()
        y, x = pacman.y // MRIEZKA, pacman.x // MRIEZKA
        self.vzd[y][x] = 0
        fronta.append((y,x))
        while len(fronta):
            y, x = fronta.popleft()
            if self.level[y][x] == '#':
                continue
            for i in range(len(self.dx)):
                yy, xx = y+self.dy[i], x+self.dx[i]
                if self.vzd[yy][xx] > self.vzd[y][x] + 1:
                    self.vzd[yy][xx] = self.vzd[y][x] + 1
                    fronta.append((yy,xx))

    # vrati vzdialenost od pacmana (pocet policok)
    def vzdialenost(self, x, y):
        y, x = y // MRIEZKA, x // MRIEZKA
        return self.vzd[y][x] 

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
                    vec.vznik_y, vec.vznik_x = vec.y, vec.x

    def nastav(self):
        Pozadie(self)
        self.level = ['#']
        self.vytvorLevel('level1.txt')
    
    @priUdalosti("KLAVES DOLE")
    def klaves(self, klaves, unicode):
        if klaves == pygame.K_ESCAPE:
            hra.koniec()

okno.nazov = "Pacman"
hra.skore = 0
hra.start(Hra())

