#  -*- coding: utf-8 -*-


class Farba(object):

    def __init__(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    def _tuple(self):
        return (
            max(min(self.r, 255), 0),
            max(min(self.g, 255), 0),
            max(min(self.b, 255), 0)
        )

    def __len__(self):
        return 3

    def __getitem__(self, item):
        return self._tuple()[item]

    def __mul__(self, other):
        return Farba(self.r * other, self.g * other, self.b * other)

    def __add__(self, other):
        return Farba(self.r + other.r, self.g + other.g, self.b + other.b)

    def __rmul__(self, other):
        return self * other

    def zmixuj(self, druha, pomer=1):
        return self * (1/(1.0+pomer)) + druha * (pomer/(1.0+pomer))

Farba.CIERNA = Farba(0, 0, 0)
Farba.BIELA = Farba(255, 255, 255)
Farba.MODRA = Farba(0, 0, 255)
Farba.ZELENA = Farba(0, 255, 0)
Farba.CERVENA = Farba(255, 0, 0)
Farba.ZLTA = Farba(255, 255, 0)







