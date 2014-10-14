#!/usr/bin/python
import config
import gm.gm as GM

if config.RENDER == 'libtcod':
	import uiblocky.render as G
else:
	import uiterminal.render as G

def exit():
	G.cleanup()
	quit()
	
def init():	
	GM.init()
	G.init()
	G.set_fov_map(GM.WORLD)
	G.set_light_map(GM.WORLD)
	G.intro()
	G.options()

init()

def handle_user_input(ui):
	
	if ui is None: 
		GM.EGO.is_updated = True if GM.EGO.is_updated is not None else False
		return False
	
	if ui == 'ESCAPE':	exit()

	xyz = (0,0,0)	
	if ui == 'UP':		xyz = (0, -1, 0)
	elif ui == 'DOWN':	xyz = (0, 1, 0)
	elif ui == 'LEFT':	xyz = (-1, 0, 0)
	elif ui == 'RIGHT':	xyz = (1, 0, 0)

	if xyz != (0,0,0):
		GM.EGO.is_updated = False
		GM.move_ego(xyz)
	
snapshot = None
		
while True:

	if snapshot:
		G.clear(snapshot)

	ui = G.get_keyboard()
	if ui is False:
		break
		
	handle_user_input(ui)
	
	snapshot = GM.snapshot()
	G.render(snapshot)
	
exit()
