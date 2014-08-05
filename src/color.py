import pygame

#pisat malym

trans = {
	"cervena": "red",
	"modra": "blue",
	"biela": "white",
	"zelena": "green",
	"cierna": "black",
}


class Farba ():
	"""Wrapper k pygame.color.Color

	Farba().CERVENA == Farba()("cervena") == pygame.color.Color("red")
	"""


	def __init__ (self, trans = trans):
		self.trans = trans
		self.eng_names = sorted (pygame.color.THECOLORS.keys())
		self.svk_names = sorted(trans.keys())

	def __call__ (self, *params):
		if len (params) == 1 and params[0] in self.trans:
			params = (self.trans[params[0]], )

		return pygame.color.Color (*params)

	def __getattr__ (self, name):
		if name.isupper() and (name.lower() in self.svk_names or name.lower() in self.eng_names):
			return self(name.lower())

		raise AttributeError (name)

	def slovenske_mena (self):
		return self.svk_names

	def anglicke_mena (self):
		return self.eng_names