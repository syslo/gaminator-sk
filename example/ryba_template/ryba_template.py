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
        pass

    def nakresli(self,kreslic):
        pass

    def krok(self):
        pass

class Ryba(Vec):
    def nastav(self):
        self.sytost = 500
        pass

    def nakresli(self,kreslic):
        pass

    def krok(self):
        pass


class Jedlo(Obrazok):
    def nastav(self):
        pass

    def nakresli(self,kreslic):
        pass

    def krok(self):
        pass


class Akvarium(Svet):
    okno.nazov="Moje akvarium"

    def vytvorJedlo(self):
        Jedlo(self)

    def nastav(self):
        self.rybka = Ryba(self)
        self.vytvorJedlo()
        self.zralok = Zralok(self)
        self.panel = Info_panel(self)

    def nakresli(self,kreslic):
        pass

    def krok(self):
        pass

hra.fps = 50
hra.start(Akvarium())
