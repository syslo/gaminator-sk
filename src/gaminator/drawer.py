#  -*- coding: utf-8 -*-

from .color import Farba
import pygame

class Kreslic:

    def __init__(self, x=0, y=0, farba=0):
        self.farba = farba
        self.x = x
        self.y = y
        self._surface = pygame.display.get_surface()

    def obdlznik(self, (x, y), sirka, vyska, okraj=0):
        pygame.draw.rect(
            self._surface, self.farba,
            (x + self.x, y + self.y, sirka, vyska), okraj)

    def elipsa(self, (x, y), sirka, vyska, okraj=0):
        pygame.draw.ellipse(
            self._surface, self.farba,
            (x + self.x, y + self.y, sirka, vyska), okraj
        )

    def mnohouholnik(self, body, okraj=0):
        pygame.draw.polygon(
            self._surface, self.farba,
            map(lambda (x, y): (x + self.x, y + self.y), body), okraj
        )

    def ciara(self, (x1, y1), (x2, y2), hrubka=0):
        pygame.draw.line(
            self._surface, self.farba,
            (x1 + self.x, y1 + self.y), (x2 + self.x, y2 + self.y), hrubka
        )

