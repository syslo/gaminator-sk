#  -*- coding: utf-8 -*-

""" GAMINATOR

PyGame Extension
"""

__author__ = "KSP"

from collections import defaultdict
import pygame
import color

##############
### EVENTS ###
##############

class EventEmitter(object):

    def __init__(self):
        self.listeners = []

    def register(self, instance, f):
        self.listeners.append((instance, f))

    def emit(self, *args, **kw_args):
        for instance, f in self.listeners:
            f(instance, *args, **kw_args)


class NamedEventEmitter(object):

    def __init__(self):
        self.emitters = defaultdict(EventEmitter)

    def register(self, instance, f, name):
        self.emitters[name].register(instance, f)

    def emit(self, name, *args, **kw_args):
        self.emitters[name].emit(*args, **kw_args)

global_named_emitter = NamedEventEmitter()


class CollisionEventEmitter(object):

    def __init__(self):
        self.emitters = defaultdict(lambda: defaultdict(EventEmitter))

    def class_list_for(self, instance):
        return list(self.emitters[instance].keys())

    def register(self, instance, f, *classes):
        for cls in classes:
            self.emitters[instance][cls].register(instance, f)

    def emit(self, obj1, obj2):
        self.emitters[obj1][obj2.__class__].emit(obj2)

global_collision_emitter = CollisionEventEmitter()


class _EventAwareType(type):

    def __init__(cls, name, bases, dct):
        cls._listening_to = defaultdict(list)
        for k in dct:
            cls._new_attribute(dct[k])

    def __setattr__(cls, key, value):
        cls._new_attribute(value)
        return super(_EventAwareType, cls).__setattr__(key, value)

    def _new_attribute(cls, value):
        if hasattr(value, '__call__') and hasattr(value, '_callback_to'):
            for emitter, keys, kw_keys in value._callback_to:
                cls._listening_to[emitter].append((value, keys, kw_keys))

    def __call__(cls, *args, **kw_args):
        instance = super(_EventAwareType, cls).__call__(*args, **kw_args)
        for emitter in cls._listening_to:
            for f, keys, kw_keys in cls._listening_to[emitter]:
                emitter.register(instance, f, *keys, **kw_keys)
        return instance


def _register_emitter_to_function(f, emitter, *keys, **kw_keys):
    if hasattr(f, '_callback_to'):
        f._callback_to.append((emitter, keys, kw_keys))
    else:
        f._callback_to = [(emitter, keys, kw_keys)]


########################
### Public interface ###
########################

Farba = color.Farba()

CIERNA   = (   0,   0,   0)
BIELA    = ( 255, 255, 255)
MODRA    = (   0,   0, 255)
ZELENA   = (   0, 255,   0)
CERVENA  = ( 255,   0,   0)

def spusti_ked_nastane(udalost):
    def decorator(f):
        _register_emitter_to_function(f, global_named_emitter, udalost)
        return f
    return decorator


def spusti_pri_zrazke_s(*modely):
    def decorator(f):
        _register_emitter_to_function(f, global_collision_emitter, *modely)
        return f
    return decorator


class Model(object):

    __metaclass__ = _EventAwareType

    def __init__(self, svet):
        self.svet = svet
        self.miesto_hore = 0
        self.miesto_dole = 0
        self.miesto_vpravo = 0
        self.miesto_vlavo = 0
        self.x = 0
        self.y = 0
        self.nastav_sa()

    def nastav_sa(self):
        pass

    def nakresli_sa(self, platno, obrazovka):
        pass

    def urob_krok(self):
        pass


class Svet(object):

    __metaclass__ = _EventAwareType

    def __init__(self):
        self.modely = defaultdict(list)
        self.udalosti = []
        self.nastav_sa()

    def nastav_sa(self):
        pass

    def urob_krok(self):
        pass

    def novy_model(self, cls):
        instance = cls(self)
        self.modely[instance.__class__].append(instance)
        return instance

    def cas(self):
        return pygame.time.get_ticks()

    def nastala_udalost(self, udalost, *args, **kwargs):
        self.udalosti.append((udalost, args, kwargs))

    def _tick(self, screen):

        # Handle events
        events = self.udalosti
        self.udalosti = []
        for event, args, kwargs in events:
            global_named_emitter.emit(event, *args, **kwargs)


        # Do steps
        self.urob_krok()
        for cls in self.modely:
            for model in self.modely[cls]:
                model.urob_krok()

        # Handle collisions
        for cls1 in self.modely:
            for model1 in self.modely[cls1]:
                classes = global_collision_emitter.class_list_for(model1)
                for cls2 in classes:
                    for model2 in self.modely[cls2]:
                        if (
                            model1.y + model1.miesto_vpravo >
                            model2.y - model2.miesto_vlavo
                            and
                            model2.y + model2.miesto_vpravo >
                            model1.y - model1.miesto_vlavo
                            and
                            model1.x + model1.miesto_dole >
                            model2.x - model2.miesto_hore
                            and
                            model2.x + model2.miesto_dole >
                            model1.x - model1.miesto_hore
                        ):
                            global_collision_emitter.emit(model1, model2)

        # Repaint
        for cls in self.modely:
            for model in self.modely[cls]:
                model.nakresli_sa(pygame.draw, screen)


def spusti(cls):

    pygame.init()

    world = cls()

    size = (400, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Gaminator version 0")

    #Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()

    # Loop as long as done == False
    while not done:

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

        screen.fill(BIELA)

        world._tick(screen)

        pygame.display.flip()
        clock.tick(60)

    # Be IDLE friendly
    pygame.quit()




