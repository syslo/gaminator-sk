import sys, os, math
sys.path.append(os.path.abspath(os.path.join('..','..', '..', 'src')))

from gaminator import *
from random import randint
from collections import deque

class Stena(Obrazok):
    def nastav(self):
        self.nastavSubor("stena.png")
        # chceme aby kolizie ignorovali obrazok
        self.maskuj = False

class Jedlo(Obrazok):
    grav = [0.2, 0.02, 0.02/90.0]
    odpor = [0.005, 0.05]
    trenie = [0.001, 0.001]
    
    def nastav(self):
        self.nastavSubor("cukrik.png")
        self.z = -1
        self.rychlost_y = 0.0
        self.mokra = 0
        self.y = -20
        self.x = randint(10, okno.sirka-10)
    
    def voVode(self):
        voda = self.y > self.svet.vzduch
        if voda != self.mokra: 
            self.brzda = 0.7
        self.mokra = voda
        return self.mokra
    
    def krok(self):
        self.brzda = 1
        sila_y = self.grav[self.voVode()]
        sila_y -= self.y*self.grav[2]
        self.rychlost_y += sila_y;
        
        self.rychlost_y *= (1.0-self.odpor[self.voVode()])
        
        self.y += self.rychlost_y
        if self.y > okno.vyska + 20:
            self.znic()


class Ryba(Animacia):
    # na vzuchu, vo vode, 1px hlbky
    grav = [0.1, 0.01, 0.01/160.0]
    odpor = [0.001, 0.03]
    trenie = [0.001, 0.001]
    sila = [0.0, 0.2]

    def voVode(self):
        voda = self.y > self.svet.vzduch
        if voda != self.mokra: 
            self.brzda = 0.7
        self.mokra = voda
        return self.mokra

    def rych(self):
        return math.sqrt(self.rychlost_x**2 + self.rychlost_y**2)

    def nastav(self):
        # nacita obrazky pre animacie
        self.vytvorZMriezky(40,46,"rybka.png")
        # smer ktorym je otocena (0 = vlavo, 1 = vpravo)
        self.snimka = 1
        self.rychlost_x = 0.0
        self.rychlost_y = 0.0

        self.mokra = 1

    def krok(self):
        self.prev_x, self.prev_y = self.x, self.y
        self.prev_smer = self.snimka
        self.brzda = 1
        sila_x = 0
        sila_y = self.grav[self.voVode()]
        sila_y -= self.y*self.grav[2]

        if(self.svet.stlacene[pygame.K_UP]):
            sila_y -= self.sila[self.voVode()]
        if(self.svet.stlacene[pygame.K_DOWN]):
            sila_y += self.sila[self.voVode()]
        if(self.svet.stlacene[pygame.K_LEFT]):
            sila_x -= self.sila[self.voVode()]
            self.snimka = 0
        if(self.svet.stlacene[pygame.K_RIGHT]):
            sila_x += self.sila[self.voVode()]
            self.snimka = 1
           
        self.rychlost_x += sila_x;
        self.rychlost_y += sila_y;
        
        rychlost = self.rych()
        rych = rychlost
        rychlost *= (1.0-self.odpor[self.voVode()])
        rychlost = max(0.0, rychlost - self.trenie[self.voVode()])
        if (rych > 0):
            self.rychlost_x *= rychlost/rych
            self.rychlost_y *= self.brzda*rychlost/rych

        self.x += self.rychlost_x
        self.y += self.rychlost_y

        if self.x > okno.sirka:
            self.x -= okno.sirka
        if self.x < 0:
            self.x += okno.sirka

    @priZrazke(Jedlo)
    def zjedene(self, jedlo):
        jedlo.znic()
    
    @priZrazke(Stena)
    def zastav(self, stena):
        if self.snimka != self.prev_smer:
            self.snimka = 1-self.snimka
            if not self.narazilBySom(Stena, 0, 0):
                return
            self.snimka = 1-self.snimka

        if not self.narazilBySom(Stena, 0, -self.rychlost_y):
            self.y -= self.rychlost_y
            self.rychlost_y *= 0.5
        elif not self.narazilBySom(Stena, -self.rychlost_x, 0):
            self.x -= self.rychlost_x
            self.rychlost_x *= 0.5
        else:
            self.x, self.y = self.prev_x, self.prev_y
            self.rychlost_x *= 0.5
            self.rychlost_y *= 0.5


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
        kreslic.farba = Farba(244,244,255)
        kreslic.obdlznik((0,0),okno.sirka,self.vzduch)
        kreslic.farba = Farba(144,144,255)
        kreslic.obdlznik((0,self.vzduch),okno.sirka,okno.vyska-self.vzduch)

    def krok(self):
        if randint(0,50) == 0:
            Jedlo(self)

    @priUdalosti("KLAVES DOLE")
    def klaves(self, klaves, unicode):
        if klaves == pygame.K_ESCAPE:
            hra.koniec()

hra.start(Hra())

