import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', '..', 'src')))

from gaminator import *

okno.sirka = 600
okno.vyska = 400
okno.pevne()


class Ryba(Vec):
	
	def nastav(self):
		self.x = okno.sirka/2
		self.y = okno.vyska/2
		#self.miestoHore =
	
	def nakresli(self, kreslic):
		#kreslic.farba = Farba(30,200,30)
		#kreslic.elipsa( [-25,-15], 50, 30 )
		kreslic.farba = Farba(256,200,0)
		kreslic.elipsa([-15, -15], 40, 30)
		kreslic.mnohouholnik( [[-25, 14], [-25, -14], [0,0] ])

class Hra(Svet):

	def nastav(self):
		self.ryba = Ryba(self)

	def nakresli(self, kreslic):
		kreslic.farba = Farba(0,35,150)
		kreslic.obdlznik( [0,0] , okno.sirka,okno.vyska )




hra.fps = 60
hra.start(Hra())
