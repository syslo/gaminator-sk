from gaminator import *
import math
import random

from bisect import bisect_left

def binary_search(a, x, lo=0, hi=None):
    hi = hi if hi is not None else len(a)
    pos = bisect_left(a,x,lo,hi)
    return (pos if pos != hi and a[pos] == x else -1)

SIRKA = 800
VYSKA = 600


def randomIntDist(mi, ma, dist):
    random.randInt(random.random()*dist[-1])
    # TODO dorobit


class Ryba(Vec):
    def nastav(self):
        self.miestoHore = 0
        self.miestoDole = 30
        self.miestoVlavo = 0
        self.miestoVpravo = 70
        self.sytost = 100
        self.x = SIRKA/2
        self.y = VYSKA/2

    def nakresli(self, kreslic):
        kreslic.farba = Farba.MODRA
        kreslic.elipsa((0, 0), 60, 30)
        kreslic.mnohouholnik([(70,0), (70,30), (52,15)])

    def krok(self):
        if random.randint(1, 10) == 1 and self.sytost > 0:
            self.sytost -= 1
        if self.sytost < 1:
            pass
        if self.sytost > 0:
            if self.svet.stlacene[pygame.K_UP]:
                self.y -= 5
                if random.randint(1, 5) == 1: self.sytost -= 1
            if self.svet.stlacene[pygame.K_DOWN]:
                self.y += 5
                if random.randint(1, 5) == 1: self.sytost -= 1
            if self.svet.stlacene[pygame.K_RIGHT]:
                self.x += 5
                if random.randint(1, 5) == 1: self.sytost -= 1
            if self.svet.stlacene[pygame.K_LEFT]:
                self.x -= 5
                if random.randint(1, 5) == 1: self.sytost -= 1
        else:
            if random.randint(1,5):
                self.y += 0.7 * math.sin(self.svet.cas/1000.)
                self.x += 0.3

class Zralok(Vec):
    def nastav(self):
        self.miestoHore = 0
        self.miestoDole = 50
        self.miestoVlavo = 0
        self.miestoVpravo = 140
        self.zivot = 1000
        self.x = SIRKA
        self.y = r.y

    def nakresli(self, kreslic):
        kreslic.farba = Farba.CIERNA.zmixuj(Farba.BIELA).zmixuj(Farba.CIERNA)
        kreslic.elipsa((0, 0), 120, 50)
        kreslic.mnohouholnik([(140, 0), (140, 50), (100, 25)])

    def krok(self):
        self.x -= 2
        if self.y > r.y + r.miestoVpravo + self.miestoVlavo:
            self.y -= (self.y - r.y)/VYSKA*5.
        if self.x + self.miestoVlavo + self.miestoVpravo < 0:
            self.x = SIRKA+100

    @priZrazke(Ryba)
    def zjedene(self, r):
        r.sytost = 0
        r.znic()

class Papanica(Vec):
    def nastav(self):
        self.miestoHore = self.miestoDole = self.miestoVpravo = self.miestoVlavo = 5
        self.rychlost = random.randint(1, 5)
        self.vyzivnost = self.rychlost*10
        self.x = (r.x + (1+self.rychlost)*random.randint(-10, 10) + (random.randint(0, 2)*2-1)*(r.miestoVlavo + r.miestoVpravo)**1.2/(max(r.y, 1)*2)**0.2) % SIRKA
        self.y = 0
    def nakresli(self, kreslic):
        kreslic.farba = Farba(100 + self.vyzivnost*3, 50, 0)
        kreslic.elipsa((0, 0), 10, 10)
    def krok(self):
        if self.y + self.miestoHore > VYSKA:
            self.znic()
            self.svet.nastalaUdalost("STVOR PAPANICU")
        self.y += self.rychlost

    @priZrazke(Ryba)
    def zjedene(self, r):
        if r.sytost < 1: return
        r.sytost += self.vyzivnost
        self.znic()
        self.svet.nastalaUdalost("STVOR PAPANICU")

    @priZrazke(Zralok)
    def zjedeneZralokom(self, z):
        self.znic()
        self.svet.nastalaUdalost("STVOR PAPANICU")

class Hra(Svet):
    def nastav(self):
        global r, body, z, zradlo
        r = Ryba(self)
        z = Zralok(self)
        zradlo = Papanica(self)

        self.body = Text(self)
        self.body.zarovnajX = 1.0
        self.body.zarovnajY = 0.0
        self.body.x = SIRKA - 5
        self.body.y = 5
        self.body.aktualizuj(velkost=18)

    def kresli(self, kreslic):
        kreslic.farba = Farba(0,0,100)
        kreslic.obdlznik((0, 0), SIRKA, VYSKA)

    def krok(self):
        self.body.aktualizuj(text="Sytost: "+ str(r.sytost))

    @priUdalosti("STVOR PAPANICU")
    def stvorPapanicu(self):
        zradlo = Papanica(self)

okno.nazov = "Rybicka"
okno.sirka = SIRKA
okno.vyska = VYSKA
hra.fps = 60
hra.start(Hra())