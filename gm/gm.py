import config
import characters as cha
from world import *

ego = None
cast = []
world = []

def init():
	global world
	create_ego()
	create_npc()
	world = make_map(config.MAP_WIDTH, config.MAP_HEIGHT, world)

def create_ego():
	global ego, cast, world
	ego = cha.Ego((3, 3, 0))
	cast.append(ego)
	
def create_npc():
	global ego, cast, world
	cast.append(cha.NPC((2, 2, 0)))
	
def snapshot():
	global ego
	return {
		'Ego.name': ego.name,
		'Ego.x': ego.x,
		'Ego.y': ego.y,
		'Ego.z': ego.z
	}
	
def move_ego(xyz):
	global ego
	ego.move(xyz)
	
def cycle():
	pass
	
	


