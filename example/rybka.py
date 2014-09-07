import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'src')))

from gaminator import *

SIRKA = 600
VYSKA = 400

class Ryba(Vec):
	def nastav(self):
		self.x = SIRKA/2
		self.y = VYSKA/2
		self.hlad = 0
		self.miesto_dole = 15
		self.miesto_hore = 15
		self.miesto_vpravo = 30 
		self.miesto_vlavo = 40

	def nakresli(self,kreslic):
		kreslic.farba = Farba.ZELENA
		kreslic.elipsa( (-30,-15), 60, 30)
		kreslic.mnohouholnik( [(-20,0), (-40,-13), (-40, 13)] )
		kreslic.farba = Farba.CIERNA
		kreslic.elipsa( (20,-8), 5, 5)

	def krok(self):
		self.hlad = self.hlad + 1
		okno.nazov = "Hlad: " + str(self.hlad)

class Jedlo(Vec):
	def nastav(self):
		self.r = 10
		self.x = SIRKA/2
		self.y = -2*self.r
		self.miesto_vlavo = self.miesto_vpravo = self.miesto_hore = self.miesto_dole = self.r

	def nakresli(self,kreslic):
		kreslic.farba = Farba.ZLTA
		kreslic.elipsa( (-self.r,-self.r), 2*self.r, 2*self.r)

	def krok(self):
		self.y = self.y + 2

	@priZrazke(Ryba)
	def zjedene(self, ryba):
		ryba.hlad -= 100
		self.svet.nastalaUdalost("GENERUJ JEDLO")
		self.znic()

class Zralok(Vec):
	def nastav(self):
		self.x = 0
		self.y = VYSKA/2
		self.miesto_dole = 25
		self.miesto_hore = 25
		self.miesto_vpravo = 70 
		self.miesto_vlavo = 90

	def nakresli(self, kreslic):
		kreslic.farba = Farba.CIERNA.zmixuj(Farba.BIELA)
		kreslic.elipsa( (-70,-25), 140, 50)
		kreslic.mnohouholnik( [(-60,5), (-90,5), (-90,-40)])
		kreslic.mnohouholnik( [(-10,-10), (-10,-60), (30 , 0 )])
		kreslic.farba = Farba.CIERNA
		kreslic.elipsa( (45,-15), 10,10)

	def krok(self):
		self.x = self.x + 1

	@priZrazke(Ryba)
	def zjem(self,ryba):
		ryba.znic()

class Hra(Svet):
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

	def nastav(self):
		ryba = Ryba(self)
		zralok = Zralok(self)
		jedlo = Jedlo(self)


	@priUdalosti("GENERUJ JEDLO")
	def vytvor_jedlo(self):
		Jedlo(self)

okno.vyska = VYSKA
okno.sirka = SIRKA
hra.fps = 60
hra.start(Hra())

