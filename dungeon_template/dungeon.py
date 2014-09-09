import os
from gaminator import *
import dungeon_utility as utility


#Pomocne polia pre navigaciu
DX = [-1,0,1,0]
DY = [0,-1,0,1]
KEY_POHYB = [pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s]
#velkost dlazdiciek
GRID = 30

# Staticke objekty
class Stena(Obrazok):
	def nastav(self, x, y, znak):
		self.x = x
		self.y = y
		self.nastavSubor("grafika", "stena2.png")

class Dvere(Obrazok):
	def nastav(self, x, y, znak):
		self.x = x
		self.y = y
		self.typ = ord(znak) - ord('A')
		self.nastavSubor("grafika","drevozamok"+str(self.typ) +".png")

class Pasca(Obrazok):
	def nastav(self, x, y, znak):
		self.x = x
		self.y = y
		self.vysun()

	def vysun(self):
		self.nastavSubor("grafika","ohen.png")
		self.vysunuta = True

	def zasun(self):
		self.nastavSubor("grafika","ohenzamrezami.png")
		self.vysunuta = False

# Specialne template objekty

class Prisera(Obrazok):
	def nastav(self, x, y, znak):
		self.x = x
		self.y = y
		self.nazov = self.__class__.__name__
		
		self.stoj = False
		self.rychlost = 0
		self.smer = 0
		self.staraX = self.x
		self.staraY = self.y

		self.lifebar = utility.Lifebar(self.svet, self)
		self.zivoty = 0
		self.maxZivoty = 0
		self.utok = 0
		self.odmeny = [] #zoznam charakterovych skratiek pre itemy

	def zomri(self):
		for odmena in self.odmeny:
			if odmena in LEGENDA:
				LEGENDA[odmena](self.svet, self.x, self.y, odmena)
		self.lifebar.znic()
		self.znic()

	@priZrazke(Dvere)
	def dvereVCeste(self,dvere):
		self.x = self.staraX
		self.y = self.staraY

class Item(Obrazok):
	def nastav(self, x, y, znak):
		self.x = x
		self.y = y
		self.nazov = self.__class__.__name__		

# Hrac
class Hrac(Obrazok):
	def nastav(self, x, y, znak):
		self.x = x
		self.y = y
		self.nastavSubor("grafika", "hrac.png")
		self.staraX = x
		self.staraY = y
		
		self.zivoty = 300
		self.maxZivoty = 300
		self.utok = 1 
		self.rychlost = 2

	def krok(self):
		self.staraX = self.x
		self.staraY = self.y
		#pohyb, ktory overuje zrazky so stenami
		for i in range(4):
			if self.svet.stlacene[KEY_POHYB[i]] and utility.daSaIst(self, i):
				self.x += self.rychlost*DX[i]
				self.y += self.rychlost*DY[i]

	@priZrazke(Dvere)
	def pokusOOtvorenie(self, dvere):
		self.x = self.staraX
		self.y = self.staraY
		
# Odvodeniny od zakladnych class
class NapojZivoty(Item):
	def nastav(self, x, y, znak):
		super(NapojZivoty, self).nastav(x,y,znak)
		self.nastavSubor("grafika","napojZivoty.png")

class Kluc(Item):
	def nastav(self, x, y, znak):
		super(Kluc, self).nastav(x,y,znak)
		self.typ = int(znak)
		self.nastavSubor("grafika","kluc"+str(self.typ)+".png")

class Zmrazovac(Item):
	def nastav(self, x, y, znak):
		super(Zmrazovac, self).nastav(x,y,znak)
		self.nastavSubor("grafika","zmrazovac.png")

class Zvitok(Item):
	def nastav(self, x, y, znak):
		super(Zvitok, self).nastav(x,y,znak)
		self.nastavSubor("grafika","zvitok.png")

#NESNASTE SA POCHOPIT FUNGOVANIE KONKRETNEJ PRISERY
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

# Svety
LEGENDA = {
	'H': Hrac,
	#staticke
	'#': Stena,
	'P': Pasca,
	'A': Dvere, 'B': Dvere, 'C': Dvere, 'D': Dvere, #typy dveri 0-3
	#itemy
	'L': NapojZivoty,
	'Z': Zmrazovac,
	'0': Kluc,  '1': Kluc,  '2': Kluc,  '3': Kluc,	#typy kluca 0-3
	'a': Zvitok,
	#prisery
	'@': Duch
}

class Miestnost(Svet):
	def nastav(self):
		self.vyska = 0
		self.sirka = 0		

okno.nazov = "Dungeon"
