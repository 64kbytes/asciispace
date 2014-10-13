import config
import entities as ent
import world as wrl

EGO = None
CAST = []
WORLD = []

def init():
	create_world()
	create_npc()
	create_ego()	

def create_world():
	global WORLD
	WORLD = wrl.make_map(config.MAP_WIDTH, config.MAP_HEIGHT, WORLD)

def create_ego():
	global EGO
	EGO = ent.Ego(wrl.PLAYER_XYZ)
	CAST.append(EGO)
	
def create_npc():
	CAST.append(ent.NPC((2, 2, 0)))
	
def snapshot():
	global WORLD
	return {
		'world':	WORLD,
		'cast':		CAST,
		'ego':		EGO		
	}
	
def move_ego(xyz):
	nx = EGO.x + xyz[0]
	ny = EGO.y + xyz[1]

	if nx < config.MAP_WIDTH and ny < config.MAP_HEIGHT:	
		if not WORLD[nx][ny].blocked:
			EGO.move(xyz)
	
def cycle():
	pass

