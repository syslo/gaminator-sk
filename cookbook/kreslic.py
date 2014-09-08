import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'src')))

from gaminator import *

okno.sirka = 600
okno.vyska = 400
okno.pevne()

class Akvarium(Svet):
    okno.nazov = "Ukazka kreslenia"

    def nakresli(self,kreslic):
        kreslic.farba = Farba.CERVENA
        kreslic.obdlznik((0,0),200,80,5)
        kreslic.farba = Farba(0,255,0)
        kreslic.elipsa((300,200),100,100)
        kreslic.farba = Farba.MODRA
        kreslic.ciara((500,300),(okno.sirka,okno.vyska),5)
        kreslic.mnohouholnik([(0,100),(100,100),(50,200)])

hra.fps = 40
hra.start(Akvarium())