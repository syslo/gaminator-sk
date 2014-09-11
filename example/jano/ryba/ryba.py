import sys, os, math
sys.path.append(os.path.abspath(os.path.join('..','..', '..', 'src')))

from gaminator import *
from random import randint
from collections import deque

EPS = 1e-7
Farba.VODA = Farba(144, 144, 255)
Farba.JEDLO = Farba(255, 200, 0)
Farba.VZDUCH = Farba(240, 240, 255)

def interpoluj(v1, v2, pomer_v1):
    return v1*pomer_v1 + v2*(1.0-pomer_v1)

class MorskyPohyb: # musi to byt vec
    # gravitacna konstanta
    g = 9.8
    # hustota:
    ro_voda = 1.0
    ro_vzduch = 0.001
    ro_hlbka = 0.001
    ro_vec = 0.5
    # odpory: 
    #   - povrchove napatie, trenie navyse, ked ide vec cez hladinu
    #   - aeordinamycka konstant
    odpor_hladina = 0.02
    odpor = 0.01

    def init(self, podVodou = True):
        self.rychlost_x = 0
        self.rychlost_y = 0
        self.acc_x = 0
        self.acc_y = 0
        # aka cast je ponorena
        self.ponorene = podVodou 

    def zratajSily(self):
        vyska = self.miestoDole + self.miestoHore
        #sirka = self.miestoVlavo + self.miestoVpravo
        #hrubka = (vyska + sirka) * 0.5

        hlbka = (self.y + self.miestoDole - self.svet.vzduch)
        self.ponorene = max(0.0, min(1.0, hlbka/float(vyska)))
        ro1 = (self.ro_voda + hlbka*self.ro_hlbka) / float(self.ro_vec)
        ro2 = self.ro_vzduch / float(self.ro_vec)
        self.acc_y += (1.0 - interpoluj(ro1, ro2, self.ponorene)) * self.g

    def pohyb(self):
        self.rychlost_x += self.acc_x 
        self.rychlost_y += self.acc_y
        self.acc_x = 0.0
        self.acc_y = 0.0
        if (self.ponorene > EPS and self.ponorene < 1.0-EPS):
            self.rychlost_y *= (1.0 - self.odpor_hladina)
        odpor = self.odpor * interpoluj(self.ro_voda, 
            self.ro_vzduch, self.ponorene)
        self.rychlost_x *= (1.0 - odpor)
        self.rychlost_y *= (1.0 - odpor)
        
        self.x += self.rychlost_x / float(hra.fps)
        self.y += self.rychlost_y / float(hra.fps)
        
        if self.x > okno.sirka:
            self.x -= okno.sirka
        if self.x < 0:
            self.x += okno.sirka
        


class Stena(Obrazok):
    def nastav(self):
        self.nastavSubor("stena.png")
        # chceme aby kolizie ignorovali obrazok
        self.maskuj = False

class Jedlo(Obrazok, MorskyPohyb):
    odpor = 0.01
    odpor_hladina = 0.1

    def nastav(self):
        self.nastavSubor("jedlo.png")
        self.z = -1
        self.suche = 1.0
        self.usus = 1.0
        self.init(False)
        self.y = -20
        self.x = randint(10, okno.sirka-10)
    
    def krok(self):
        if self.ponorene > 0.1:
            self.suche *= 0.998*self.usus
            self.usus = 1.0
        self.ro_vec = 2.0 - self.suche*1.8
        self.zratajSily()
        self.pohyb()

        if self.y > okno.vyska + 20 or self.suche < 0.01:
            self.znic()

    def nakresli(self, kreslic):
        kreslic.farba = interpoluj(Farba.JEDLO, Farba.VODA, self.suche)
        kreslic.elipsa((-8, -8), 16, 16)
    
    @priZrazke(Stena)
    def rozmoc(self, stena):
        self.usus = 0.85


