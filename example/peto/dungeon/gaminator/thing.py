#  -*- coding: utf-8 -*-

from .event import EventAwareType
import pygame

class Vec(object):

    __metaclass__ = EventAwareType

    def __init__(self, svet, *args, **kwargs):
        self._world = svet
        self.miestoHore = 0
        self.miestoDole = 0
        self.miestoVpravo = 0
        self.miestoVlavo = 0
        self._mask = None
        self._destroyed = False
        self.x = 0
        self.y = 0
        self._z = 0
        self.nastav(*args, **kwargs)
        svet._register_thing(self)

    @property
    def svet(self):
        return self._world

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._world._resort_things = True
        self._z = value

    def nastav(self):
        pass

    def nakresli(self, kreslic):
        pass

    def krok(self):
        pass

    def prekryva(self, vec):
        prienik_x = (
            max(self.x - self.miestoVlavo, vec.x - vec.miestoVlavo),
            min(self.x + self.miestoVpravo, vec.x + vec.miestoVpravo),
        )
        prienik_y = (
            max(self.y - self.miestoHore, vec.y - vec.miestoHore),
            min(self.y + self.miestoDole, vec.y + vec.miestoDole),
        )
        if prienik_x[0] >= prienik_x[1] or prienik_y[0] >= prienik_y[1]:
            return False
        return _prekry_masky(self, vec, prienik_x, prienik_y)
    
    # Vrati vec triedy trieda, do ktorej by narazil, keby sa posunul o posun_x a
    # posun_y, pripadne None, ak nic take nie je.
    # Ak je veci viac, vrati lubovolnu z nich.
    def narazilBySom(self, trieda, posun_x = 0, posun_y = 0):
        temp_x, temp_y = self.x, self.y
        self.x, self.y = self.x + posun_x, self.y + posun_y
        
        for thing in self.svet._things_by_class[trieda]:
            if self != thing and self.prekryva(thing):
                self.x, self.y = temp_x, temp_y
                return thing
        self.x, self.y = temp_x, temp_y
        return None

    def znic(self):
        if self._destroyed:
            return None
        self._destroyed = True
        self._deregister()

    def _deregister(self):
        self._world._deregister_thing(self)
        for registration in self._emitter_registrations:
            registration.deregister()
        self._emitter_registrations = []

# Pre dve veci vyhodnoti, ci sa ich masky prekryvaju
# Maska typu None sa momentalne prekryva so vsetkym

def _prekry_masky(vec1, vec2, prienik_x, prienik_y):
    if vec1._mask == None and vec2._mask == None:
        return True
    if vec1._mask == None:
        vec1, vec2 = vec2, vec1
    if vec2._mask == None:
        prienik = pygame.mask.Mask((prienik_x[1] - prienik_x[0],
                                    prienik_y[1] - prienik_y[0]))
        prienik.fill()
        return prienik.overlap(vec1._mask,
                               (vec1.x - vec1.miestoVlavo - prienik_x[0],
                                vec1.y - vec1.miestoHore - prienik_y[0]));

    return vec2._mask.overlap(vec1._mask,
        (vec1.x - vec1.miestoVlavo - vec2.x + vec2.miestoVlavo,
         vec1.y - vec1.miestoHore - vec2.y + vec2.miestoHore))
