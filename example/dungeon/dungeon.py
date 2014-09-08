import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', '..', 'src')))

from gaminator import *

#velkost dlazdiciek
GRID = 30
#Pomocne polia pre navigaciu
DX = [-1,0,1,0]
DY = [0,-1,0,1]
KEY_POHYB = [pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s]

##################################
#   TOTO TU SOM ROBIL 3 HODINY   #
##################################
# HRAC NARAZA DO NEPRIECHODNYCH  #
# VECI A ZAROVEN KLZE PO STENACH #
##################################

#self potrebuje mat x,y,rychlost,svet
def daSaIst(self, smer4):
	DDX = [-1,-1,0,1,1,1,0,-1]
	DDY = [0,-1,-1,-1,0,1,1,1]
	smer8 = 2*smer4
	#pre kazdy pohyb overime 3 body posunute v smere tohto pohybu
	for okolie in [-1,0,1]:
		ss = (smer8+okolie+8)%8
		ny = (self.y + DDY[ss]*(GRID/2-1) + DDY[smer8]*self.rychlost) / GRID
		nx = (self.x + DDX[ss]*(GRID/2-1) + DDX[smer8]*self.rychlost) / GRID
		ny = min( max(0, ny), self.svet.vyska-1)
		nx = min( max(0, nx), self.svet.sirka-1) 
		if (self.svet.mapa[ny][nx]!=0) and (not self.svet.mapa[ny][nx].priechodne): return False
	return True
	
# Objekty, ktore su pouzivane sami o sebe
	
class Hrac(Obrazok):
	def nastav(self, x, y, *ine):
		self.x = x
		self.y = y
		self.nastavSubor("grafika", "hrac.png")
		self.priechodne = False

		self.rychlost = 2
		self.zivoty = 100

	def krok(self):
		#pohyb, ktory overuje priechodne a nepriechodne objekty
		for i in range(4):
			if self.svet.stlacene[KEY_POHYB[i]] and daSaIst(self, i):
				self.x += self.rychlost*DX[i]
				self.y += self.rychlost*DY[i]

class Stena(Obrazok):
	def nastav(self, x, y, *ine):
		self.x = x
		self.y = y
		self.priechodne = False
		self.nastavSubor("grafika", "stena2.png")

class Dvere(Obrazok):
	def nastav(self, x, y, *ine):
		self.x = x
		self.y = y
		self.priechodne = False
		self.typ = ord(ine[0]) - ord('A')
		self.nastavSubor("grafika","drevozamok"+str(self.typ) +".png")

	@priZrazke(Hrac)
	def pokusOOtvorenie(self,hrac):
		pass

# Classy, ktore su zakladom pre rozne typy priser/itemov

class Prisera(Vec):
	def nastav(self, x, y, *ine):
		self.x = x
		self.y = y
		self.priechodne = False

		self.zivoty = 0
		self.utok = 0
		self.odmeny = []

	def zomri(self):
		self.znic()

class Item(Obrazok):
	def nastav(self, x, y, *ine):
		self.x = x
		self.y = y
		self.priechodne = True
		self.hrac = None
		
	@priZrazke(Hrac)
	def zodvihnuteHracom(self, hrac):
		pass

	def pouzi(self):
		pass

# Odvodeniny od zakladnych class

class NapojZivoty(Item, Obrazok):
	def nastav(self, x, y, *ine):
		super(NapojZivoty, self).nastav(x,y)
		self.nastavSubor("grafika","napojZivoty.png")

	def zodvihnuteHracom(self, hrac):
		self.hrac = hrac	

	def pouzi(self):
		self.hrac.zivoty += 30

class Kluc(Item, Obrazok):
	def nastav(self, x, y, *ine):
		super(Kluc, self).nastav(x,y)
		self.typ = int(ine[0])
		self.nastavSubor("grafika","kluc"+str(self.typ)+".png")

# Svety

class Miestnost(Svet):
	legenda = {
		'H': Hrac,
		'#': Stena,
		'Z': NapojZivoty,
		'0': Kluc,  '1': Kluc,  '2': Kluc,  '3': Kluc,	#typy kluca
		'A': Dvere, 'B': Dvere, 'C': Dvere, 'D': Dvere
	}

	def nastav(self):
		# Dvojrozmerne pole objektov, jediny objekt, co nie je na mape je hrac
		self.mapa = []
		self.nacitajMiestnostZoSuboru("miestnosti","0.room")

	def nacitajMiestnostZoSuboru(self, *paths):
		mapa = open(os.path.join(*paths),'r').read().strip().split('\n')
		self.vyska = len(mapa)
		self.sirka = len(mapa[0])
		self.mapa = [ [0 for x in range(self.sirka)] for y in range(self.vyska) ]
		for i in range(self.vyska):
			for j in range(self.sirka):
				if mapa[i][j] == 'H':
					self.hrac = Hrac(self, j*GRID+GRID/2, i*GRID+GRID/2) 
				elif mapa[i][j] in self.legenda : 
					self.mapa[i][j] = self.legenda[mapa[i][j]](self, j*GRID+GRID/2, i*GRID+GRID/2, mapa[i][j])
		okno.sirka = self.sirka*GRID
		okno.vyska = self.vyska*GRID

okno.nazov = "Dungeon"
hra.start(Miestnost())