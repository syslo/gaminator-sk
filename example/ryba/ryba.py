import sys
import os
sys.path.append(os.path.abspath(os.path.join('..','..', 'src')))

from gaminator import *
import random

okno.sirka = 600
okno.vyska = 400
okno.pevne()


class Info_panel(Vec):
    def nastav(self):
        self.najedenost_text = Text(self.svet)
        self.najedenost_text.x = 0
        self.najedenost_text.y = 0
        self.najedenost_text.zarovnajX = 0
        self.najedenost_text.zarovnajY = 0
        self.najedenost_text.aktualizuj(velkost=30,farba = Farba(255,255,255))

    def krok(self):
        self.najedenost_text.aktualizuj(text = "Najedenost: " + str(self.svet.najedenost))

class Zralok(Vec):
    def nastav(self):
        self.x = okno.sirka+50
        self.y = okno.vyska/2
        self.miesto_hore = 15
        self.miesto_dole = 15
        self.miesto_vpravo = 35
        self.miesto_vlavo = 25

    def nakresli(self,kreslic):
        kreslic.farba = Farba(0,0,0)
        kreslic.elipsa((-25, -15), 50, 30)
        kreslic.mnohouholnik([(35,-18),(35,18),(15,0)])
        kreslic.mnohouholnik([(10,-25),(10,0),(-15,0)])
        kreslic.farba = Farba(128,128,128)
        kreslic.elipsa((-19, -6), 7, 7)
        kreslic.farba = Farba(200,0,0)
        kreslic.elipsa((-22, 5), 10, 6)

    def krok(self):
        self.x -= 3
        if self.x > self.svet.rybka.x-50:
            if self.svet.rybka.y <= self.y-2:
                self.y -=2
            elif self.svet.rybka.y >= self.y+2:
                self.y +=2

        if self.x < -50:
            self.x = okno.sirka+50

class Ryba(Vec):
    def nastav(self):
        self.x = okno.sirka/2
        self.y = okno.vyska/2
        self.miesto_hore = 15
        self.miesto_dole = 15
        self.miesto_vpravo = 25
        self.miesto_vlavo = 35
        self.svet.najedenost = 500
        self.poslednySmer = 1

    def nakresli(self,kreslic):
        if self.poslednySmer == 1:
            self.miesto_vpravo = 25
            self.miesto_vlavo = 35
            kreslic.farba = Farba(256,200,0)
            kreslic.elipsa((-25, -15), 50, 30)
            kreslic.mnohouholnik([(-35,-18),(-35,18),(-15,0)])
            kreslic.mnohouholnik([(-10,-25),(-10,0),(15,0)])
            kreslic.farba = Farba(0,0,0)
            kreslic.elipsa((12, -6), 7, 7)
            kreslic.farba = Farba(200,0,0)
            kreslic.elipsa((12, 5), 10, 6)
        else:
            self.miesto_vpravo = 35
            self.miesto_vlavo = 25
            kreslic.farba = Farba(256,200,0)
            kreslic.elipsa((-25, -15), 50, 30)
            kreslic.mnohouholnik([(35,-18),(35,18),(15,0)])
            kreslic.mnohouholnik([(10,-25),(10,0),(-15,0)])
            kreslic.farba = Farba(0,0,0)
            kreslic.elipsa((-19, -6), 7, 7)
            kreslic.farba = Farba(200,0,0)
            kreslic.elipsa((-22, 5), 10, 6)

    def krok(self):
        self.svet.najedenost -=1
        if(self.svet.stlacene[pygame.K_UP]):
            if self.y - self.miesto_hore >= 0:
                self.y -= 4
        if(self.svet.stlacene[pygame.K_DOWN]):
            if self.y + self.miesto_dole <= okno.vyska:
                self.y += 4
        if(self.svet.stlacene[pygame.K_LEFT]):
            if self.x - self.miesto_vlavo >= 0:
                self.x -= 4
            self.poslednySmer = -1
        if(self.svet.stlacene[pygame.K_RIGHT]):
            if self.x + self.miesto_vpravo <= okno.sirka:
                self.x += 4
            self.poslednySmer = 1

        self.svet.rybka.x = self.x
        self.svet.rybka.y = self.y

        if self.svet.najedenost <= 0:
            self.znic()

    @priZrazke(Zralok)
    def somZozrana(self,zralok):
        self.znic()

