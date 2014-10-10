#!/usr/bin/python
import config
import gm.gm as GM
import uiterminal.render as G

def exit():
	G.cleanup()
	
def init():
	# invert keyboard map. Better for code
	config.KEYBOARD_MAP = dict([[v,k] for k,v in config.KEYBOARD_MAP.items()])
	
	GM.init()
	G.init()
	G.intro()
	G.options()

init()

def handle_user_input(ui):
	ev = config.KEYBOARD_MAP.get(ui, None)
	
	xyz = (0,0,0)
	
	if ev is None: 
		return False
	elif ev == 'UP':	xyz = (0, -1, 0)
	elif ev == 'DOWN':	xyz = (0, 1, 0)
	elif ev == 'LEFT':	xyz = (-1, 0, 0)
	elif ev == 'RIGHT':	xyz = (1, 0, 0)

	GM.move_ego(xyz)
		
while True:

	ui = G.read()

	if ui == 'q':
		break

	handle_user_input(ui)	
	
	ss = GM.snapshot()
	
	G.cycle(ss)


exit()