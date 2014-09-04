#  -*- coding: utf-8 -*-

from collections import defaultdict

import heapq
import pygame

from .event import EventAwareType
from .event import global_collision_emitter, global_named_emitter

from .drawer import Kreslic

class Svet(object):

    __metaclass__ = EventAwareType

    def __init__(self):
        self._things_by_class = defaultdict(set)
        self._things = set()
        self._things_sorted = []
        self._resort_things = True
        self._events = []
        self._actual_time = 0
        self._zero_time = 0
        self.cas = 0
        self.stlacene = None
        self.nastav()

    def _activate(self):
        self._zero_time = pygame.time.get_ticks() - self._actual_time

    def _deactivate(self):
        self._actual_time = pygame.time.get_ticks() - self._zero_time

    def nastav(self):
        pass

    def krok(self):
        pass

    def nastalaUdalost(self, udalost, *args, **kwargs):
        self.nacasujUdalost(0, udalost, *args, **kwargs)

    def nacasujUdalost(self, cas, udalost, *args, **kwargs):
        heapq.heappush(
            self._events, (self._actual_time + cas, udalost, args, kwargs))

    def _register_thing(self, instance):
        for cls in instance.__class__.mro():
            self._things_by_class[cls].add(instance)
        self._resort_things = True
        self._things.add(instance)

    def _deregister_thing(self, instance):
        for cls in instance.__class__.mro():
            self._things_by_class[cls].discard(instance)
        self._resort_things = True
        self._things.remove(instance)

    def _tick(self):

        # Update time
        self._actual_time = pygame.time.get_ticks() - self._zero_time
        self.cas = self._actual_time

        # Update keys
        self.stlacene = pygame.key.get_pressed()

        # Handle events
        events = []
        while self._events and self._events[0][0] <= self._actual_time:
            events.append(heapq.heappop(self._events))
        for _, event, args, kwargs in events:
            global_named_emitter.emit(event, *args, **kwargs)

        # Do steps

        self.krok()
        for thing in list(self._things):
            thing.krok()

        # Handle collisions
        collisions = []
        for thing1 in self._things:
            for cls2 in global_collision_emitter.classes_for(thing1):
                if cls2 in self._things_by_class:
                    for thing2 in self._things_by_class[cls2]:
                        if thing1.prekryva(thing2):
                            collisions.append((thing1, cls2, thing2))
        for thing1, cls2, thing2 in collisions:
            global_collision_emitter.emit(thing1, cls2, thing2)

        # Repaint
        if self._resort_things:
            self._things_sorted = sorted(self._things, key=lambda x: x._z)
            self._resort_things = False
        for thing in self._things_sorted:
            thing.nakresli(Kreslic(x=thing.x, y=thing.y))


