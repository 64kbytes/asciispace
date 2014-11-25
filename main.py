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
	def __init__(self, map_size, x = 0, y = 0):
		self.width		= min(config.VIEWPORT_WIDTH, map_size)
		self.height		= min(config.VIEWPORT_HEIGHT, map_size)		
		self.map_size	= config.MAP_SIZE
		self.x			= x
		self.y			= y
		self.offset_x	= 0
		self.offset_y	= 0
		#keep track of viewport xy beetween zoom in/out
		self.zoom		= 0
		self.stack		= [None for i in range(config.MAX_ZOOM)]
		
	def get_screen_offset(self):
		#offset between screen and viewport
		return (self.x, self.y)
		
	def get_map_offset(self):
		#offset between map and viewport 
		return (self.offset_x, self.offset_y)
		
	def screen_to_map(self, x, y):
		#convert xy from screen to map
		vx, vy = self.get_screen_offset()
		mx, my = self.get_map_offset()			
		return (x + mx - vx, y + my - vy)
		
	def screen_to_viewport(self, x, y):
		#convert xy from screen to viewport
		return (self.x - x, self.y - y)
		
	def viewport_to_screen(self, x, y):
		#convert xy from viewport to screen
		return (self.x + x, self.y + y)
		
	def map_to_viewport(self, x, y):
		#convert xy from map to viewport
		mx, my = self.get_map_offset()
		return (x + mx, y + my)
		
	def move_to(self, x, y):
		
		"""
		if x < 0:
			x = self.x
		elif (x + self.width) > self.map_size:
			x = self.map_size - self.width
			 
		if y < 0:
			y = self.y
		elif (y + self.height) > self.map_size:
			y = self.map_size - self.height
		"""
		self.offset_x = x
		self.offset_y = y
		
	def move(self, dx, dy, z):
		self.move_to(self.offset_x + dx, self.offset_y + dy)
		return True
		
	def center_on_map(self):		
		self.offset_x = (self.map_size - self.width) / 2
		self.offset_y = (self.map_size - self.height) / 2
		
	def center_at(self, x, y):
	
		cx = (self.map_size - self.width) / 2
		cy = (self.map_size - self.height) / 2
		
		self.offset_x = cx
		self.offset_y = cy
		
		# at edge. Take in acount viewport w/h != map w/h
		if x < cx:
			self.offset_x = 0
		elif x > (self.map_size - cx):
			self.offset_x = self.map_size - self.width
			
		if y < cy:
			self.offset_y = 0
		elif y > (self.map_size - cy):
			self.offset_y = self.map_size - self.height
		
	def is_leaving(self, x, y, boundary = 10):
		leaving = dict.fromkeys(('N','E','S','W'), False)
	
		#is inside scroll boundary
		in_north_boundary	= ((y - self.offset_y) < boundary)
		in_south_boundary	= ((y - self.offset_y) > (self.height - boundary - 1))
		in_east_boundary	= ((x - self.offset_x) > (self.width - boundary - 1))
		in_west_boundary	= ((x - self.offset_x) < boundary)
		#is at map scroll end
		at_north_map_end	= self.offset_y		<= 0
		at_south_map_end	= (self.offset_y	>= (self.map_size - self.height))
		at_east_map_end		= (self.offset_x	>= (self.map_size - self.width))
		at_west_map_end		= self.offset_x		<= 0
		#leaving condition
		leaving['N'] = in_north_boundary	and not at_north_map_end
		leaving['S'] = in_south_boundary	and not at_south_map_end
		leaving['E'] = in_east_boundary		and not at_east_map_end
		leaving['W'] = in_west_boundary		and not at_west_map_end
		
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
	
	VP = Viewport(GM.get_region().length, 1, 1)
	#VP.center_at(GM.EGO.x, GM.EGO.y)
	#VP.move_to(0, 0)
	#VP.center_on_map()
	VP.move_to(0, 0)
	
	G.intro()
	G.options()

init()

while True:
		
	#if snapshot is not None:
	#	G.clear(snapshot)
	
	ui = G.get_keyboard()
	if ui is False:
		break
		
	G.handle_user_input(ui, VP, GM)
	
	G.set_snapshot(GM.get_snapshot())
	G.render(VP)
	
exit()
