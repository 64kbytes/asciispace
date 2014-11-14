import text.words as wrd

wrd.Words.init()

def all_subclasses(cls):
	return cls.__subclasses__() + [g for s in cls.__subclasses__()
		for g in all_subclasses(s)]

class Entity(object):
	def __init__(self):
		self.context = None
		pass
	
	def set_context(self, tile):
		self.context = tile
		self.xyz(tile.get_xy_global(), tile.get_xyz_local())
		
	def get_context(self):
		return self.context

class Race(object):
	pass
	
class Human(Race):
	pass

class Character(Entity):
	def __init__(self, l_xyz, g_xy):
		
		self.x, self.y, self.z = l_xyz if l_xyz is not None else [None for i in range(3)]
		self.gx, self.gy = g_xy if g_xy is not None else [None for i in range(2)]
		
		self.name = wrd.Words.randomName(1)
		self.is_updated = None
		super(Character, self).__init__()
		
	def xyz(self, g_xy, l_xyz):
		self.x, self.y, self.z = l_xyz
		self.gx, self.gy = g_xy
	
	def move(self, delta, scale_unit = 1):
		self.x += delta[0]
		self.y += delta[1]
		self.z += delta[2]
		self.gx += delta[0] * scale_unit
		self.gy += delta[1] * scale_unit
		
class Ego(Character):
	def __init__(self, g_xy = None, l_xyz = None):
		super(Ego, self).__init__(g_xy, l_xyz)

class NPC(Character):
	def __init__(self, g_xy = None, l_xyz = None):
		super(NPC, self).__init__(g_xy, l_xyz)

class Race(object):
	pass

class Human(Race):
	pass
class Robot(Race):
	pass
class Alien(Race):
	pass


	
	
