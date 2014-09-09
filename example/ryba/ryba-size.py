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
        self.sytost_text = Text(self.svet)
        self.sytost_text.x = 0
        self.sytost_text.y = 0
        self.sytost_text.zarovnajX = 0
        self.sytost_text.zarovnajY = 0
        self.sytost_text.aktualizuj(velkost=30,farba = Farba(0,0,0))

    def krok(self):
        self.sytost_text.aktualizuj(text = "Sytost: " + str(self.svet.rybka.sytost))

class Zralok(Vec):
    def nastav(self):
        self.x = okno.sirka+50
        self.y = okno.vyska/2
        self.miestoHore = 15
        self.miestoDole = 15
        self.miestoVpravo = 35
        self.miestoVlavo = 25
        self.velkost = 1.5

    def nakresli(self,kreslic):
        self.miestoHore = int(15*self.velkost)
        self.miestoDole = int(15*self.velkost)
        self.miestoVpravo = int(35*self.velkost)
        self.miestoVlavo = int(25*self.velkost)
        kreslic.farba = Farba(0,0,0)
        kreslic.elipsa((int(-25*self.velkost), int(-15*self.velkost)), int(50*self.velkost), int(30*self.velkost))
        kreslic.mnohouholnik([(int(35*self.velkost),int(-18*self.velkost)),(int(35*self.velkost),int(18*self.velkost)),(int(15*self.velkost),0)])
        kreslic.mnohouholnik([(int(10*self.velkost),int(-25*self.velkost)),(int(10*self.velkost),0),(int(-15*self.velkost),0)])
        kreslic.farba = Farba(128,128,128)
        kreslic.elipsa((int(-19*self.velkost), int(-6*self.velkost)), int(7*self.velkost), int(7*self.velkost))
        kreslic.farba = Farba(200,0,0)
        kreslic.elipsa((int(-22*self.velkost), int(5*self.velkost)), int(10*self.velkost), int(6*self.velkost))

    def krok(self):
        self.x -= 3
        if self.x > self.svet.rybka.x-50:
            if self.svet.rybka.y <= self.y-2:
                self.y -=2
            elif self.svet.rybka.y >= self.y+2:
                self.y +=2

        if self.x < -50:
            self.x = okno.sirka+50

        self.velkost = 1.5 + (self.svet.cas / 1000000.0)

