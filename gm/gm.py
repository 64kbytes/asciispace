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
	EGO = ent.Ego()	
	CAST.append(EGO)
	put_in_map(REGION.get_tile(wrl.PLAYER_XY[0], wrl.PLAYER_XY[1]), EGO)

def put_in_map(tile, entity):
	
	if entity.get_context():
		entity.context.release(entity)

	tile.hold(entity)
	entity.set_context(tile)
	
def set_entities():
	for entity in CAST:
		x,y = REGION.xy_global_to_local((entity.gx, entity.gy))
		REGION.terrain[y][x].hold(entity)
	
def create_npc():
	pass
	#CAST.append(ent.NPC((2, 2, 0)))
	
def get_ego():
	return EGO
	
def zoom_in(xy, f):
	if REGION.zoom_in(xy, f) is True:
		for entity in CAST:
			entity.x,entity.y = REGION.xy_global_to_local((entity.gx, entity.gy))
		return True
	return False

def zoom_out():
	if REGION.zoom_out() is True:
		for entity in CAST:
			entity.x,entity.y = REGION.xy_global_to_local((entity.gx, entity.gy))			
		return True
	return False
	
def get_region():
	return REGION

def get_cast_in_region():
	visible_cast = []
	for char in CAST:
		if (REGION.bounds['W'][0] <= char.gx <= REGION.bounds['E'][0]) and (REGION.bounds['N'][1] <= char.gy <= REGION.bounds['S'][1]):
			visible_cast.append(char)
	return visible_cast
	
def get_snapshot():
	return {
		'region':	REGION,
		'cast':		get_cast_in_region(),
		'ego':		EGO	
	}
	
def move_ego(xyz):

	# distance of each ego step its a function of map scale unit
	u = REGION.get_map_scale_unit()
	nx = EGO.x + xyz[0]
	ny = EGO.y + xyz[1]
	nz = EGO.z + xyz[2]

	if nx < REGION.length and ny < REGION.length and nx >= 0 and ny >= 0:
		tile = REGION.terrain[ny][nx]
		if not tile.blocked:
			EGO.move(xyz, u)
			EGO.z = int(tile.z)
			return True
	return False
	
def cycle():
	pass

