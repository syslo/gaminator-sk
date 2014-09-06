#  -*- coding: utf-8 -*-

from .event import EventAwareType
import pygame

class Vec(object):

    __metaclass__ = EventAwareType

    def __init__(self, svet, *args, **kwargs):
        self._world = svet
        self.miesto_hore = 0
        self.miesto_dole = 0
        self.miesto_vpravo = 0
        self.miesto_vlavo = 0
        self._mask = None
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
            max(self.x - self.miesto_vlavo, vec.x - vec.miesto_vlavo),
            min(self.x + self.miesto_vpravo, vec.x + vec.miesto_vpravo),
        )
        prienik_y = (
            max(self.y - self.miesto_hore, vec.y - vec.miesto_hore),
            min(self.y + self.miesto_dole, vec.y + vec.miesto_dole),
        )
        if prienik_x[0] >= prienik_x[1] or prienik_y[0] >= prienik_y[1]:
            return False
        return _prekry_masky(self, vec, prienik_x, prienik_y)

    # nevieme zabepecit, aby nejaka vec nebola znicena viac krat, tak aby sa
    # nezrubala cela hra, dovolime ju deregistrovat len raz
    _destroyed = False
    def znic(self):
        if self._destroyed: return None
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
                               (vec1.x - vec1.miesto_vlavo - prienik_x[0],
                                vec1.y - vec1.miesto_hore - prienik_y[0]));

    return vec2._mask.overlap(vec1._mask,
        (vec1.x - vec1.miesto_vlavo - vec2.x + vec2.miesto_vlavo,
         vec1.y - vec1.miesto_hore - vec2.y + vec2.miesto_hore))
