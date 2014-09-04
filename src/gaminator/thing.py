#  -*- coding: utf-8 -*-

from .event import EventAwareType


class Vec(object):

    __metaclass__ = EventAwareType

    def __init__(self, svet):
        self._world = svet
        self.svet = svet
        self.miesto_hore = 0
        self.miesto_dole = 0
        self.miesto_vpravo = 0
        self.miesto_vlavo = 0
        self.x = 0
        self.y = 0
        self._z = 0
        self.nastav()
        svet._register_thing(self)

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
        return (
            self.x + self.miesto_vpravo >
            vec.x - vec.miesto_vlavo
            and
            vec.x + vec.miesto_vpravo >
            self.x - self.miesto_vlavo
            and
            self.y + self.miesto_dole >
            vec.y - vec.miesto_hore
            and
            vec.y + vec.miesto_dole >
            self.y - self.miesto_hore
        )

    def znic(self):
        self._deregister()

    def _deregister(self):
        self._world._deregister_thing(self)
        for registration in self._emitter_registrations:
            registration.deregister()
        self._emitter_registrations = []

