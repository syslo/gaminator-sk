from gaminator import *

class Hrac(Model):

    def nastav_sa(self):
        self.miesto_hore = 10
        self.miesto_dole = 10
        self.miesto_vpravo = 10
        self.miesto_vlavo = 10
        self.x = 200
        self.y = 200

    def nakresli_sa(self, kreslic, obrazovka):
        kreslic.ellipse(obrazovka, CIERNA, [self.x-10, self.y-10, 21, 21])

    def urob_krok(self):
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.y -= 5
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.y += 5
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.x += 5
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.x -= 5


class Prepinac(Model):

    def nastav_sa(self):
        self.miesto_hore = 10
        self.miesto_dole = 10
        self.miesto_vpravo = 10
        self.miesto_vlavo = 10
        self.x = 200
        self.y = 200
        self.farba = CERVENA

    def nakresli_sa(self, kreslic, obrazovka):
        kreslic.rect(obrazovka, self.farba, [self.x-10, self.y-10, 21, 21])

    @spusti_pri_zrazke_s(Hrac)
    def prepni_sa(self, hrac):
        if self.farba == CERVENA:
            self.svet.nastala_udalost("modra")
        else:
            self.svet.nastala_udalost("cervena")
        hrac.x = 200
        hrac.y = 200

    @spusti_ked_nastane("cervena")
    def bud_cerveny(self):
        self.farba = CERVENA

    @spusti_ked_nastane("modra")
    def bud_modry(self):
        self.farba = MODRA



class Hra(Svet):

     def nastav_sa(self):
         self.novy_model(Hrac)

         p1 = self.novy_model(Prepinac)
         p1.x += 50
         p2 = self.novy_model(Prepinac)
         p2.x -= 50
         p3 = self.novy_model(Prepinac)
         p3.y -= 50
         p4 = self.novy_model(Prepinac)
         p4.y += 50


spusti(Hra)

