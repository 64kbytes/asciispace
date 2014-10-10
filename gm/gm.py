import characters as cha
from world import *

ego = None
cast = []
world = []

def create_ego():
	global ego, cast, world
	ego = cha.Ego((3, 3, 0))
	cast.append(ego)
	
def create_npc():
	global ego, cast, world
	cast.append(cha.NPC((2, 2, 0)))
	
def init(cfg):
	global world
	create_ego()
	create_npc()
	world = make_map(cfg.MAP_WIDTH, cfg.MAP_HEIGHT, world)

