import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join('../..', 'src')))

from gaminator import *

rspd = 2
rfloat = 1

#okno.celaObrazovka() prilis nebezpecne, zatial zakomentovane

class Akvarium(Svet):
    def nastav(self):
        okno.nazov="Akvarium level 1"
        okno.vyska=480
        okno.sirka=640
        moja_rybka = Ryba(self)
        self.nacasujUdalost(1000,"Jedloooo")
        
    def nakresli(self,kreslic):
        kreslic.farba=Farba(173,216,230)
        kreslic.obdlznik((0,0),okno.sirka,okno.vyska,0)
        kreslic.farba=Farba(144,95,0)
        kreslic.obdlznik((0,okno.vyska-50),okno.sirka,50)
    def krok(self):
        if (self.stlacene[pygame.K_ESCAPE]):
            hra.koniec()
    @priUdalosti("Jedloooo")
    def davajJedlo(self):
        Jedlo(self)
        self.nacasujUdalost(100,"Jedloooo")
class Ryba(Vec):
    def nastav(self):
        self.x = okno.sirka/2
        self.y = okno.vyska/2
        self.miestoHore = 10
        self.miestoDole = 10
        self.miestoVpravo = 20
        self.miestoVlavo = 20
    def krok(self):
        if (self.svet.stlacene[pygame.K_LEFT]):
            self.x -= rspd
        if (self.svet.stlacene[pygame.K_RIGHT]):
            self.x += rspd
        if (self.svet.stlacene[pygame.K_UP]):
            self.y -= rspd
        else:
            self.y += rfloat
        if self.x > okno.sirka:
            self.x = okno.sirka
        if self.x < 0:
            self.x = 0
        if self.y > okno.vyska-60:
           self.y = okno.vyska-60
    def nakresli(self,kreslic):
        kreslic.farba = Farba(59,89,100)
        kreslic.elipsa((-20,-10),40,20)
class Jedlo(Vec):
    def nastav(self):
        self.x = random.randrange(okno.sirka)
        self.y = -20
        self.miestoDole = 10
        self.miestoHore = 10
        self.miestoVlavo = 10
        self.miestoVpravo = 10
    def nakresli(self,kreslic):
        kreslic.farba = Farba(0,255,0)
        kreslic.elipsa((-10,-10),20,20)
    def krok(self):
        self.y += 1
    @priZrazke(Ryba)
    def zahyn(self,rybka):
        self.znic()
        print "kolizia"
hra.start(Akvarium())