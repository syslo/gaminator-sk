import sys
import os
sys.path.append(os.path.abspath(os.path.join('..','..', 'src')))

from gaminator import *
import random

#ZRAZKY - Had(sam so sebou), Stena(s hadom), Jedlo(so stenou a hadom)
#EVENTY - smrt, zjedene jedlo_nech sa objavi nove

TYPY_JEDLA = ["NORMAL", "SPEED", "LIFE", "IMMORTALITY", "FAT", "NONE"]			
MIERKA = 15
RYCHLOST = 5
POCET_BEZPECNYCH_CASTI_TELA = 4
DLZKA_ZJAVENIA = 4000
DLZKA_EFEKTU = 3000
IMMORTALITY = 0
INF = 1000000000

#Pomocne polia pre navigaciu hadika
DX = [-1,0,1,0]
DY = [0,-1,0,1]

#Velkost obrazovky
SIRKA = 600
VYSKA = 400

#TODO 
#	zaklady
#		- userfriendly keydown
#		- vypis textu, nacitanie z obrazku

#	hratelnost
#		- texty v menu / high score / helpe / hra-horny panel
#		- ukladanie high score

#	grafika
#		- obrazok pre kazde jedlo
#		- pozadie pre kazdy level
#		- obrazky do menu
#		+ cool hadik a steny z nejakych tileov

#	levely

#CASTI HRY - LEVELU

