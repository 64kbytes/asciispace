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
	def __init__(self, x = 0, y = 0):
		self.width		= config.VIEWPORT_WIDTH
		self.height		= config.VIEWPORT_HEIGHT		
		self.map_size	= config.MAP_SIZE
		self.x			= x
		self.y			= y
		self.offset_x	= 0
		self.offset_y	= 0
		#keep track of viewport xy beetween zoom in/out
		self.zoom		= 0
		self.stack		= [None for i in range(config.MAX_ZOOM)]
		
	def get_screen_offset(self):
		return (self.x, self.y)
		
	def get_map_offset(self):
		return (self.offset_x, self.offset_y)
		
	def screen_to_map(self, x, y):
		vx, vy = self.get_screen_offset()
		mx, my = self.get_map_offset()			
		return (x + mx - vx, y + my - vy)
		
	def screen_to_viewport(self, x, y):
		return (self.x - x, self.y - y)
		
	def viewport_to_screen(self, x, y):
		return (self.x + x, self.y + y)
		
	def map_to_viewport(self, x, y):
		mx, my = self.get_map_offset()
		return (x + mx, y + my)
		
	def move_to(self, x, y):
		
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
		
	def move(self, dx, dy, z):		
		
		self.move_to(self.offset_x + dx, self.offset_y + dy)
		
		#x,y = self.map_to_viewport(x, y)
		#self.move_to(x, y)
		return True
		
	def center_on_map(self):
		self.offset_x = (self.map_size - self.width) / 2
		self.offset_y = (self.map_size - self.height) / 2
		
	def center_at(self, x, y):
		
		cx = x - int(self.width / 2)
		cy = y - int(self.height / 2)
		
		
				
		self.move_to(cx, cy)
		
	def is_at_viewport_edge(self, x, y):
		at_edge = dict.fromkeys(('N','E','S','W'), False)
		at_edge['N'] = (y - self.offset_y) == 0
		at_edge['E'] = (x - self.offset_x) == self.width - 1
		at_edge['S'] = (y - self.offset_y) == self.height - 1
		at_edge['W'] = (x - self.offset_x) == 0
		return at_edge
		
	#def is_at_screen_edge(self, x, y):
	#	return self.is_at_edge(x - self.offset_x - 1, y - self.offset_y - 1, self.width, self.height)
		
	def is_leaving(self, x, y, boundary = 10):
	
		leaving = dict.fromkeys(('N','E','S','W'), False)
		
		leaving['N'] = ((y - self.offset_y) < boundary) and self.offset_y > 0
		leaving['E'] = ((x - self.offset_x) > (self.width - boundary - 1)) and (self.offset_x < (self.map_size - self.width))
		leaving['S'] = ((y - self.offset_y) > (self.height - boundary - 1)) and (self.offset_y < (self.map_size - self.height))
		leaving['W'] = ((x - self.offset_x) < boundary) and self.offset_x > 0

		return leaving
		
	def zoom_in(self, pos, f):
		pos = self.screen_to_map(pos[0], pos[1])

		if GM.zoom_in(pos, f):
			#store current viewport xy
			self.stack[self.zoom] = (self.offset_x, self.offset_y)
			self.zoom += 1
			
			self.center_at(pos[0], pos[1])
					
	def zoom_out(self):
		if GM.zoom_out():
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
	
	VP = Viewport(5, 10)
	#VP.center_at(GM.EGO.x, GM.EGO.y)
	#VP.move_to(0, 0)
	#VP.center_on_map()
	VP.move_to(0, 0)
	
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
								
			leaving = VP.is_leaving(GM.EGO.x, GM.EGO.y)
								
			dx = xyz[0] if ((leaving['E'] and xyz[0] > 0) or (leaving['W'] and xyz[0] < 0)) else 0
			dy = xyz[1] if ((leaving['N'] and xyz[1] < 0) or (leaving['S'] and xyz[1] > 0)) else 0
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
