import sys
import os
sys.path.append(os.path.abspath(os.path.join('..','..', 'src')))

from gaminator import *

SIRKA = okno.sirka = 600
VYSKA = okno.vyska = 400
okno.pevne()

class Info_panel(Vec):
    def nastav(self):
        self.sytost_text = Text(self.svet)
        self.sytost_text.x = 0
        self.sytost_text.y = 0
        self.sytost_text.zarovnajX = 0
        self.sytost_text.zarovnajY = 0
        self.sytost_text.aktualizuj(velkost=30,farba = Farba(255,255,255))

    def krok(self):
        self.sytost_text.aktualizuj(text = "Sytost: " + str(self.svet.rybka.sytost))


class Jedlo(Vec):
    def nastav(self):
        pass

    def krok(self):
        pass

    def nakresli(self,kreslic):
        pass


class Ryba(Vec):
    def nastav(self):
        self.sytost = 500
        pass

    def krok(self):
        pass

    @priZrazke(Jedlo)
    def zjemJedlo(self,jedlo):
        pass

    def nakresli(self,kreslic):
        pass


class Zralok(Vec):
    def nastav(self):
        pass

    def krok(self):
        pass

    @priZrazke(Ryba)
    def zjemRybu(self,ryba):
        pass

    def nakresli(self,kreslic):
        pass


class Akvarium(Svet):

    def vytvorJedlo(self):
        Jedlo(self)

    def nastav(self):
        okno.nazov="Moje akvarium"
        self.rybka = Ryba(self)
        self.vytvorJedlo()
        self.zralok = Zralok(self)
        self.panel = Info_panel(self)

    def nakresli(self,kreslic):
        #voda
        kreslic.farba = Farba.MODRA*0.4 + Farba.BIELA*0.6
        kreslic.obdlznik( (0,0), SIRKA,VYSKA)					#ako budeme vysvetlovat pozicie?
        kreslic.farba = Farba.BIELA
        kreslic.obdlznik( (0,0), SIRKA, 10)
        for i in range(10):
            kreslic.elipsa( (i*60,-20), 60,60)
        #zem
        kreslic.farba = Farba(180, 160, 0)
        kreslic.obdlznik( (0,VYSKA-10), SIRKA, 10 )

        #potapac
        kreslic.farba = Farba.CIERNA
        kreslic.elipsa( (100,100), 75, 25 )
        kreslic.elipsa( (175,100), 25, 25 )
        kreslic.ciara(  (158,120), (170, 132) , 3 )
        kreslic.ciara(  (158,120), (160, 140) , 3 )
        kreslic.ciara(  (190,136), (170, 132) , 3 )
        kreslic.ciara(  (178,144), (160, 140) , 3 )

        kreslic.ciara(  (100,112), (67, 101)  , 4 )
        kreslic.ciara(  (100,112), (67, 121)  , 4 )
        kreslic.ciara(  (45 ,79) , (67, 101)  , 4 )
        kreslic.ciara(  (42 ,106), (67, 121)  , 4 )

        kreslic.farba = Farba.ZLTA
        kreslic.obdlznik( (120,90), 40, 12)
        kreslic.elipsa( (160-6,90),12,12)

        #bublinky
        kreslic.farba = Farba.MODRA*0.3 + Farba.BIELA*0.7
        kreslic.elipsa( (300,200), 30, 30, 4)
        kreslic.elipsa( (330,230), 30, 30, 4)
        kreslic.elipsa( (290,270), 30, 30, 4)
        kreslic.elipsa( (195,60 ), 20, 20, 3)

        #truhlica
        kreslic.farba = Farba(100, 50, 0)
        kreslic.obdlznik( (290, VYSKA-50), 80, 40)
        kreslic.elipsa( (290,VYSKA-70), 80, 40)
        kreslic.farba = Farba.ZLTA
        kreslic.ciara( (290, VYSKA-50), (370,VYSKA-50), 2)

        #hviezdica
        from math import sin, cos, pi
        bodyx = [ 500 + (10 + 20*(x%2))*cos(x * 2*pi/10) for x in range(10) ]
        bodyy = [ 300 + (10 + 20*(x%2))*sin(x * 2*pi/10) for x in range(10)]
        kreslic.farba = Farba(255, 150, 0)
        kreslic.mnohouholnik(zip(bodyx,bodyy))

        #korytnacka
        kreslic.farba = Farba(128,128,0)
        kreslic.elipsa([415,85],20,30)
        kreslic.elipsa([386,110],30,18)
        kreslic.elipsa([434,110],30,18)
        kreslic.elipsa([390,135],30,18)
        kreslic.elipsa([430,135],30,18)
        kreslic.elipsa([420,135],10,30)
        kreslic.farba = Farba(128,220,0)
        kreslic.elipsa([400,100],50,60)
        kreslic.farba = Farba(0,0,0)
        kreslic.elipsa([420,90],5,5)
        kreslic.elipsa([426,90],5,5)

        #slimacik
        kreslic.farba = Farba(220,160,0)
        kreslic.elipsa([88,347],45,45)
        kreslic.farba = Farba(175,128,0)
        kreslic.elipsa([70,375],65,18)
        kreslic.ciara([85,390],[60,365],5)
        kreslic.ciara([85,390],[80,365],5)

        #musla
        kreslic.farba = Farba(255,255,200)
        kreslic.elipsa([180,250],50,30)
        kreslic.mnohouholnik(([180,265],[230,265],[205,290]))
        kreslic.mnohouholnik(([195,290],[215,290],[205,275]))
        kreslic.farba = Farba(255,255,50)
        kreslic.ciara([205,250],[205,280],3)
        kreslic.ciara([180,265],[200,280],3)
        kreslic.ciara([230,265],[210,280],3)
        kreslic.ciara([192,257],[203,280],3)
        kreslic.ciara([217,257],[207,280],3)

    def krok(self):
        if(self.stlacene[pygame.K_ESCAPE]):
            hra.koniec()

hra.fps = 50
hra.start(Akvarium())