class Jedlo(Obrazok):
    def nastav(self):
        self.nastavSubor("jedlo.png")
        self.x = random.randrange(okno.sirka)
        self.y = -5
        self.miesto_hore = 12
        self.miesto_dole = 12
        self.miesto_vpravo = 12
        self.miesto_vlavo = 12

    def krok(self):
        self.y += 1
        if self.y > okno.vyska:
           self.znic()

    @priZrazke(Ryba)
    def zjedene(self,rybka):
        self.svet.najedenost +=100
        self.znic()


class Akvarium(Svet):
    okno.nazov="Moje male akvarko"

    def nastav(self):
        self.moj_panel = Info_panel(self)
        self.rybka = Ryba(self)
        Jedlo(self)
        self.zralocik = Zralok(self)
        self.nacasujUdalost(1000,"NoveJedlo")

    @priUdalosti("NoveJedlo")
    def generujJedlo(self):
        Jedlo(self)
        self.nacasujUdalost(1000,"NoveJedlo")

    def nakresli(self,kreslic):
        #pozadie
        kreslic.farba = Farba(0,64,128)
        kreslic.obdlznik([0,0],okno.sirka,okno.vyska)

        #truhlica
        kreslic.farba = Farba(256,128,0)
        kreslic.elipsa([100,250],70,70)
        kreslic.obdlznik([100,285],70,50)
        kreslic.farba = Farba(0,64,128)
        kreslic.obdlznik([100,285],65,5)

        #bublinky
        kreslic.farba = Farba(0,128,256)
        kreslic.elipsa([50,120],40,40)
        kreslic.elipsa([70,170],30,30)
        kreslic.elipsa([60,210],25,25)
        kreslic.elipsa([80,240],20,20)
        kreslic.elipsa([100,210],15,15)
        kreslic.elipsa([100,140],25,25)

        #riasy
        kreslic.farba = Farba(0,200,0)
        kreslic.ciara([250,350],[260,330],8)
        kreslic.ciara([260,330],[250,310],8)
        kreslic.ciara([250,310],[260,290],8)

        kreslic.ciara([250+20,350],[260+20,330],8)
        kreslic.ciara([260+20,330],[250+20,310],8)
        kreslic.ciara([250+20,310],[260+20,290],8)

        kreslic.ciara([250+40,350],[260+40,330],8)
        kreslic.ciara([260+40,330],[250+40,310],8)
        kreslic.ciara([250+40,310],[260+40,290],8)

        #hviezda
        kreslic.farba = Farba(125,75,0)
        kreslic.mnohouholnik([[10+420,40+250],[40+420,40+250],[50+420,10+250],[60+420,40+250],[90+420,40+250],[65+420,60+250],[75+420,90+250],[50+420,70+250],[25+420,90+250],[35+420,60+250]])
        kreslic.farba = Farba(255,0,0)
        kreslic.elipsa([460,295],20,20)
        kreslic.farba = Farba(125,75,0)
        kreslic.mnohouholnik(([460,295],[480,295],[480,305],[460,305]))
        kreslic.farba = Farba(0,0,0)
        kreslic.elipsa([460,295],10,10)
        kreslic.elipsa([470,295],10,10)

    def krok(self):
        if(self.svet.stlacene[pygame.K_ESCAPE]):
            hra.koniec()
        if(self.svet.stlacene[pygame.K_f]):
            okno.celaObrazovka()
        if(self.svet.stlacene[pygame.K_w]):
            okno.pevne()

        #if(self.svet.stlacene[pygame.K_SPACE]):
        #    hra.koniec()





hra.fps = 50
hra.start(Akvarium())
