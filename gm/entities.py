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
	def __init__(self, lxy, gxy):
		self.x, self.y = lxy
		self.gx, self.gy = gxy
		self.z = 0
		
		self.name = wrd.Words.randomName(1)
		self.is_updated = None
		super(Character, self).__init__()
	
	def move(self, delta, scale_unit = 1):
		self.x += delta[0]
		self.y += delta[1]
		self.z += delta[2]
		self.gx += delta[0] * scale_unit
		self.gy += delta[1] * scale_unit
		
class Ego(Character):
	def __init__(self, tile):
		lxy = tile.get_xy_local()
		gxy = tile.get_xy_global()
		super(Ego, self).__init__(lxy, gxy)

class NPC(Character):
	def __init__(self, xyz):
		super(NPC, self).__init__(lxy, gxy)

class Race(object):
	pass

class Human(Race):
	pass
class Robot(Race):
	pass
class Alien(Race):
	pass


	
	
