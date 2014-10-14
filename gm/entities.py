import text.words as wrd

wrd.Words.init()

def all_subclasses(cls):
	return cls.__subclasses__() + [g for s in cls.__subclasses__()
		for g in all_subclasses(s)]

class Entity(object):
	def __init__(self):
		pass

class Race(object):
	pass
	
class Human(Race):
	pass

class Character(Entity):
	def __init__(self, xyz):
		self.x, self.y, self.z = xyz
		self.name = wrd.Words.randomName(1)
		self.is_updated = None
		super(Character, self).__init__()
	
	def move(self, delta):
		self.x += delta[0]
		self.y += delta[1]
		self.z += delta[2]
		
class Ego(Character):
	def __init__(self, xyz):
		super(Ego, self).__init__(xyz)

class NPC(Character):
	def __init__(self, xyz):
		super(NPC, self).__init__(xyz)

class Race(object):
	pass

class Human(Race):
	pass
class Robot(Race):
	pass
class Alien(Race):
	pass


	
	
