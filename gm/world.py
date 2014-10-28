import random
import math
from algorithms.fov import *
from algorithms.geometry import *
from algorithms.terrain import *

PLAYER_XYZ = (20, 39, 0)
LIGHTS = []

class Tile:
	#a tile of the map and its properties
	def __init__(self, blocked, x, y, block_sight = None, explored = False):
		self.x = x
		self.y = y
		self.height = None
		self.seed = None
		self.blocked = blocked
		self.explored = explored
		self.connections = '0000'
		#by default, if a tile is blocked, it also blocks sight
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight

class Planet(object):
	def __init__(self):
		self.name = 'Earth'

class Region(object):
	max_zoom = 10
	
	def __init__(self, width, height):
	
		self.width = width
		self.height = height
		self.cache = [None for i in range(Region.max_zoom + 1)]
		self.seed = random.random()
		
		#parameters for dungeon generator
		self.room_max_size = 10
		self.room_min_size = 6
		self.max_rooms = 160
		self.zoom = 0
					
		self.cache[self.zoom] = self.get_empty_region(0, 0, width, height)
		self.terrain = self.cache[self.zoom]
		
		self.seed_terrain()
		self.create_terrain(True)
		
		#self.create_dungeon(width, height)		
		self.fov_map = set_fov_map(self.terrain)
		self.fov = None

		
	def get_empty_region(self, x0, y0, width, height):
		#fill map with "blocked" tiles
		return [[ Tile(False, x0 + int(x * math.pow(2, Region.max_zoom - self.zoom)), y0 + int(y * math.pow(2, Region.max_zoom - self.zoom)))
			for x in range(width) ]
				for y in range(height) ]
		
	def get_fov_map(self):
		return self.fov_map
		
	def get_fov(self):
		return self.fov
		
	def get_terrain(self):
		return self.terrain
		
	def update_fov(self, x, y, radius):
		self.fov = map_compute_fov(self.fov_map, x, y, True, radius)
		return self.fov
	
	def create_dungeon(self, width, height):
		global PLAYER_XYZ
		
		rooms = []
		num_rooms = 0
	
		for r in range(self.max_rooms):
			#random width and height
			w = random.randint(self.room_min_size, self.room_max_size)
			h = random.randint(self.room_min_size, self.room_max_size)
			#random position without going out of the boundaries of the map
			x = random.randint(0, width - w - 1)
			y = random.randint(0, height - h - 1)

			#"Rect" class makes rectangles easier to work with
			new_room = Rect(x, y, w, h)

			#run through the other rooms and see if they intersect with this one
			failed = False
			for other_room in rooms:
				if new_room.intersect(other_room):
					failed = True
					break
		    
			if not failed:
				self.create_room(new_room)
				(new_x, new_y) = new_room.center()
				LIGHTS.append((new_x, new_y))
				if num_rooms == 0:
					PLAYER_XYZ = (new_x, new_y, 0)
				else:
					(prev_x, prev_y) = rooms[num_rooms-1].center()
					if random.randint(0, 1) == 1:
						self.create_h_tunnel(prev_x, new_x, prev_y)
						self.create_v_tunnel(prev_y, new_y, new_x)
					else:
						self.create_v_tunnel(prev_y, new_y, prev_x)
						self.create_h_tunnel(prev_x, new_x, new_y)
				rooms.append(new_room)
				num_rooms += 1
				
	def create_room(self, room):
		#go through the tiles in the rectangle and make them passable
		for y in range(room.y1 + 1, room.y2):
			for x in range(room.x1 + 1, room.x2):
				self.terrain[y][x].blocked = False
				self.terrain[y][x].block_sight = False
	
	def create_h_tunnel(self, x1, x2, y):
		#horizontal tunnel. min() and max() are used in case x1>x2
		for x in range(min(x1, x2), max(x1, x2) + 1):
			self.terrain[y][x].blocked = False
			self.terrain[y][x].block_sight = False
	
	def create_v_tunnel(self, y1, y2, x):
		#vertical tunnel
		for y in range(min(y1, y2), max(y1, y2) + 1):
			self.terrain[y][x].blocked = False
			self.terrain[y][x].block_sight = False
	
	def square_points(self, x, y, length):
		return {
			'N': (x + length / 2, y),
			'E': (x + length, y + length / 2),
			'S': (x + length / 2, y + length),
			'W': (x, y + length / 2),
			'NW': (x,y),
			'NE': (x + length, y), 
			'SE': (x + length, y + length), 
			'SW': (x, y + length), 
			'CN': (x + length / 2, y + length / 2)
		}
			
	def seed_terrain(self):
		random.seed(self.seed)
		self.terrain[0][0].height = random.uniform(-1.0, 1.0)
		self.terrain[0][-1].height = random.uniform(-1.0, 1.0)
		self.terrain[-1][-1].height = random.uniform(-1.0, 1.0)
		self.terrain[-1][0].height = random.uniform(-1.0, 1.0)
		
	def zoom_in(self, pos, f):
		if not self.zoom < Region.max_zoom: 
			return False
	
		self.zoom += 1
					
		x0,y0 = pos
		l = int((self.width - 1) / math.pow(2, f-1))
		s = (self.width - 1) / l

		x0 -= l/2
		y0 -= l/2
		
		if x0 < 0: x0 = 0
		if y0 < 0: y0 = 0
		if (x0 + l) > (self.width - 1): x0 = (self.width - 1) - l
		if (y0 + l) > (self.height - 1): y0 = (self.height - 1) - l
				
				
		nx0, ny0 = (self.terrain[y0][x0].x, self.terrain[y0][x0].y)
				
		exp = self.get_empty_region(nx0, ny0, self.width, self.height);
	
		for y in range(y0, y0+l + 1):
			for x in range(x0, x0+l + 1):
				ox = x - x0
				oy = y - y0

				exp[oy * s][ox * s] = self.terrain[y][x]
	
		self.terrain = exp
		self.create_terrain(False, 0, 128 * (1 / self.zoom), 0.8)
		self.cache[self.zoom] = self.terrain
	
	def zoom_out(self):
		if self.zoom == 0:
			return False
		else:
			self.zoom -= 1
			self.terrain = self.cache[self.zoom]
			return True										
	
	def create_terrain(self, wrap, i = 0, d = 128, h = .5):
	
		sq = int(math.pow(2, i))	#square divisions in this iteration: 1, 2, 4, 8, 16, 32, 64, ...
		ln = (self.width - 1) / sq	#square side length
		
		if not ln > 1:
			return

		d = d * math.pow(2, -h)
					
		for y in range(sq):
			for x in range(sq):
				p = self.square_points(x * ln, y * ln, ln)	
				#coordinates
				cx, cy = p['CN']					
				nx, ny = p['N']
				ex, ey = p['E']
				sx, sy = p['S']
				wx, wy = p['W']
				nwx, nwy = p['NW'] 
				nex, ney = p['NE']
				sex, sey = p['SE']
				swx, swy = p['SW']

				random.seed((self.terrain[nwy][nwx].height + self.terrain[ney][nex].height + self.terrain[sey][sex].height + self.terrain[swy][swx].height))								
				r = random.uniform(-d, d)

				#center										
				if self.terrain[cy][cx].height is None:
					c = (self.terrain[nwy][nwx].height + self.terrain[ney][nex].height + self.terrain[sey][sex].height + self.terrain[swy][swx].height) / 4	
					self.terrain[cy][cx].height = c + r
				#north
				if self.terrain[ny][nx].height is None:
					if nex == (self.width - 1) and self.terrain[ney][0].height is not None and wrap is True:
						n = (self.terrain[cy][cx].height + self.terrain[nwy][nwx].height + self.terrain[ney][0].height) / 3
					else:
						n = (self.terrain[cy][cx].height + self.terrain[nwy][nwx].height + self.terrain[ney][nex].height) / 3
					self.terrain[ny][nx].height = n + r
				#east
				if self.terrain[ey][ex].height is None:
					if ex == (self.width - 1) and self.terrain[ey][0].height is not None and wrap is True:
						e = self.terrain[ey][0].height
					else:
						e = (self.terrain[cy][cx].height + self.terrain[ney][nex].height + self.terrain[sey][sex].height) / 3
					self.terrain[ey][ex].height = e + r
				#south
				if self.terrain[sy][sx].height is None:
					if sex == (self.width - 1) and self.terrain[sey][0].height is not None and wrap is True:
						s = (self.terrain[cy][cx].height + self.terrain[sey][0].height + self.terrain[swy][swx].height) / 3
					else:
						s = (self.terrain[cy][cx].height + self.terrain[sey][sex].height + self.terrain[swy][swx].height) / 3
					self.terrain[sy][sx].height = s + r
				#west
				if self.terrain[wy][wx].height is None:
					w = (self.terrain[cy][cx].height + self.terrain[swy][swx].height + self.terrain[nwy][nwx].height) / 3
					self.terrain[wy][wx].height = w + r
			
				
		i += 1
		self.create_terrain(wrap, i, d, h)