class Ryba(Vec):
    def nastav(self):
        self.sytost = 500
        self.x = okno.sirka/2
        self.y = okno.vyska/2
        self.miestoVpravo = 25
        self.miestoVlavo = 35
        self.poslednySmer = 1
        self.velkost = 1.0
        self.ziva = 1

    def nakresli(self,kreslic):
        self.miestoHore = int(15*self.velkost)
        self.miestoDole = int(15*self.velkost)

        if self.ziva ==1:
            if self.poslednySmer == 1:
                self.miestoVpravo = int(25*self.velkost)
                self.miestoVlavo = int(35*self.velkost)
                kreslic.farba = Farba(256,200,0)
                kreslic.elipsa((int(-25*self.velkost), int(-15*self.velkost)), int(50*self.velkost), int(30*self.velkost))
                kreslic.mnohouholnik([(int(-35*self.velkost),int(-18*self.velkost)),(int(-35*self.velkost),int(18*self.velkost)),(int(-15*self.velkost),0)])
                kreslic.mnohouholnik([(int(-10*self.velkost),int(-25*self.velkost)),(int(-10*self.velkost),0),(int(15*self.velkost),0)])
                kreslic.farba = Farba(0,0,0)
                kreslic.elipsa((int(12*self.velkost), int(-6*self.velkost)), int(7*self.velkost), int(7*self.velkost))
                kreslic.farba = Farba(200,0,0)
                kreslic.elipsa((int(12*self.velkost), int(5*self.velkost)), int(10*self.velkost), int(6*self.velkost))
            else:
                self.miestoVpravo = int(35*self.velkost)
                self.miestoVlavo = int(25*self.velkost)
                kreslic.farba = Farba(256,200,0)
                kreslic.elipsa((int(-25*self.velkost), int(-15*self.velkost)), int(50*self.velkost), int(30*self.velkost))
                kreslic.mnohouholnik([(int(35*self.velkost),int(-18*self.velkost)),(int(35*self.velkost),int(18*self.velkost)),(int(15*self.velkost),0)])
                kreslic.mnohouholnik([(int(10*self.velkost),int(-25*self.velkost)),(int(10*self.velkost),0),(int(-15*self.velkost),0)])
                kreslic.farba = Farba(0,0,0)
                kreslic.elipsa((int(-19*self.velkost), int(-6*self.velkost)), int(7*self.velkost), int(7*self.velkost))
                kreslic.farba = Farba(200,0,0)
                kreslic.elipsa((int(-22*self.velkost), int(5*self.velkost)), int(10*self.velkost), int(6*self.velkost))
        else:
            self.miestoVpravo = int(25*self.velkost)
            self.miestoVlavo = int(35*self.velkost)
            kreslic.farba = Farba(50,255,100)
            kreslic.elipsa((int(-25*self.velkost), int(-15*self.velkost)), int(50*self.velkost), int(30*self.velkost))
            kreslic.mnohouholnik([(int(-35*self.velkost),int(-18*self.velkost)),(int(-35*self.velkost),int(18*self.velkost)),(int(-15*self.velkost),0)])
            kreslic.mnohouholnik([(int(-10*self.velkost),int(25*self.velkost)),(int(-10*self.velkost),0),(int(15*self.velkost),0)])
            kreslic.farba = Farba(0,0,0)
            #kreslic.elipsa((int(12*self.velkost), int(-1*self.velkost)), int(7*self.velkost), int(7*self.velkost))
            kreslic.ciara((int(12*self.velkost), int(-1*self.velkost)), (int(19*self.velkost), int(6*self.velkost)),3)
            kreslic.ciara((int(19*self.velkost), int(-1*self.velkost)), (int(12*self.velkost), int(6*self.velkost)),3)
            kreslic.farba = Farba(128,128,128)
            kreslic.elipsa((int(12*self.velkost), int(-10*self.velkost)), int(10*self.velkost), int(6*self.velkost))

    def krok(self):
        if self.ziva==1:
            self.sytost -=1
            self.velkost = (float(self.sytost)/float(500))**(0.3)
            if(self.svet.stlacene[pygame.K_UP]):
                if self.y - self.miestoHore >= 0:
                    self.y -= 4
            if(self.svet.stlacene[pygame.K_DOWN]):
                if self.y + self.miestoDole <= okno.vyska:
                    self.y += 4
            if(self.svet.stlacene[pygame.K_LEFT]):
                if self.x - self.miestoVlavo >= 0:
                    self.x -= 4
                self.poslednySmer = -1
            if(self.svet.stlacene[pygame.K_RIGHT]):
                if self.x + self.miestoVpravo <= okno.sirka:
                    self.x += 4
                self.poslednySmer = 1

            self.svet.rybka.x = self.x
            self.svet.rybka.y = self.y

            if self.sytost <= 0:
                self.znic()

    @priZrazke(Zralok)
    def somMoznoZozrana(self,zralok):
        if self.ziva == 1:
            print self.velkost
            print zralok.velkost

        if self.velkost <= zralok.velkost:
            #self.znic()
            self.ziva = 0
        else:
            zralok.znic()

class Jedlo(Obrazok):
    def nastav(self):
        self.nastavSubor("jedlo.png")
        self.x = random.randrange(okno.sirka)
        self.y = -5
        self.miestoHore = 12
        self.miestoDole = 12
        self.miestoVpravo = 12
        self.miestoVlavo = 12

    def krok(self):
        self.y += 1
        if self.y > okno.vyska:
           self.znic()

    @priZrazke(Ryba)
    def zjedene(self,rybka):
        if rybka.ziva == 1:
            rybka.sytost +=100
            self.znic()


class Akvarium(Svet):

    def nastav(self):
        okno.nazov="Moje male akvarko"
        self.rybka = Ryba(self)
        Jedlo(self)
        self.zralocik = Zralok(self)
        self.moj_panel = Info_panel(self)
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