class Cast_tela(Vec):
	"""Kazda ina cast tela hada okrem hlavy. Casti tela sa pohybuju posuvanim na miesto predoslej."""
	def nastav(self):
		self.k_hlave = 0
		self.k_chvostu = 0
		self.smer = 0
		self.poradie = 0
		self.miesto_vlavo = self.miesto_vpravo = self.miesto_hore = self.miesto_dole = 0

	def nakresli(self, kreslic):
		kreslic.farba = Farba.CIERNA
		kreslic.elipsa( (- MIERKA//2 +1, - MIERKA//2 +1), MIERKA -2, MIERKA -2)

	def _krok(self):
		if self.k_chvostu != 0:
			self.k_chvostu._krok()
		self.smer = self.k_hlave.smer
		self.x    = self.k_hlave.x 
		self.y    = self.k_hlave.y 

	def pridaj_telo(self):
		if self.k_chvostu == 0:
			dalsi = Cast_tela(self.svet)
			self.k_chvostu = dalsi 
			dalsi.k_hlave = self
			dalsi.poradie = self.poradie+1
			dalsi.smer = self.smer
			dalsi.x    = self.x - DX[self.smer]*RYCHLOST
			dalsi.y    = self.y - DY[self.smer]*RYCHLOST
		else:
			self.k_chvostu.pridaj_telo()
		
class Had(Vec):
	"""Hlava hada - papa a robi vsetky rozhodnutia, kam sa pohnut."""
	def nastav(self):
		self.smer = 0
		self.k_chvostu = 0
		self.miesto_vlavo = self.miesto_vpravo = self.miesto_hore = self.miesto_dole = MIERKA//2-2
		self.z = 100

		#kontrola stlacania
		self.dalsie_stlacenie = 0

	def krok(self):
		"""Reaguje na klavesy a hybe sa. Spusti _krok() aj pre casti tela."""
		if (self.svet.stlacene[pygame.K_LEFT] or self.svet.stlacene[pygame.K_RIGHT]) and self.svet.cas > self.dalsie_stlacenie:
			if self.svet.stlacene[pygame.K_LEFT]: 
				self.smer = (self.smer - 1 + 4) % 4
			elif self.svet.stlacene[pygame.K_RIGHT]: 
				self.smer = (self.smer + 1 + 4) % 4
			self.dalsie_stlacenie = self.svet.cas + 100 
		
		if self.k_chvostu != 0:
			self.k_chvostu._krok()	
		self.x = (self.x + DX[self.smer]*RYCHLOST + SIRKA) % SIRKA
		self.y = (self.y + DY[self.smer]*RYCHLOST + VYSKA) % VYSKA

	def nakresli(self, kreslic):
		kreslic.farba = Farba.CIERNA
		kreslic.elipsa( (- MIERKA//2, - MIERKA//2), MIERKA, MIERKA)

	def pridaj_telo(self):
		if self.k_chvostu == 0:
			dalsi = Cast_tela(self.svet)
			self.k_chvostu = dalsi 
			dalsi.poradie = 1
			dalsi.smer = self.smer
			dalsi.k_hlave = self
			dalsi.x = self.x - DX[self.smer]*RYCHLOST
			dalsi.y = self.y - DY[self.smer]*RYCHLOST
		else:
			self.k_chvostu.pridaj_telo()

	@priZrazke(Cast_tela)
	def zarazka_so_sebou(self, cast):
		if cast.poradie > POCET_BEZPECNYCH_CASTI_TELA:
			self.svet.nastalaUdalost("smrt")

class Stena(Vec):
	"""Obycajny obdlznik... Po naraze nasleduje smrt."""
	def inicializuj(self,x1,y1,x2,y2):
		self.x = x1
		self.y = y1
		self.miesto_vpravo = x2-x1
		self.miesto_dole  = y2-y1

	def nakresli(self,kreslic):
		kreslic.farba = Farba.CIERNA
		kreslic.obdlznik((0,0), self.miesto_vpravo, self.miesto_dole)

	@priZrazke(Had)
	def zrazka_s_hadom(self,had):
		self.svet.nastalaUdalost("smrt")

class Jedlo(Vec):
	"""Upravy staty a posle svetu spravu, nech sa vygeneruje dalsie.
	   NORMAL, SPEED, LIFE, IMMORTALITY, FAT"""
	def nove_miesto(self):
		self.x = random.randrange(SIRKA)
		self.y = random.randrange(VYSKA)

	def nastav(self):
		self.typ = "NORMAL"
		self.nove_miesto()
		self.miesto_vlavo=self.miesto_vpravo=self.miesto_dole=self.miesto_hore = 10
		self.vyprsanie = INF

	def zmen_typ(self,typ):
		self.typ = typ
		if typ != "NORMAL":
			self.vyprsanie = self.svet.cas + DLZKA_ZJAVENIA

	def nakresli(self,kreslic):
		if self.typ == "NORMAL":
			kreslic.farba = Farba.CERVENA
		else:
			kreslic.farba = Farba.ZLTA
		kreslic.elipsa( (-10, -10), 20, 20 )
		#toto by malo byt v urob krok
		if self.svet.cas > self.vyprsanie: 
			self.znic()

	@priZrazke(Had)
	def zrazka_s_jedlom(self, had):
		self.svet.nastalaUdalost(self.typ)
		self.znic()
		
	@priZrazke(Stena)
	def zrazka_jedla_so_stenou(self, stena):
		self.nove_miesto()			

#STRUKTURA LEVELOV

class Player_data():
	def __init__(self):
		self.dlzka  = 0
		self.smer   = 1
		self.level  = 0
		self.skore  = 0
		self.zivoty = 0
		
	def load_from_file(self, nazov_suboru):
		with open(nazov_suboru,"r") as file: 
			parametre = []
			for line in file:
				parametre.append(int(line))	
			self.dlzka, self.smer, self.level, self.skore, self.zivoty = parametre

class Level_data():
	def __init__(self):
		self.max_score = 0
		self.bonusy = []
		self.steny = []		#stvorice

	def load_from_file(self, nazov_suboru):
		with open(nazov_suboru,"r") as file: 
			i = 0
			parametre = []
			for line in file:
				if i==0: 
					self.max_score =  int(line.strip(),10) 
				elif i==1:
					self.bonusy = [ int(x,10) for x in line.strip().split(" ")]
				else:
					self.steny.append( [ int(x,10) for x in line.strip().split(" ")] )
				i += 1

class Level(Svet):
	def nastav(self):
		self.posledna_smrt = 0		
		
	def load_from_file(self, save):
		#RESET GLOBALNYCH "PREMENNYCH"
		global RYCHLOST
		RYCHLOST = 5
		global IMMORTALITY
		IMMORTALITY = 0
		global MIERKA
		MIERKA = 15

		#HRAC
		hrac = Player_data()
		hrac.load_from_file(save)

		self.dlzka = hrac.dlzka
		self.level = hrac.level
		self.skore = hrac.skore
		self.zivoty = hrac.zivoty

		self.hadik = Had(self)
		self.hadik.smer = hrac.smer
		self.hadik.x, self.hadik.y = SIRKA/2, VYSKA/2
		for i in range(self.dlzka): self.hadik.pridaj_telo()
		
		#LEVEL
		level = Level_data()
		level.load_from_file("level"+str(self.level)+".data")

		self.max_score = level.max_score

		for x1,y1,x2,y2 in level.steny:
			st = Stena(self)
			st.inicializuj(x1, y1, x2, y2)

		jedlo = Jedlo(self)
		self.bonusy = level.bonusy
		self.terajsi_bonus = 0
			
	def uloz_hraca(self, save):
		with open(save,"w") as f: 
			f.write(str(self.dlzka) +"\n") 
			f.write(str(self.hadik.smer) + "\n")
			f.write(str(self.level) + "\n")
			f.write(str(self.skore) + "\n")
			f.write(str(self.zivoty) + "\n")
				
	def krok(self):
		okno.nazov ="Body: "+str(self.skore)+", Zivoty: "+str(self.zivoty)

		if self.stlacene[pygame.K_ESCAPE]:
			hra.zatvorSvet()

		if self.skore >= self.max_score:
			self.level += 1
			self.uloz_hraca("quicksave.data")
			level = Level()
			level.load_from_file("quicksave.data")
			hra.nahradSvet(level)
	
	@priUdalosti("smrt")
	def nastala_smrt(self):
		if IMMORTALITY != 0:
			return

		if self.cas < self.posledna_smrt+100:
			return
		else:
			self.posledna_smrt = self.cas

		if self.zivoty == 0:
			hra.nahradSvet(HighScore())
		else:
			self.zivoty -= 1
			self.hadik.x = SIRKA//2
			self.hadik.y = VYSKA//2

	#Udalosti spustene jedlom
	@priUdalosti("NORMAL")
	def jedlo_NORMAL(self):
		self.skore += 1
		self.hadik.pridaj_telo()
		self.jedlo = Jedlo(self)
		if random.randrange(4) == 0:
			self.bonus = Jedlo(self)
			self.bonus.zmen_typ(TYPY_JEDLA[self.bonusy[self.terajsi_bonus]])
			self.terajsi_bonus = (self.terajsi_bonus+1) % len(self.bonusy)

	@priUdalosti("LIFE")
	def jedlo_LIFE(self):
		self.zivoty += 1

	@priUdalosti("SPEED")
	def jedlo_SPEED(self):
		global RYCHLOST
		RYCHLOST += 3
		self.nacasujUdalost( DLZKA_EFEKTU, "xSPEED")

	@priUdalosti("xSPEED")
	def jedlo_xSPEED(self):
		global RYCHLOST
		RYCHLOST -= 3

	@priUdalosti("IMMORTALITY")
	def jedlo_IMMORTALITY(self):
		global IMMORTALITY
		IMMORTALITY += 1
		self.nacasujUdalost( DLZKA_EFEKTU, "xIMMORTALITY")

	@priUdalosti("xIMMORTALITY")
	def jedlo_xIMMORTALITY(self):
		global IMMORTALITY
		IMMORTALITY -= 1

	@priUdalosti("FAT")
	def jedlo_FAT(self):
		global MIERKA
		MIERKA += 4
		self.hadik.miesto_vpravo +=2
		self.hadik.miesto_vlavo  +=2
		self.hadik.miesto_hore   +=2
		self.hadik.miesto_dole   +=2
		self.nacasujUdalost(DLZKA_EFEKTU, "xFAT")

	@priUdalosti("xFAT")
	def jedlo_xFAT(self):
		global MIERKA
		MIERKA -= 4
		self.hadik.miesto_vpravo -=2
		self.hadik.miesto_vlavo  -=2
		self.hadik.miesto_hore   -=2
		self.hadik.miesto_dole   -=2

#MENU

class Textholder(Vec):
	def vytvor_sa(self,x,y,sirka,vyska,text):
		self.x = x
		self.y = y
		self.vyska = vyska
		self.sirka = sirka
		self.napis = text
		self.vysvietene= False
		
	def nakresli(self,kreslic):
		if self.vysvietene:
			kreslic.farba = Farba.CERVENA
		else:
			kreslic.farba = Farba(255, 150, 0)
		kreslic.obdlznik( (-self.sirka/2, -self.vyska/2),self.sirka,self.vyska)	
		
class UvodneMenu(Svet):

	def nastav(self):
		self.banner = Textholder(self)
		self.banner.vytvor_sa(SIRKA/2, 95, SIRKA-80, 90, "HADIIIIIIIIIK")

		self.nazvy = ["NEW GAME", "HIGH SCORE", "HELP"]
		self.tlacitka = []
		for i in range(len(self.nazvy)):
			self.tlacitka.append( Textholder(self) )
			self.tlacitka[i].vytvor_sa(SIRKA//2, 180+i*(60+10), 240, 60, self.nazvy[i])

		self.vybrane = 0
		self.dalsie_stlacenie = 0

	def krok(self):
		"""Reaguje na klavesy a hybe sa. Spusti _krok() aj pre casti tela."""
		if (self.stlacene[pygame.K_UP] or self.stlacene[pygame.K_DOWN]) and self.cas > self.dalsie_stlacenie:
			if self.stlacene[pygame.K_UP]: 
				self.vybrane = (self.vybrane - 1 + len(self.tlacitka)) % len(self.tlacitka)
			elif self.stlacene[pygame.K_DOWN]: 
				self.vybrane = (self.vybrane + 1 + len(self.tlacitka)) % len(self.tlacitka)
			for t in self.tlacitka: t.vysvietene = False
			self.dalsie_stlacenie = self.cas + 100 
		self.tlacitka[self.vybrane].vysvietene = True

		if (self.stlacene[pygame.K_RETURN]):
			self.nastalaUdalost( self.tlacitka[self.vybrane].napis )
		
	@priUdalosti("NEW GAME")
	def nova_hra(self):
		level = Level()
		level.load_from_file("save0.data")
		hra.otvorSvet(level)

	@priUdalosti("HIGH SCORE")
	def skore(self):
		hra.otvorSvet(HighScore())

	@priUdalosti("HELP")
	def pomoc(self):
		hra.otvorSvet(Help())
		pass

class HighScore(Svet):
	def nastav(self):
		self.zapisujem = 0
		self.zaznamy = []		#skore, meno, cas
		with open("highscore.data") as file:
			for line in file:
				self.zaznamy.append(  [ x for x in line.strip().split("|")] )
		for i in range(len(self.zaznamy)):
			th = Textholder(self)
			th.vytvor_sa(SIRKA/2, 100 + i*(40+10), SIRKA-20, 40, "   ".join(self.zaznamy[i]) )

	def krok(self):
		if self.stlacene[pygame.K_ESCAPE]:
			hra.zatvorSvet()

class Help(Svet):
	def nastav(self):
		text = ""
		th = Textholder(self)
		th.vytvor_sa(SIRKA/2,VYSKA/2,SIRKA-20,VYSKA-20,text)

	def krok(self):
		if self.stlacene[pygame.K_ESCAPE]:
			hra.zatvorSvet()

#MAIN

okno.sirka = SIRKA
okno.vyska = VYSKA
hra.fps = 60
hra.start(UvodneMenu())
