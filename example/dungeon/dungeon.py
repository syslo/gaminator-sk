import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', '..', 'src')))

from gaminator import *

#velkost dlazdiciek
GRID = 30
VYSKA_SPODNEHO_BARU = GRID + 16
#Pomocne polia pre navigaciu
DX = [-1,0,1,0]
DY = [0,-1,0,1]
KEY_POHYB = [pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s]

#bez inventara, zrazky iba s dverami/stenami, prisery ziju
#itemy nemaju pouzi

#zrazky s priserami 				- aby uberali hp a a odskakovali
#bomba, zmraz, (pridaj zivot) 		- udalost pri zrazke s itemom
#pasce, odmraz 						- nacasujUdalost 
#klavesDole
#------------------------------------
#inventar(append,remove,for,break)	- presun predmet do inventara/ do pola
#pouzivanie inventara+pouzi() 		- vlastna klasa
#------------------------------------
#Pauza/GameOver	(Uvodny)			- novySvet, vymenSvet + Texty
#------------------------------------
#Scrolly							- citanie zo suboru
#------------------------------------
#Prechod do noveho levelu			- subory, novyhrac

#zranennie volaj priamo, camelcase stare, bomba
#zmaz sys.path

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
		nny = min( max(0, ny), self.svet.vyska-1)
		nnx = min( max(0, nx), self.svet.sirka-1) 
		if (self.svet.mapa[nny][nnx]!=0) or (nnx != nx) or (nny != ny): return False
	return True
	
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
		self.vysunuta = False

	@priUdalosti("VYSUN")
	def vysun(self):
		self.nastavSubor("grafika","ohen.png")
		self.vysunuta = True

	@priUdalosti("ZASUN")
	def zasun(self):
		self.nastavSubor("grafika","ohenzamrezami.png")
		self.vysunuta = False

# Specialne template objekty
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
		kreslic.obdlznik( (-GRID/2,-GRID/2-5), GRID*z/m, 3)

class Prisera(Obrazok):
	def nastav(self, x, y, znak):
		self.x = x
		self.y = y
		self.nazov = self.__class__.__name__
		
		self.stoj = False
		self.rychlost = 0
		self.smer = 0
		self.starax = self.x
		self.staray = self.y

		self.lifebar = Lifebar(self.svet, self)
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

	@priUdalosti("ZRANENIE")
	def zranenenie(self, mnozstvo, prisera=None):
		if prisera == None or prisera == self:
			self.zivoty -= mnozstvo
			if self.zivoty <= 0:
				self.zomri()

	@priUdalosti("ZMRAZ")
	def zmraz(self,cas):
		self.svet.nacasujUdalost(cas,"ODMRAZ")
		self.stoj = True

	@priUdalosti("ODMRAZ")
	def odmraz(self):
		self.stoj = False

	@priZrazke(Dvere)
	def dvereVCeste(self,dvere):
		self.x = self.starax
		self.y = self.staray

class Item(Obrazok):
	def nastav(self, x, y, znak):
		self.x = x
		self.y = y
		self.nazov = self.__class__.__name__
		
	def pouzi(self):
		pass

# GUI
class StatusBar(Vec):
	def nastav(self):
		self.x = 0
		self.y = okno.vyska-GRID-16
		self.zivoty = Text(self.svet)
		self.zivoty.y = okno.vyska - GRID - 8
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

class Inventar(Vec):
	def nastav(self, velkost):
		self.predmety = []
		self.velkost = velkost
		self.x = (okno.sirka-velkost*GRID)/2
		self.y = okno.vyska - GRID
		self.z = 100
		self.oznaceny = 0

	def nakresli(self,kreslic):
		kreslic.farba = Farba(100, 50, 0)
		for i in range(self.velkost):
			kreslic.obdlznik( (i*GRID, 0), GRID, GRID,2)
		kreslic.farba = Farba.CERVENA
		kreslic.obdlznik( (self.oznaceny*GRID, 0), GRID, GRID,2)

	def pridajPredmet(self, predmet):
		if len(self.predmety) >= self.velkost:
			return
		else:
			self.predmety.append(predmet)
			predmet.x = self.x+len(self.predmety)*GRID - GRID/2
			predmet.y = okno.vyska - GRID/2

	def pouziPredmet(self, index):
		if self.predmety[index] == None: return
		self.predmety[index].pouzi()
		for i in range(index, len(self.predmety)-1):
			self.predmety[i] = self.predmety[i+1]
			self.predmety[i].x -= GRID
		self.predmety.pop()

	@priUdalosti("KLAVES DOLE")
	def klaves(self, klaves, unicode):
		if klaves == pygame.K_q:
			self.oznaceny = (self.oznaceny - 1 + self.velkost) % self.velkost
		elif klaves == pygame.K_e:
			self.oznaceny = (self.oznaceny + 1 + self.velkost) % self.velkost
		elif klaves == pygame.K_SPACE:
			if not isinstance( self.predmety[self.oznaceny], Kluc):
				self.pouziPredmet(self.oznaceny)

