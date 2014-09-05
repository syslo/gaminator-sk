import sys
import os
sys.path.append(os.path.abspath(os.path.join('..','..', 'src')))

from gaminator import *
import random
import time

#ZRAZKY - Had(sam so sebou), Stena(s hadom), Jedlo(so stenou a hadom)

#KONSTANTY
TYPY_JEDLA = ["NORMAL", "SPEED", "LIFE", "IMMORTALITY", "FAT", "NONE"]			
POCET_BEZPECNYCH_CASTI_TELA = 4
DLZKA_ZJAVENIA = 4000
DLZKA_EFEKTU = 3000
INF = 1000000000
#Velkost obrazovky
SIRKA = 600
VYSKA = 400
#Pomocne polia pre navigaciu hadika
DX = [-1,0,1,0]
DY = [0,-1,0,1]

#TOTO SU GLOBALNE PREMENNE - v Level.nastav() sa vzdy inicializuju na [0,15,5]
IMMORTALITY = 0
MIERKA = 15
RYCHLOST = 5

#CASTI HRY - LEVELU

class Cast_tela(Vec):
	"""Kazda ina cast tela hada okrem hlavy. Casti tela sa pohybuju posuvanim na miesto predoslej."""
	def nastav(self):
		self.k_hlave = 0
		self.k_chvostu = 0
		self.smer = 0
		self.poradie = 0
		self.miesto_vlavo = self.miesto_vpravo = self.miesto_hore = self.miesto_dole = 1

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
	def nastav(self,x,y,dlzka,smer):
		self.smer = smer
		self.k_chvostu = 0
		self.dlzka = 0
		self.miesto_vlavo = self.miesto_vpravo = self.miesto_hore = self.miesto_dole = MIERKA//2
		self.z = 100
		self.x, self.y = x,y
		for i in range(dlzka): self.pridaj_telo()
		self.pauza = False

	def krok(self):
		"""Spusti _krok() aj pre casti tela."""
		if self.pauza:
			return
		if self.k_chvostu != 0:
			self.k_chvostu._krok()	
		self.x = (self.x + DX[self.smer]*RYCHLOST + SIRKA) % SIRKA
		self.y = (self.y + DY[self.smer]*RYCHLOST + VYSKA) % VYSKA

	def nakresli(self, kreslic):
		kreslic.farba = Farba.CIERNA
		kreslic.elipsa( (- MIERKA//2, - MIERKA//2), MIERKA, MIERKA)

	def pridaj_telo(self):
		self.dlzka += 1
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

	@priUdalosti("KLAVES DOLE")
	def klaves(self, klaves, unicode):
		if self.pauza:
			return
		if klaves == pygame.K_LEFT:
			self.smer = (self.smer - 1 + 4) % 4
		elif klaves == pygame.K_RIGHT:
			self.smer = (self.smer + 1 + 4) % 4
		
	@priZrazke(Cast_tela)
	def zarazka_so_sebou(self, cast):
		if cast.poradie > POCET_BEZPECNYCH_CASTI_TELA:
			self.svet.nastalaUdalost("smrt")

	@priUdalosti("PAUZA")
	def pauzuj(self):
		self.pauza = not self.pauza

class Stena(Vec):
	"""Obycajny obdlznik... Po naraze nasleduje smrt."""
	def nastav(self,x1,y1,x2,y2):
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

class Jedlo(Obrazok):
	"""Upravy staty a posle svetu spravu, nech sa vygeneruje dalsie.
	   NORMAL, SPEED, LIFE, IMMORTALITY, FAT"""
	def nove_miesto(self):
		self.x = random.randrange(SIRKA)
		self.y = random.randrange(VYSKA)

	def nastav(self,typ):
		self.typ = typ

		if typ == "NORMAL":
			self.vyprsanie = INF
		else:
			self.vyprsanie = self.svet.cas + DLZKA_ZJAVENIA		

		if typ == "NONE":
			pass
		else:
			self.nastavSubor("obr/"+typ+"c.png")

		self.nove_miesto()
		self.miesto_vlavo=self.miesto_vpravo=self.miesto_dole=self.miesto_hore = 10
			
	def krok(self):
		if self.svet.cas > self.vyprsanie: 
			self.znic()

	@priZrazke(Had)
	def zrazka_s_jedlom(self, had):
		self.svet.nastalaUdalost(self.typ)
		self.znic()
		
	@priZrazke(Stena)
	def zrazka_jedla_so_stenou(self, stena):
		self.nove_miesto()			

class Horny_panel(Vec):
	def nastav(self):
		self.body = Text(self.svet)
		self.body.x = 55
		self.body.y = 15
		self.body.z = 100
		self.body.zarovnajX = 0
		self.body.zarovnajY = 0
		self.body.aktualizuj(velkost = 30, farba = Farba(50,50,50))


		self.zivoty = Text(self.svet)
		self.zivoty.x = SIRKA - 150
		self.zivoty.y = 15
		self.zivoty.z = 100
		self.zivoty.zarovnajX = 0
		self.zivoty.zarovnajY = 0
		self.zivoty.aktualizuj(velkost = 30, farba = Farba(50,50,50))

		self.lvl = Text(self.svet)
		self.lvl.x = SIRKA/2
		self.lvl.y = 15
		self.lvl.z = 100
		self.lvl.zarovnajX = 0.5
		self.lvl.zarovnajY = 0
		#self.lvl.aktualizuj(text = "Level "+str(self.svet.level), velkost = 30)

	def krok(self):
		self.body.aktualizuj(text = "Body: "+str(self.svet.skore))
		if IMMORTALITY != 0:
			self.zivoty.aktualizuj(text = "Nesmrtelny")
		else:
			self.zivoty.aktualizuj(text = "Zivoty: "+str(self.svet.zivoty))

class Pozadie(Obrazok):
	def nastav(self,subor):
		self.z = -100
		self.nastavSubor(subor)
		self.zarovnajY = 0
		self.zarovnajX = 0
		
#STRUKTURA LEVELOV

class Player_data():
	def __init__(self,nazov_suboru):
		self.dlzka  = 0
		self.smer   = 1
		self.level  = 0
		self.skore  = 0
		self.zivoty = 0
		with open(nazov_suboru,"r") as file: 
			parametre = []
			for line in file:
				parametre.append(int(line))	
			self.dlzka, self.smer, self.level, self.skore, self.zivoty = parametre

class Level_data():
	def __init__(self,nazov_suboru):
		self.max_score = 0
		self.bonusy = []
		self.steny = []		#stvorice
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
	def nastav(self,save):
		#RESET GLOBALNYCH "PREMENNYCH"
		global RYCHLOST
		RYCHLOST = 5
		global IMMORTALITY
		IMMORTALITY = 0
		global MIERKA
		MIERKA = 15

		#HRAC
		hrac = Player_data(save)
		self.level = hrac.level
		self.dlzka = hrac.dlzka
		self.skore = hrac.skore
		self.zivoty = hrac.zivoty

		#HAD
		self.hadik = Had(self, SIRKA/2, VYSKA/2, self.dlzka, 1)
		self.hadik.pauza = True
		self.nacasujUdalost(1000, "PAUZA") 
		
		#LEVEL
		level = Level_data("level"+str(self.level)+".data")
		self.max_score = level.max_score
		for x1,y1,x2,y2 in level.steny:
			st = Stena(self, x1, y1, x2, y2)
		jedlo = Jedlo(self, "NORMAL")
		self.bonusy = level.bonusy
		self.terajsi_bonus = 0

		#UI
		panel = Horny_panel(self)
		pozadie = Pozadie(self, "obr/level"+str(self.level)+".png")
			
	def uloz_hraca(self, save):
		with open(save,"w") as f: 
			f.write(str(self.hadik.dlzka) +"\n") 
			f.write(str(self.hadik.smer) + "\n")
			f.write(str(self.level) + "\n")
			f.write(str(self.skore) + "\n")
			f.write(str(self.zivoty) + "\n")
				
	def krok(self):
		if self.skore >= self.max_score:
			self.level += 1
			self.uloz_hraca("quicksave.data")
			hra.nahradSvet(Level("quicksave.data"))
	
	@priUdalosti("KLAVES DOLE")
	def klaves(self,klaves,unicode):
		if klaves == pygame.K_ESCAPE:
			hra.zatvorSvet()
		elif klaves == pygame.K_SPACE:
			self.nastalaUdalost("PAUZA")

	@priUdalosti("smrt")
	def nastala_smrt(self):
		global IMMORTALITY
		if IMMORTALITY != 0:
			pass
		elif self.zivoty == 0:
			hra.nahradSvet(HighScore(self.skore))
		else:
			self.zivoty -= 1
			self.hadik.x = SIRKA//2
			self.hadik.y = VYSKA//2
			self.hadik.smer = 1
			IMMORTALITY += 1
			self.nacasujUdalost(300, "xIMMORTALITY")

	#Udalosti spustene jedlom
	@priUdalosti("NORMAL")
	def jedlo_NORMAL(self):
		self.skore += 1
		self.hadik.pridaj_telo()
		self.jedlo = Jedlo(self, "NORMAL")
		if random.randrange(2) == 0:
			self.bonus = Jedlo(self, TYPY_JEDLA[self.bonusy[self.terajsi_bonus]])
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
	def nastav(self,x,y,sirka,vyska,text):
		self.x = x
		self.y = y
		self.vyska = vyska
		self.sirka = sirka
		self.napis = text
		self.vysvietene= False

		self.text = Text(self.svet)
		self.text.z = 100
		self.text.x = self.x
		self.text.y = self.y
		self.text.zarovnajX = 0.5
		self.text.zarovnajY = 0.5
		self.text.aktualizuj(self.napis, Farba.CIERNA, 30)
		
	def nakresli(self,kreslic):
		if self.vysvietene:
			kreslic.farba = Farba.CERVENA
		else:
			kreslic.farba = Farba(255, 150, 0)
		kreslic.obdlznik( (-self.sirka/2, -self.vyska/2),self.sirka,self.vyska)	
		
class UvodneMenu(Svet):

	def nastav(self):
		okno.nazov = "Hadik"
		self.banner = Textholder(self, SIRKA/2, 95, SIRKA-80, 90, "HADIIIIIIIIIK")
		self.banner.text.aktualizuj(velkost=50)

		self.nazvy = ["NEW GAME", "HIGH SCORE", "HELP"]
		self.tlacitka = []
		for i in range(len(self.nazvy)):
			self.tlacitka.append( Textholder(self, SIRKA//2, 180+i*(60+10), 240, 60, self.nazvy[i]) )

		self.vybrane = 0
		self.tlacitka[0].vysvietene = True

	@priUdalosti("KLAVES DOLE")
	def klaves(self,klaves,unicode):
		if klaves == pygame.K_ESCAPE:
			hra.zatvorSvet()
		elif klaves == pygame.K_RETURN:
			self.nastalaUdalost( self.tlacitka[self.vybrane].napis )
		elif klaves == pygame.K_UP:
			self.vybrane = (self.vybrane - 1 + len(self.tlacitka)) % len(self.tlacitka)
		elif klaves == pygame.K_DOWN:
			self.vybrane = (self.vybrane + 1 + len(self.tlacitka)) % len(self.tlacitka)
		for t in self.tlacitka: t.vysvietene = False
		self.tlacitka[self.vybrane].vysvietene = True

		
	@priUdalosti("NEW GAME")
	def nova_hra(self):
		hra.otvorSvet(Level("save0.data"))

	@priUdalosti("HIGH SCORE")
	def skore(self):
		hra.otvorSvet(HighScore(-1))

	@priUdalosti("HELP")
	def pomoc(self):
		hra.otvorSvet(Help())

class TextovePole(Textholder):

	@priUdalosti("kurzor")
	def kurzor(self):
		self.napis = self.napis+"|"
		self.svet.nacasujUdalost(500,"xkurzor")
		self.text.aktualizuj(self.napis)

	@priUdalosti("xkurzor")
	def xkurzor(self):
		self.napis = self.napis.strip("|")
		self.svet.nacasujUdalost(500,"kurzor")
		self.text.aktualizuj(self.napis)
		
	@priUdalosti("KLAVES DOLE")
	def klaves(self,klaves,unicode):
		if klaves == pygame.K_RETURN:
			self.svet.nastalaUdalost("ULOZ SKORE")
		elif klaves == pygame.K_BACKSPACE:
			self.napis = self.napis[:-1]
		else: self.napis = self.napis.strip("|") + unicode

		self.text.aktualizuj(self.napis)

class HighScore(Svet):
	def nastav(self, nove):
		self.nove = nove
		self.zaznamy = []		#skore, meno, cas
		with open("highscore.data") as file:
			for line in file:
				self.zaznamy.append(  [ str(x) for x in line.strip().split("|")] )
		for i in range(len(self.zaznamy)):
			Textholder(self, 40, 100 + i*(40+10), 0, 0, self.zaznamy[i][0] )
			Textholder(self, SIRKA/2, 100 + i*(40+10), SIRKA-20, 40, self.zaznamy[i][1] )
			Textholder(self, SIRKA-90, 100 + i*(40+10), 0, 0, self.zaznamy[i][2] )
			
		if nove > int( self.zaznamy[-1][0] ):
			self.pole = TextovePole(self,SIRKA/2,35,SIRKA -20, 50,"sem napis meno")
			Textholder(self,60,35,0,0,"Body: "+str(nove))
			t = [ str(x) for x in time.localtime( time.time() ) ]
			self.cas_string = ":".join(t[3:5])+" "+".".join( (reversed(t[0:3])) )
			Textholder(self,SIRKA-100,35,0,0, self.cas_string) 
			self.nastalaUdalost("kurzor")
		else:
			Textholder(self,SIRKA/2,35,SIRKA -20, 50,"HIGH SCORE ... sien slavy")
			
	@priUdalosti("KLAVES DOLE")
	def klaves(self,klaves,unicode):
		if klaves == pygame.K_ESCAPE:
			hra.zatvorSvet()

	@priUdalosti("ULOZ SKORE")
	def uloz_skore(self):
		self.zaznamy.append([ str(x) for x in [self.nove, self.pole.napis.strip("|"), self.cas_string ]])
		for z in self.zaznamy: z[0] = int(z[0]) 
		self.zaznamy.sort()
		self.zaznamy.reverse()
		self.zaznamy.pop()
		for z in self.zaznamy: z[0] = str(z[0])
		with open("highscore.data","w") as file:
			for z in self.zaznamy:
				file.write("|".join(z)+"\n")
		hra.nahradSvet(HighScore(-1))

class Help(Svet):
	def nastav(self):
		with open("help.data") as file:
			i = 0
			for line in file:
				t = Textholder(self, 30, 30 + i*25,0,0,str(line.strip()))
				t.text.zarovnajX = 0
				t.text.zarovnajY = 0
				t.text.aktualizuj(velkost = 25)
				i += 1

		Textholder(self, SIRKA/2,VYSKA/2,SIRKA-20,VYSKA-20,"")

	@priUdalosti("KLAVES DOLE")
	def klaves(self,klaves,unicode):
		if klaves == pygame.K_ESCAPE:
			hra.zatvorSvet()

#MAIN
okno.sirka = SIRKA
okno.vyska = VYSKA
hra.fps = 60
hra.start(UvodneMenu())
