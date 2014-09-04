import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'src')))

from gaminator import *
import random

SIRKA = 800
VYSKA = 600

class Papkac(Vec):

    def nastav(self):
        self.miesto_hore = 20
        self.miesto_dole = 20
        self.miesto_vpravo = 20
        self.miesto_vlavo = 20
        self.body = 0
        self.zivoty = 10
        self.x = SIRKA/2
        self.y = VYSKA/2

    def nakresli(self, kreslic):
        kreslic.farba = Farba.ZLTA
        kreslic.elipsa((-20, -20), 41, 41)
        kreslic.farba = Farba.BIELA
        kreslic.elipsa((-15, -15), 15, 15)
        kreslic.elipsa((1, -15), 15, 15)
        kreslic.farba = Farba.CERVENA.zmixuj(Farba.BIELA)
        kreslic.elipsa((-10, 3), 21, 10)

    def krok(self):
        if self.svet.stlacene[pygame.K_UP]:
            self.y -= 5
        if self.svet.stlacene[pygame.K_DOWN]:
            self.y += 5
        if self.svet.stlacene[pygame.K_RIGHT]:
            self.x += 5
        if self.svet.stlacene[pygame.K_LEFT]:
            self.x -= 5

    def vyvoj(self):
        novy = Superpapkac(self.svet)
        novy.x = self.x
        novy.y = self.y
        novy.body = self.body
        novy.zivoty = self.zivoty + 1
        self.svet.papkac = novy
        self.znic()


class Superpapkac(Obrazok, Papkac):

    def nastav(self):
        self.nastavSubor("superpapkac.png")


class Jedlo(Vec):

    def nastav(self):
        self.miesto_hore = 10
        self.miesto_dole = 10
        self.miesto_vpravo = 10
        self.miesto_vlavo = 10
        self.x = -10
        self.y = random.randint(20, VYSKA-20)
        self.rychlost = random.randint(1, 7)
        self.farba = None
        self.dobre = True

    def krok(self):
        self.x += self.rychlost
        if self.x > SIRKA+10:
            self.x = -10

    def nakresli(self, kreslic):
        kreslic.farba = self.farba
        kreslic.elipsa((-10, -10), 21, 21, 3)

    @priZrazke(Papkac)
    def zjedene(self, papkac):
        if self.dobre:
            papkac.body += 1
            if papkac.body % 20 == 0:
                papkac.vyvoj()
        else:
            papkac.zivoty -= 1
            if papkac.zivoty == 0:
                papkac.znic()
        self.zomri()

    @priUdalosti("Instant kill")
    def zomri(self):
        if self.dobre:
            self.svet.nacasujUdalost(1000, "Vytvor dobre jedlo")
        else:
            self.svet.nacasujUdalost(5000, "Vytvor zle jedlo")
        self.znic()

class Hra(Svet):

    def nastav(self):

        self.body = Text(self)
        self.body.zarovanajX = 1.0  # zarovnaj vlavo
        self.body.zarovanajY = 0.0  # zarovnaj hore
        self.body.x = SIRKA - 5
        self.body.y = 5
        self.body.aktualizuj(velkost=50)

        self.zivoty = Text(self)
        self.zivoty.zarovanajX = 0.0  # zarovnaj vpravo
        self.zivoty.zarovanajY = 0.0  # zarovnaj hore
        self.zivoty.x = 5
        self.zivoty.y = 5
        self.zivoty.aktualizuj(velkost=50)

        self.papkac = Papkac(self)
        for i in range(5):
            self.nacasujUdalost(1000*i, "Vytvor dobre jedlo")
        for i in range(5):
            self.nacasujUdalost(1000*i, "Vytvor zle jedlo")

    def krok(self):

        self.body.aktualizuj(text=str(self.papkac.body)+" b")
        self.zivoty.aktualizuj(text="zivoty: "+str(self.papkac.zivoty))

        if self.stlacene[pygame.K_f]:
            okno.celaObrazovka()
        if self.stlacene[pygame.K_g]:
            okno.pevne()
        if self.stlacene[pygame.K_i]:
            self.nastalaUdalost("Instant kill")
        if self.stlacene[pygame.K_n]:
            hra.nahradSvet(Hra())


    @priUdalosti("Vytvor dobre jedlo")
    def noveDobreJedlo(self):
        jedlo = Jedlo(self)
        jedlo.farba = Farba.ZELENA
        jedlo.dobre = True

    @priUdalosti("Vytvor zle jedlo")
    def noveZleJedlo(self):
        jedlo = Jedlo(self)
        jedlo.farba = Farba.CERVENA
        jedlo.dobre = False

okno.nazov = "Papkac"
okno.sirka = SIRKA
okno.vyska = VYSKA
hra.fps = 60
hra.start(Hra())
