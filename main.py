#!/usr/bin/python
import sys
import config
import gm.gm as GM

opt = sys.argv[1] if len(sys.argv) > 1 else config.RENDER

if opt == '--blocky':
	import uiblocky.render as G
else:
	import uiterminal.render as G
	
VP = None

class Viewport(object):
	def __init__(self, x = 0, y = 0):
		self.scr_width	= config.SCREEN_WIDTH
		self.scr_height	= config.SCREEN_HEIGHT
		self.reg_width	= config.MAP_WIDTH
		self.reg_height	= config.MAP_HEIGHT
		self.x			= x
		self.y			= y
	def move_to(self, x, y):
	
		if x < 0:
			x = 0
		elif x > self.reg_width - 1:
			x = self.reg_width - self.scr_width
			 
		if y < 0:
			y = 0
		elif y > self.reg_height - 1:
			y = self.reg_width - self.scr_width
		
		self.x = x
		self.y = y
		
	def move(self, xyz):
		x,y,z = xyz
		
		if ((self.x + x) < 0 or (self.x + x) > self.reg_width):
			return
		if ((self.y + y) < 0 or (self.y + y) > self.reg_height):
			return
		
		self.x += x
		self.y += y
		
	def center_at(self, x, y):
		cx = x - int(self.scr_width / 2)
		cy = y - int(self.scr_height / 2) 
		self.move_to(cx, cy)
	
	def pos(self, x, y):
		px = x - self.x
		py = y - self.y 
		return (px,py)
		
	def is_leaving(self, x, y):
		boundary = 10
		px,py = self.pos(x, y)	
		return (not ((self.scr_width - boundary) > px > boundary), not (self.scr_height - boundary) > py > boundary)
			
def exit():
	G.cleanup()
	quit()
	
def init():
	global VP
	GM.init()
	G.init()
	
	VP = Viewport()
	VP.center_at(GM.EGO.x, GM.EGO.y)
	
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
		if GM.move_ego(xyz):
			GM.EGO.is_updated = False
			leaving_x, leaving_y = VP.is_leaving(GM.EGO.x, GM.EGO.y)					
			dx = xyz[0] if leaving_x else 0
			dy = xyz[1] if leaving_y else 0
			dz = xyz[2]
			
			VP.move((dx, dy, dz))
	
snapshot = None

while True:
	
	#if snapshot is not None:
	#	G.clear(snapshot)
	
	ui = G.get_keyboard()
	if ui is False:
		break
		
	handle_user_input(ui)
	
	snapshot = GM.snapshot()
	G.render(VP, snapshot)
	
exit()