class Ryba(Animacia, MorskyPohyb):
    ro_vec = 0.95
    odpor = 0.03
    sila = 10.0

    def nastav(self):
        # nacita obrazky pre animacie
        self.vytvorZMriezky(40,46,"rybka.png")
        # smer ktorym je otocena (0 = vlavo, 1 = vpravo)
        self.snimka = 1
        self.init() 

    def krok(self):
        self.prev_x, self.prev_y = self.x, self.y
        self.prev_smer = self.snimka

        self.zratajSily()

        if(self.svet.stlacene[pygame.K_UP]):
            self.acc_y -= self.sila*self.ponorene
        if(self.svet.stlacene[pygame.K_DOWN]):
            self.acc_y += self.sila*self.ponorene
        if(self.svet.stlacene[pygame.K_LEFT]):
            self.acc_x -= self.sila*self.ponorene
            self.snimka = 0
        if(self.svet.stlacene[pygame.K_RIGHT]):
            self.acc_x += self.sila*self.ponorene
            self.snimka = 1
           
        self.pohyb()


    @priZrazke(Jedlo)
    def zjedene(self, jedlo):
        y = self.y + 8.0
        if y < jedlo.y and (jedlo.x < self.x)^self.snimka:
            jedlo.znic()
        else:
            jedlo.acc_x += 200.0 / (jedlo.x - self.x + 
                (5.0, -5.0)[jedlo.x < self.x])
            jedlo.acc_y += 200.0 / (jedlo.y - y +
                (5.0, -2.0)[jedlo.y < y])
    
    @priZrazke(Stena)
    def zastav(self, stena):
        r_x = self.rychlost_x / float(hra.fps)
        r_y = self.rychlost_y / float(hra.fps)
        if self.snimka != self.prev_smer:
            self.snimka = 1-self.snimka
            if not self.narazilBySom(Stena, 0, 0):
                return
            self.snimka = 1-self.snimka

        if not self.narazilBySom(Stena, 0, -r_y):
            self.y -= r_y
            self.rychlost_y *= 0.5
        elif not self.narazilBySom(Stena, -r_x, 0):
            self.x -= r_x
            self.rychlost_x *= 0.5
        else:
            self.x, self.y = self.prev_x, self.prev_y
            r_x *= 0.5
            r_y *= 0.5


class Hra(Svet):
    mriezka = 32
    vzduch = 80

    legenda = {
        '#':Stena,
        'R':Ryba,
    }

    def vytvorLevel(self, subor):
        self.level = open(subor, 'r').read().strip().split('\n')
        if not len(self.level):
            print "Prazny self.level!!"
            return
        self.riadky = len(self.level)
        self.stlpce = len(self.level[0])
        okno.vyska = self.riadky * self.mriezka
        okno.sirka = self.stlpce * self.mriezka
        for i in range(self.riadky):
            for j in range(self.stlpce):
                if self.level[i][j] in self.legenda:
                    vec = self.legenda[self.level[i][j]](self)
                    vec.y = i * self.mriezka + self.mriezka//2
                    vec.x = j * self.mriezka + self.mriezka//2
                    vec.vznik_y, vec.vznik_x = vec.y, vec.x

    def nastav(self):
        okno.nazov = "Akvarium"
        self.level = ['#']
        self.vytvorLevel('akvarium.txt')
        
    
    def nakresli(self,kreslic):
        kreslic.farba = Farba.VZDUCH
        kreslic.obdlznik((0,0),okno.sirka,self.vzduch)
        kreslic.farba = Farba.VODA
        kreslic.obdlznik((0,self.vzduch),okno.sirka,okno.vyska-self.vzduch)

    def krok(self):
        if randint(0,50) == 0:
            Jedlo(self)

    @priUdalosti("KLAVES DOLE")
    def klaves(self, klaves, unicode):
        if klaves == pygame.K_ESCAPE:
            hra.koniec()

hra.start(Hra())

