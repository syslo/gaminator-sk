import os
from gaminator import *
import dungeon_utility as utility

# pomocne polia pre navigaciu
DX = [-1,0,1,0]
DY = [0,-1,0,1]
KEY_POHYB = [pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s]
# velkost dlazdiciek
GRID = 30

# STATICKE OBJEKTY - sami skoro nic nerobia, Prisera/Hrac rozhoduje co sa stane pri zrazke
#------------------

# zrazky so stenami sa automaticky overuju
class Stena(Obrazok):
	def nastav(self, x, y, znak):
		self.x = x
		self.y = y
		self.nastavSubor("grafika", "stena2.png")

# ak mate spravny kluc, mohli by ste vediet otvorit dvere rovnakej farby
class Dvere(Obrazok):
	def nastav(self, x, y, znak):
		self.x = x
		self.y = y
		self.typ = ord(znak) - ord('A')
		self.nastavSubor("grafika","drevozamok"+str(self.typ) +".png")

# pasce by sa mohli automaticky zasuvat a vysuvat
class Pasca(Obrazok):
	def nastav(self, x, y, znak):
		self.x = x
		self.y = y
		self.vysun()

	def vysun(self):
		self.nastavSubor("grafika","vysunute.png")
		self.vysunuta = True

	def zasun(self):
		self.nastavSubor("grafika","zasunute.png")
		self.vysunuta = False

# SPECIALNE NADTRIEDY - sablony, ktore popisuju zakladne vlastnosti a spravanie spolocne pre ich podtriedy
#---------------------
# pomocou self.nazov sa da zistit, aky konkretny predmet/priseru mame
class Item(Obrazok):
	def nastav(self, x, y, znak):
		self.nazov = self.__class__.__name__		
		self.x = x
		self.y = y

# prisery by mali vediet interagovat s hracom a reagovat na Udalosti
class Prisera(Obrazok):
	def nastav(self, x, y, znak):
		self.nazov = self.__class__.__name__
		self.lifebar = utility.Lifebar(self.svet, self)
		
		# pozicie prisery, pri zrazke s predmetmi sa prisera vie vratit na staru poziciu
		self.x = x
		self.y = y
		self.staraX = x
		self.staraY = y

		# premenne na ovladanie prisery
		self.stoj = False
		self.smer = 0			#cislo z [0,1,2,3]
		
		# vlastnosti, ktore si mozete sami definovat pre svoju priseru
		self.rychlost = 0
		self.zivoty = 0
		self.maxZivoty = 0 		#potrebne pri kresleni ukazovaca zivotov
		self.utok = 0

		# zoznam itemov, ktore z prisery vypadnu po jej smrti
		# format je string zo znakov v LEGENDE, napr.: "BL" vyhodi Bombu a NapojZivoty
		self.odmeny = [] 

	def zomri(self):
		for odmena in self.odmeny:
			if odmena in LEGENDA:
				LEGENDA[odmena](self.svet, self.x, self.y, odmena)
		self.lifebar.znic()
		self.znic()

	#prisery su hlupe a nevedia chodit cez dvere
	@priZrazke(Dvere)
	def dvereVCeste(self,dvere):
		self.x = self.staraX
		self.y = self.staraY

# PREDMETY - konkretne typy predmetov, kde definujeme ich vyzor a typ
#-----------
class NapojZivoty(Item):
	def nastav(self, x, y, znak):
		super(NapojZivoty, self).nastav(x,y,znak)
		self.nastavSubor("grafika","napojZivoty.png")

class Bomba(Item):
	def nastav(self, x, y, znak):
		super(Bomba, self).nastav(x, y, znak)
		self.nastavSubor("grafika", "bomba.png")

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

# PRISERY - jedna prisera na ukazku
#---------
class Duch(Prisera):
	def nastav(self, x, y, znak):
		super(Duch, self).nastav(x,y,znak)
		self.nastavSubor("grafika", "duchdraka.png")
		self.rychlost = 1
		self.zivoty = self.maxZivoty = 32
		self.utok = 3
		self.odmeny = ['OZL___'[nahodneCislo(0,5)]] # vyberie nahodnu odmenu z retazca

	def krok(self):
		# cela umela inteligencia nasej prisery -> popisuje, ako sa ma hybat
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

# HRAC
#------
class Hrac(Obrazok):
	def nastav(self, x, y, znak):
		self.nastavSubor("grafika", "hrac.png")

		# pozicie hraca, pri zrazke s predmetmi/priserami sa prisera vie vratit na staru poziciu
		self.x = x
		self.y = y
		self.staraX = x
		self.staraY = y
		
		# premenne, ktore mozete menit
		self.zivoty = 300
		self.maxZivoty = 300 		#potrebne pri kresleni ukazovaca zivotov a piti napoja zivota
		self.utok = 1 
		self.rychlost = 2

	def krok(self):
		# zaloha starej pozicie
		self.staraX = self.x
		self.staraY = self.y
		# pohyb v smere stlacenej klavesy, ktory overuje zrazky so stenami
		for i in range(4):
			if self.svet.stlacene[KEY_POHYB[i]] and utility.daSaIst(self, i):
				self.x += self.rychlost*DX[i]
				self.y += self.rychlost*DY[i]

	# hrac nevie chodit cez dvere, ale casom by ich mal vediet otvarat
	@priZrazke(Dvere)
	def pokusOOtvorenie(self, dvere):
		self.x = self.staraX
		self.y = self.staraY
		
# legenda popisu miestnosti v textovom subore
LEGENDA = {
	'H': Hrac,
	#staticke
	'#': Stena,
	'P': Pasca,
	'A': Dvere, 'B': Dvere, 'C': Dvere, 'D': Dvere, #typy dveri 0-3
	#itemy
	'L': NapojZivoty,
	'Z': Zmrazovac,
	'O': Bomba,
	'0': Kluc,  '1': Kluc,  '2': Kluc,  '3': Kluc,	#typy kluca 0-3
	'a': Zvitok,
	#prisery
	'@': Duch
}

# miestnost sa odporuca vytavarat pomocou utility.vytvorMiestnostZoSuboru(subor)
class Miestnost(Svet):
	def nastav(self):
		# pocet dlazdiciek v stlpci a riadku mapy 
		self.vyska = 0
		self.sirka = 0		

okno.nazov = "Dungeon"
#vyska a sirka okna sa nastavi podla velkosti mapy pri nacitani zo suboru
