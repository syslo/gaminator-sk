#  -*- coding: utf-8 -*-

from collections import defaultdict


class EventRegistration(object):

    def __init__(self, emitter, target, fname, keys, kw_keys):
        self.target = target
        self.fname = fname
        self.deregistrator = emitter.register(self, *keys, **kw_keys)

    def __call__(self, *args, **kw_args):
        getattr(self.target, self.fname, lambda: None)(*args, **kw_args)

    def deregister(self):
        self.deregistrator.deregister(self)


class _MultiDeregistrator(object):

    def __init__(self, deregistrators=None):
        if not deregistrators:
            deregistrators = []
        self.deregistrators = deregistrators

    def deregister(self, registration):
        for deregistrator in self.deregistrators:
            deregistrator.deregister(registration)

    def add(self, deregistrator):
        self.deregistrators.append(deregistrator)


class EventEmitter(object):

    def __init__(self):
        self.listeners = set()

    def register(self, registration):
        self.listeners.add(registration)
        return self

    def deregister(self, registration):
        self.listeners.discard(registration)

    def emit(self, *args, **kw_args):
        for registration in list(self.listeners):
            registration(*args, **kw_args)


class NamedEventEmitter(object):

    def __init__(self):
        self.emitters = defaultdict(EventEmitter)

    def register(self, registration, name):
        return self.emitters[name].register(registration)

    def emit(self, name, *args, **kw_args):
        self.emitters[name].emit(*args, **kw_args)

global_named_emitter = NamedEventEmitter()


class CollisionEventEmitter(object):

    def __init__(self):
        self.emitters = defaultdict(lambda: defaultdict(EventEmitter))

    def class_list_for(self, instance):
        return list(self.emitters[instance].keys())

    def register(self, registration, *classes):
        deregistrator = _MultiDeregistrator()
        for cls in classes:
            deregistrator.add(
                self.emitters[registration.target][cls].register(registration))
        return deregistrator

    def emit(self, obj1, cls, obj2):
        self.emitters[obj1][cls].emit(obj2)

global_collision_emitter = CollisionEventEmitter()


class EventAwareType(type):

    def __init__(cls, name, bases, dct):
        super(EventAwareType, cls).__init__(name, bases, dct)
        cls._listening_to = defaultdict(list)
        for k in dct:
            cls._new_attribute(k, dct[k])

    def __setattr__(cls, key, value):
        cls._new_attribute(key, value)
        return super(EventAwareType, cls).__setattr__(key, value)

    def _new_attribute(cls, key, value):
        if hasattr(value, '__call__') and hasattr(value, 'hooked_emitters'):
            for emitter, keys, kw_keys in value.hooked_emitters:
                cls._listening_to[emitter].append((key, keys, kw_keys))
            del value.hooked_emitters

    def __call__(cls, *args, **kw_args):
        instance = super(EventAwareType, cls).__call__(*args, **kw_args)
        instance._emitter_registrations = []
        for super_cls in cls.mro():
            if isinstance(super_cls, EventAwareType):
                super_cls._create_emitter_registrations(
                    instance, instance._emitter_registrations)
        return instance

    def _create_emitter_registrations(cls, instance, res):
        for emitter in cls._listening_to:
            for fname, keys, kw_keys in cls._listening_to[emitter]:
                res.append(
                    EventRegistration(emitter, instance, fname, keys, kw_keys))


def _register_emitter_to_function(f, emitter, *keys, **kw_keys):
    if hasattr(f, 'hooked_emitters'):
        f.hooked_emitters.append((emitter, keys, kw_keys))
    else:
        f.hooked_emitters = [(emitter, keys, kw_keys)]


def priUdalosti(udalost):
    def decorator(f):
        _register_emitter_to_function(f, global_named_emitter, udalost)
        return f
    return decorator


def priZrazke(*modely):
    def decorator(f):
        _register_emitter_to_function(f, global_collision_emitter, *modely)
        return f
    return decorator
