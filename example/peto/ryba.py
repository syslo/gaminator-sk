import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'src')))

from gaminator import *

okno.celaObrazovka()

class Hra(Svet):

     def nastav(self):
         pass

hra.start(Hra())

