import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', '..', 'src')))

from gaminator import *
import dungeon_template as dungeon

VYSKA_SPODNEHO_BARU = 16 + dungeon.GRID

# Nad priserami
class Lifebar(Vec):
	def nastav(self, prisera):
		self.prisera = prisera
		self.z = 100

	def nakresli(self, kreslic):
		self.x = self.prisera.x
		self.y = self.prisera.y
		z = self.prisera.zivoty
		m = self.prisera.maxZivoty
		if   1.*z/m > 0.5:  kreslic.farba = Farba.ZELENA
		elif 1.*z/m > 0.25: kreslic.farba = Farba.ZLTA
		else:	            kreslic.farba = Farba.CERVENA
		kreslic.obdlznik( (-dungeon.GRID/2,-dungeon.GRID/2-5), dungeon.GRID*z/m, 3)

# GUI
class StatusBar(Vec):
	def nastav(self):
		self.x = 0
		self.y = okno.vyska-dungeon.GRID-16
		self.zivoty = Text(self.svet)
		self.zivoty.y = okno.vyska - dungeon.GRID - 8
		self.zivoty.x = okno.sirka / 2
		self.zivoty.z = 100
		self.zivoty.aktualizuj(velkost = 20)

	def nakresli(self, kreslic):
		z = self.svet.hrac.zivoty
		m = self.svet.hrac.maxZivoty
		if   1.*z/m > 0.5:  kreslic.farba = Farba.ZELENA
		elif 1.*z/m > 0.25: kreslic.farba = Farba.ZLTA
		else:	            kreslic.farba = Farba.CERVENA
		kreslic.obdlznik( (0,0), okno.sirka*z/m, 16)
		self.zivoty.aktualizuj( str(z)+"/"+str(m) )

#self potrebuje mat x,y,rychlost,svet
def daSaIst(self, smer4):
	DDX = [-1,-1,0,1,1,1,0,-1]
	DDY = [0,-1,-1,-1,0,1,1,1]
	smer8 = 2*smer4
	#pre kazdy pohyb overime 3 body posunute v smere tohto pohybu
	for okolie in [-1,0,1]:
		ss = (smer8+okolie+8)%8
		ny = (self.y + DDY[ss]*(dungeon.GRID/2-1) + DDY[smer8]*self.rychlost) / dungeon.GRID
		nx = (self.x + DDX[ss]*(dungeon.GRID/2-1) + DDX[smer8]*self.rychlost) / dungeon.GRID
		nny = min( max(0, ny), self.svet.vyska-1)
		nnx = min( max(0, nx), self.svet.sirka-1) 
		if (self.svet.mapa[nny][nnx]!=0) or (nnx != nx) or (nny != ny): return False
	return True

class Duch(Prisera):
	def nastav(self, x, y, znak):
		super(Duch, self).nastav(x,y,znak)
		self.nastavSubor("grafika", "duchdraka.png")
		self.rychlost = 1
		self.zivoty = self.maxZivoty = 32
		self.utok = 3
		odmena = 'ZL__'
		self.odmeny = [odmena[nahodneCislo(0,3)]]

	def krok(self):
		if self.stoj:
			return
		for i in range(4):
			if not utility.daSaIst(self, self.smer): 
				self.smer = (self.smer + 1) % 4
			else:
				break

		if nahodneCislo(0, 120) == 0:
			self.smer = nahodneCislo(0, 3)

		if utility.daSaIst(self, self.smer):		
			self.x += DX[self.smer]*self.rychlost
			self.y += DY[self.smer]*self.rychlost

def vytvorMiestnostZoSuboru(*paths):
	self = dungeon.Miestnost()
	mapa = open(os.path.join(*paths),'r').read().strip().split('\n')
	self.vyska = len(mapa)
	self.sirka = len(mapa[0])
	self.mapa = [ [0 for x in range(self.sirka)] for y in range(self.vyska) ]
	for i in range(self.vyska):
		for j in range(self.sirka):
			if mapa[i][j] == 'H':
				self.hrac = dungeon.Hrac(self, j*dungeon.GRID+dungeon.GRID/2, i*dungeon.GRID+dungeon.GRID/2,mapa[i][j]) 
			elif mapa[i][j] in dungeon.LEGENDA: 
				dungeon.LEGENDA[mapa[i][j]](self, j*dungeon.GRID+dungeon.GRID/2, i*dungeon.GRID+dungeon.GRID/2, mapa[i][j])
				if mapa[i][j] == '#': self.mapa[i][j] = 1
	okno.sirka = self.sirka*dungeon.GRID
	okno.vyska = self.vyska*dungeon.GRID + VYSKA_SPODNEHO_BARU
	StatusBar(self)
	return self

hra.start( vytvorMiestnostZoSuboru("miestnosti", "0.room") )