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
DDX = [-1,-1,0,1,1,1,0,-1]
DDY = [0,-1,-1,-1,0,1,1,1]

# Objekty, ktore su pouzivane sami o sebe

class Hrac(Obrazok):
	def nastav(self, x, y):
		self.x = x
		self.y = y
		self.rychlost = 2
		self.nastavSubor("grafika", "hrac.png")

		self.zivoty = 100

	def krok(self):
		##################################
		#   TOTO TU SOM ROBIL 3 HODINY   #
		##################################
		# HRAC NARAZA DO NEPRIECHODNYCH  #
		# VECI A ZAROVEN KLZE PO STENACH #
		##################################

		#pohyb zo 4 smerov prevedieme na 8
		smer8,dx,dy = -1,0,0
		for i in range(4):
			if self.svet.stlacene[KEY_POHYB[i]]:
				dx += DX[i]
				dy += DY[i]
		for i in range(8):
			if dx == DDX[i] and dy == DDY[i]: smer8 = i
		
		if smer8 != -1:
			final = -1
			okolie = [0,1,-1]
			# skusime 3 pohyby do 3 smerov blizkych povodnemu (napr. klzanie po stene pri W+D)
			for i in okolie:
				smer = (smer8+i+8)%8
				#pre kazdy pohyb overime 3 body posunute v smere tohto pohybu
				for s in okolie:
					ss = (smer+s+8)%8
					ny = (self.y + DDY[ss]*(GRID/2-1) + DDY[smer]*self.rychlost) / GRID
					nx = (self.x + DDX[ss]*(GRID/2-1) + DDX[smer]*self.rychlost) / GRID
					if not self.svet.mapa[ny][nx].priechodne: break
				else:
					final = smer
					break
			
			if final != -1:
				self.x += self.rychlost*DDX[final]
				self.y += self.rychlost*DDY[final]

class Stena(Obrazok):
	def nastav(self, x, y):
		self.x = x
		self.y = y
		self.priechodne = False
		self.nastavSubor("grafika", "stena2.png")

class Nic(Vec):
	def nastav(self, x, y):
		self.x = x
		self.y = y
		self.priechodne = True

# Classy, ktore su zakladom pre rozne typy priser/itemov

class Prisera(Vec):
	def nastav(self, x, y):
		self.x = x
		self.y = y
		self.priechodne = False

		self.zivoty = 0
		self.utok = 0
		self.odmeny = []

	def zomri(self):
		self.znic()

class Item(Obrazok):
	def nastav(self, x, y):
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
	def nastav(self, x, y):
		super(NapojZivoty, self).nastav(x,y)
		self.nastavSubor("grafika","napojZivoty.png")

	def zodvihnuteHracom(self, hrac):
		self.hrac = hrac
		self.pouzi()

	def pouzi(self):
		self.hrac.zivoty += 30
		self.znic()
# Svety

class Miestnost(Svet):
	legenda = {
		'H': Hrac,
		'#': Stena,
		'.': Nic,
		'Z': NapojZivoty
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
					self.mapa[i][j] = Nic(self, j*GRID+GRID/2, i*GRID+GRID/2)
				else: 
					self.mapa[i][j] = self.legenda[mapa[i][j]](self, j*GRID+GRID/2, i*GRID+GRID/2)
		okno.sirka = self.sirka*GRID
		okno.vyska = self.vyska*GRID

okno.nazov = "Dungeon"
hra.start(Miestnost())