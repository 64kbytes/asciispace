import text.words as wrd

wrd.Words.init()

class Entity(object):
	def __init__(self, attr):
		self.attr = attr

class Character(Entity):
	def __init__(self, xyz, attr):
		self.x, self.y, self.z = xyz
		if attr is None:
			attr = {
				'type': self.__class__.__name__
			}
		self.name = wrd.Words.randomName(1)
		super(Character, self).__init__(attr)
	
	def move(self, delta):
		self.x += delta[0]
		self.y += delta[1]
		self.z += delta[2]
		
class Ego(Character):
	def __init__(self, xyz, attr = None):
		super(Ego, self).__init__(xyz, attr)

class NPC(Character):
	def __init__(self, xyz, attr = None):
		super(NPC, self).__init__(xyz, attr)
