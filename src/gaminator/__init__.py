#  -*- coding: utf-8 -*-

""" GAMINATOR

PyGame Extension
"""

__author__ = "KSP"

from .event import priUdalosti, priZrazke
from .color import Farba
from .thing import Vec
from .surface_thing import Obrazok, Animacia, Text
from .world import Svet
from .window import okno
from .game import hra
from .utils import nahodneCislo

# noinspection PyUnresolvedReferences
import pygame

pygame.font.init()