# Hrac
class Hrac(Obrazok):
	def nastav(self, x, y, znak):
		self.x = x
		self.y = y
		self.nastavSubor("grafika", "hrac.png")

		self.starax = x
		self.staray = y

		self.inventar = None
		
		self.zivoty = 300
		self.maxZivoty = 300
		self.utok = 1 
		self.rychlost = 2

	def krok(self):
		self.starax = self.x
		self.staray = self.y
		#pohyb, ktory overuje zrazky so stenami
		for i in range(4):
			if self.svet.stlacene[KEY_POHYB[i]] and daSaIst(self, i):
				self.x += self.rychlost*DX[i]
				self.y += self.rychlost*DY[i]

	def zranenenie(self, mnozstvo):
		self.zivoty -= mnozstvo
		if self.zivoty <= 0:
			self.zomri()

	def zomri(self):
		hra.koniec()

	@priUdalosti("VYLIEC HRACA")
	def vyliec(self, mnozstvo):
		self.zivoty = min( self.zivoty + mnozstvo, self.maxZivoty )

	@priZrazke(Dvere)
	def pokusOOtvorenie(self, dvere):
		for i in range( len(self.inventar.predmety) ):
			if self.inventar.predmety[i].nazov == "Kluc" and (self.inventar.predmety[i].typ == dvere.typ):
				self.inventar.pouziPredmet(i)
				dvere.znic()
				break
		self.x = self.starax
		self.y = self.staray
		
	@priZrazke(Pasca)
	def padDoPasce(self, pasca):
		if pasca.vysunuta:
			self.zranenenie(3)

	@priZrazke(Prisera)
	def bojSPriserou(self, prisera):
		self.svet.nastalaUdalost("ZRANENIE",self.utok,prisera)
		self.zranenenie(prisera.utok)
		self.x = self.starax
		self.y = self.staray

	@priZrazke(Item)
	def zoberItem(self, predmet):
		if predmet.nazov == "Zvitok":
			self.x = self.starax
			self.y = self.staray
		else:
			self.inventar.pridajPredmet(predmet)

# Odvodeniny od zakladnych class
class NapojZivoty(Item):
	def nastav(self, x, y, znak):
		super(NapojZivoty, self).nastav(x,y,znak)
		self.nastavSubor("grafika","napojZivoty.png")

	def pouzi(self):
		self.svet.nastalaUdalost("VYLIEC HRACA", 50)
		self.znic()

class Kluc(Item):
	def nastav(self, x, y, znak):
		super(Kluc, self).nastav(x,y,znak)
		self.typ = int(znak)
		self.nastavSubor("grafika","kluc"+str(self.typ)+".png")

	def pouzi(self):
		self.znic()

class Zmrazovac(Item):
	def nastav(self, x, y, znak):
		super(Zmrazovac, self).nastav(x,y,znak)
		self.nastavSubor("grafika","zmrazovac.png")

	def pouzi(self):
		self.svet.nastalaUdalost("ZMRAZ", 3000)
		self.znic()

class Zvitok(Item):
	def nastav(self, x, y, znak):
		super(Zvitok, self).nastav(x,y,znak)
		self.nastavSubor("grafika","zvitok.png")
		self.text = open("zvitok"+str(znak)+".txt","r").read().strip().split("\n")

	@priZrazke(Hrac)
	def precitaj(self, hrac):
		hra.otvorSvet(SvetZvitok(self.text))

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
			if not daSaIst(self, self.smer): 
				self.smer = (self.smer + 1) % 4
			else:
				break

		if nahodneCislo(0, 120) == 0:
			self.smer = nahodneCislo(0, 3)

		if daSaIst(self, self.smer):		
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
					self.hrac = Hrac(self, j*GRID+GRID/2, i*GRID+GRID/2,mapa[i][j]) 
				elif mapa[i][j] in LEGENDA: 
					LEGENDA[mapa[i][j]](self, j*GRID+GRID/2, i*GRID+GRID/2, mapa[i][j])
					if mapa[i][j] == '#': self.mapa[i][j] = 1
		okno.sirka = self.sirka*GRID
		okno.vyska = self.vyska*GRID + VYSKA_SPODNEHO_BARU
		self.hrac.inventar = Inventar(self,10)
		StatusBar(self)
		self.nastalaUdalost("VYSUN")
	
	@priUdalosti("KLAVES DOLE")
	def klaves(self, klaves, unicode):
		if klaves == pygame.K_p:
			hra.otvorSvet(Pauza())

	@priUdalosti("VYSUN")
	def vysun(self):
		self.svet.nacasujUdalost(1300, "ZASUN")

	@priUdalosti("ZASUN")
	def zasun(self):
		self.svet.nacasujUdalost(1300, "VYSUN")

class Pauza(Svet):
	def nastav(self):
		t1 = Text(self)
		t1.x = okno.sirka/2
		t1.y = okno.vyska/2
		t1.aktualizuj(velkost = 30, text = "PAUZA")

		t2 = Text(self)
		t2.x = okno.sirka/2
		t2.y = okno.vyska/2+20
		t2.aktualizuj(velkost = 20, text = "Stlacte [P] pre pokracovanie.")

	@priUdalosti("KLAVES DOLE")
	def klaves(self, klaves, unicode):
		if klaves == pygame.K_p:
			hra.zatvorSvet()

class SvetZvitok(Svet):
	def nastav(self, text):
		okrajHore = 30
		okrajVlavo = 30
		velkost = 20

		for line in text:
			t = Text(self)
			t.x = okrajVlavo
			t.y = okrajHore
			okrajHore += 20
			t.zarovnajX = 0
			t.aktualizuj(text = line, velkost = velkost)

		t = Text(self)
		t.x = 0
		t.y = okno.vyska
		t.zarovnajX = 0
		t.zarovnajY = 1
		t.aktualizuj(text = "Pre navrat do hry stlacte [ESC].", velkost = velkost)

	@priUdalosti("KLAVES DOLE")
	def odid(self, klaves, unicode):
		if klaves == pygame.K_ESCAPE:
			hra.zatvorSvet()

okno.nazov = "Dungeon"
hra.start(Miestnost())