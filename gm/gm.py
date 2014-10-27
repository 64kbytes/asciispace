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
	REGION = wrl.Region(config.MAP_WIDTH, config.MAP_HEIGHT)
	
def create_ego():
	global EGO
	EGO = ent.Ego(wrl.PLAYER_XYZ)
	CAST.append(EGO)
	
def create_npc():
	pass
	#CAST.append(ent.NPC((2, 2, 0)))
	
def get_ego():
	return EGO
	
def get_region():
	return REGION
	
def snapshot():			
	return {
		'region':	REGION,
		'cast':		CAST,
		'ego':		EGO	
	}
	
def move_ego(xyz):
	nx = EGO.x + xyz[0]
	ny = EGO.y + xyz[1]

	if nx < config.MAP_WIDTH and ny < config.MAP_HEIGHT and nx >= 0 and ny >= 0:	
		if not REGION.terrain[ny][nx].blocked:
			EGO.move(xyz)
			return True
	return False
	
def cycle():
	pass

