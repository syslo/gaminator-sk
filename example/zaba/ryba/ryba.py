import sys
import os
sys.path.append(os.path.abspath(os.path.join('..','..','..', 'src')))

from gaminator import *
import random

okno.sirka = 600
okno.vyska = 400
okno.pevne()

class InfoText(Vec):
    def nastav(self):
        self.text = Text(self.svet)
        self.text.x = 0
        self.text.y = 0
        self.text.zarovnajX = 0
        self.text.zarovnajY = 0
        self.text.aktualizuj(velkost = 30)

    def krok(self):
        self.text.aktualizuj(text = "Sytost: " + str(self.svet.ryba.sytost))

class Zralok(Vec):
    def nastav(self):
        self.y = okno.vyska/2
        self.x = 0
        self.miestoHore = 0
        self.miestoDole = 30
        self.miestoVpravo = 30
        self.miestoVlavo = 0

    def krok(self):
        self.x += 3
        if(self.x > okno.sirka):
            self.x = 0
        if(self.y < self.svet.ryba.y and self.svet.ryba.y - self.y >=3):
            self.y += 3
        elif(self.y > self.svet.ryba.y and self.y - self.svet.ryba.y >=3):
            self.y -= 3

    def nakresli(self,kreslic):
        kreslic.farba = Farba.CERVENA
        kreslic.elipsa((0,0),30,30)

class Ryba(Vec):
    def nastav(self):
        self.sytost = 500
        self.x = okno.sirka/2
        self.y = okno.vyska/2
        self.miestoHore = 0
        self.miestoDole = 20
        self.miestoVpravo = 20
        self.miestoVlavo = 0

    def krok(self):
        self.sytost -= 2
        if(self.svet.stlacene[pygame.K_UP]):
            self.y -= 5
        if(self.svet.stlacene[pygame.K_DOWN]):
            self.y += 5
        if(self.svet.stlacene[pygame.K_LEFT]):
            self.x -= 5
        if(self.svet.stlacene[pygame.K_RIGHT]):
            self.x += 5
        if(self.x < 0):
            self.x = 0
        elif(self.x > okno.sirka - 20):
            self.x = okno.sirka - 20
        if(self.y < 0):
            self.y = 0
        elif(self.y > okno.vyska - 20):
            self.y = okno.vyska - 20
        if(self.sytost < 0):
            self.znic()

    @priZrazke(Zralok)
    def somZjedena(self,zralok):
        self.znic()

    def nakresli(self,kreslic):
        kreslic.farba = Farba.CIERNA
        kreslic.elipsa((0,0),20,20)

class Jedlo(Vec):
    def nastav(self):
        self.y = -5
        self.x = random.randrange(okno.sirka)
        self.miestoHore = 0
        self.miestoDole = 10
        self.miestoVlavo = 0
        self.miestoVpravo = 10

    def krok(self):
        self.y += 2
        if(self.y > okno.vyska + 20):
            self.znic()

    @priZrazke(Ryba)
    def somZjedena(self,ryba):
        ryba.sytost += 100
        self.znic()

    def nakresli(self,kreslic):
        kreslic.farba = Farba.ZELENA
        kreslic.elipsa((0,0),10,10)

class Akvarium(Svet):
    okno.nazov = "Zabka kodi hru"

    @priUdalosti("Jedlo")
    def generujJedlo(self):
        Jedlo(self)
        self.nacasujUdalost(1000,"Jedlo")

    def nastav(self):
        self.zralok = Zralok(self)
        self.ryba = Ryba(self)
        self.generujJedlo()
        self.text_sytost = InfoText(self)

    def krok(self):
        if(self.stlacene[pygame.K_ESCAPE]):
            hra.koniec()

    def nakresli(self,kreslic):
        kreslic.farba = Farba(120,120,255)
        kreslic.obdlznik((0,0),okno.sirka,okno.vyska)
        kreslic.farba = Farba(150,150,0)
        kreslic.obdlznik((0,okno.vyska-15),okno.sirka,15)
        kreslic.farba = Farba(200,200,200)
        kreslic.elipsa((100,100),30,30,3)
        kreslic.elipsa((115,135),20,20,2)
        kreslic.elipsa((105,157),10,10,1)
        kreslic.farba = Farba(25,25,0)
        kreslic.obdlznik((300,okno.vyska-80),100,65)
        kreslic.elipsa((300,okno.vyska-95),100,30)
        kreslic.farba = Farba.ZLTA
        kreslic.ciara((300,okno.vyska-75),(400,okno.vyska-75),8)

hra.fps = 40
hra.start(Akvarium())