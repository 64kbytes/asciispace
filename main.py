#!/usr/bin/python
import sys
import math
import config
import gm.gm as GM

opt = sys.argv[1] if len(sys.argv) > 1 else config.RENDER

if opt == '--blocky':
	import uiblocky.render as G
else:
	import uiterminal.render as G
	
VP = None

class Viewport(object):
	def __init__(self, scene, x = 0, y = 0):
		self.scene		= scene
		self.width		= config.VIEWPORT_WIDTH
		self.height		= config.VIEWPORT_HEIGHT
		
		#self.scr_width	= config.SCREEN_WIDTH
		#self.scr_height	= config.SCREEN_HEIGHT
		
		self.map_size	= config.MAP_SIZE
		self.x			= x
		self.y			= y
		self.offset_x	= 0
		self.offset_y	= 0
		#keep track of viewport xy beetween zoom in/out
		self.zoom		= 0
		self.stack		= [None for i in range(self.scene.max_zoom)]
		
	def get_screen_offset(self):
		return (self.x + self.offset_x, self.y + self.offset_y)
		
	def get_map_offset(self):
		return (self.offset_x, self.offset_y)
		
	def screen_to_map(self, x, y):
		ofx, ofy = self.get_screen_offset()
		if x - ofx < 0: 
			mx = 0 
		else:
			mx = x - ofx
		if y - ofy < 0: 
			my = 0 
		else: 
			my = y - ofx 
		return (mx, my)
		
	def screen_to_viewport(self, x, y):
		return (self.x - x, self.y - y)
		
	def map_to_viewport(self, x, y):
		ofx, ofy = self.get_map_offset()
		return (x - ofx, y - ofy)
		
	def move_to(self, x, y):
		x,y = self.map_to_viewport(x, y)
	
		if x < 0:
			x = self.x
		elif (x + self.width) > self.map_size - 1:
			x = self.map_size - self.width
			 
		if y < 0:
			y = self.y
		elif (y + self.width) > (self.map_size - 1):
			y = self.map_size - self.width
		
		self.offset_x = x
		self.offset_y = y
		
	def move(self, x, y, z):
		x,y = self.map_to_viewport(x, y)
		self.move_to(self.offset_x + x, self.offset_y + y)
		return True
		
	def center_on_map(self):
		self.offset_x = (self.map_size / 2) - self.width / 2
		self.offset_y = (self.map_size / 2) - self.height / 2
		
	def center_at(self, x, y):
		x,y = self.map_to_viewport(x, y)
		cx = x - int(self.width / 2)
		cy = y - int(self.height / 2)
				
		self.move_to(cx, cy)
		
	def is_at_edge(self, x, y):
	
		at_edge = dict.fromkeys(('N','E','S','W'), False)
		if y == 0: 
			at_edge['N'] = True
		if x == self.width: 
			at_edge['E'] = True
		if y == self.height:
			at_edge['S'] = True
		if x == 0:
			at_edge['W'] = True
		return at_edge
		
	#def is_at_screen_edge(self, x, y):
	#	return self.is_at_edge(x - self.offset_x - 1, y - self.offset_y - 1, self.width, self.height)
		
	def is_leaving(self, x, y, boundary = 10):
		px,py = self.map_to_viewport(x, y)
	
		leaving_x = ((px > (self.width - boundary)) and (self.offset_x < self.width - 1)) or ((px < boundary) and self.offset_x > 0)
		leaving_y = ((py > (self.height - boundary)) and (self.offset_y < self.height - 1)) or ((py < boundary) and self.offset_y > 0)
						
		return (leaving_x, leaving_y)
		
	def zoom_in(self, pos, f):
		if self.scene.zoom_in((pos[0] + self.offset_x, pos[1] + self.offset_y), f):
			#store current viewport xy
			self.stack[self.zoom] = (self.offset_x, self.offset_y)
			self.zoom += 1
			self.center_on_map()
					
	def zoom_out(self):
		if self.scene.zoom_out():
			self.zoom -= 1
			#restore previous viewport xy
			self.offset_x, self.offset_y = (self.stack[self.zoom][0], self.stack[self.zoom][1])
			
			
def exit():
	G.cleanup()
	quit()
	
def init():
	global VP
	GM.init()
	G.init()
	
	VP = Viewport(GM.get_region(), 10, 10)
	#VP.center_at(GM.EGO.x, GM.EGO.y)
	#VP.move_to(0, 0)
	VP.center_on_map()
	
	G.intro()
	G.options()

init()

def handle_user_input(ui):
	
	#mouse
	m = G.get_mouse()
	
	if m.lbutton_pressed:
		pos = (m.cx, m.cy)
		VP.zoom_in(pos, 2)
		
	if m.rbutton_pressed:
		VP.zoom_out()
		
	
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
			
			if VP.is_at_edge(GM.EGO.x, GM.EGO.y):
				return
			
			leaving_x, leaving_y = VP.is_leaving(GM.EGO.x, GM.EGO.y)					
			dx = xyz[0] if leaving_x else 0
			dy = xyz[1] if leaving_y else 0
			dz = xyz[2]
			
			VP.move(dx, dy, dz)
	
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
