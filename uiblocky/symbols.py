import libtcodpy as ltc
import inspect

# array-like property access
class MetaContainer():
    def __delitem__(self, key):
        self.__delattr__(key)
    def __getitem__(self, key):
        return self.__getattribute__(key)
    def __setitem__(self, key, value):
        self.__setattr__(key, value)

SYMBOL_MAP = {
	'Ego': {
		'char':			'@',
		'front_color':	ltc.green,
		'back_color':	None
	},
	'NPC': {
		'char':			'@',
		'front_color':	ltc.white,
		'back_color':	None
	},
	'Robot': {
		'char':			'&'
	}
}

class Symbol(object, MetaContainer):
	def __init__(self):
		self.char 			= None		
		self.front_color	= None
		self.back_color 	= None

def get_symbol(entity):
	classlist = inspect.getmro(entity.__class__)
	li = list(reversed([cl.__name__ for cl in classlist]))	
	
	sym = Symbol()
	
	for clss in li:
		if clss in SYMBOL_MAP:
			for attr in SYMBOL_MAP[clss]:
				sym[attr] = SYMBOL_MAP[clss][attr]
		
	return sym


	

		
