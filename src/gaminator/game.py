#  -*- coding: utf-8 -*-

import pygame
from .window import okno
from .color import Farba


class _Game:

    def __init__(self):
        self._end = False
        self._screen = None
        self._worlds = []
        self._world_changes = []
        self.fps = 60
        pass

    def koniec(self):
        self._end = True

    def otvorSvet(self, svet):
        self._world_changes.append((1, svet))

    def nahradSvet(self, svet):
        self._world_changes.append((0, svet))

    def zatvorSvet(self):
        self._world_changes.append((-1, None))

    def start(self, svet):
        self.otvorSvet(svet)
        self._loop()

    def _loop(self):

        pygame.init()
        okno.aplikuj()
        self._screen = pygame.display.get_surface()

        clock = pygame.time.Clock()

        while not self._end:

            self._handle_world_changes()
            okno.aplikuj()

            if not self._worlds:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.koniec()
                elif event.type == pygame.VIDEORESIZE:
                    okno._height = event.h
                    okno._width = event.w
                elif event.type == pygame.KEYDOWN:
                    self._worlds[-1].nastalaUdalost(
                        "KLAVES DOLE", event.key, event.unicode)
                elif event.type == pygame.KEYUP:
                    self._worlds[-1].nastalaUdalost(
                        "KLAVES HORE", event.key)

            self._screen.fill(Farba.BIELA)


            self._worlds[-1]._tick()

            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit()

    def _handle_world_changes(self):
        for action, world in self._world_changes:
            if self._worlds:
                self._worlds[-1]._deactivate()
            if action in [-1, 0] and self._worlds:
                self._worlds.pop().znicVsetko()
            if action in [0, 1]:
                self._worlds.append(world)
            if self._worlds:
                self._worlds[-1]._activate()
        self._world_changes = []

hra = _Game()