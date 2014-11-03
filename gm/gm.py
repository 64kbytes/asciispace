import config
import entities as ent
import world as wrl

EGO = None
CAST = []
REGION = []

def init():
	create_world()
	create_npc()
	create_ego()	

def create_world():
	global REGION
	REGION = wrl.Region(config.MAP_SIZE)
	
def create_ego():
	global EGO
	EGO = ent.Ego(REGION.get_tile(wrl.PLAYER_XY[0], wrl.PLAYER_XY[1]))
	CAST.append(EGO)
	
def create_npc():
	pass
	#CAST.append(ent.NPC((2, 2, 0)))
	
def get_ego():
	return EGO
	
def get_region():
	return REGION

def get_cast_in_region():
	
	visible_cast = []
	
	for char in CAST:
		if (REGION.bounds['W'][0] <= char.x <= REGION.bounds['E'][0]) and (REGION.bounds['N'][1] <= char.y <= REGION.bounds['S'][1]):
			visible_cast.append(char)

	return visible_cast
	
def snapshot():
	return {
		'region':	REGION,
		'cast':		get_cast_in_region(),
		'ego':		EGO	
	}
	
def move_ego(xyz):
	unit = REGION.get_map_scale_unit()
	nx = EGO.x + xyz[0]
	ny = EGO.y + xyz[1]
	
	if nx < REGION.length and ny < REGION.length and nx >= 0 and ny >= 0:	
		if not REGION.terrain[ny][nx].blocked:
			EGO.move(xyz, unit)
			return True
	return False
	
def cycle():
	pass

