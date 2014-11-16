import random
import math
from algorithms.fov import *
from algorithms.geometry import *
from algorithms.terrain import *
from debug import *

PLAYER_XY = (0, 0, 0)
LIGHTS = []

class Tile:
	#a tile of the map and its properties
	def __init__(self, blocked, lx, ly, gx, gy, block_sight = None, explored = False):
		self.x = lx
		self.y = ly
		self.z = None
		self.gx = gx
		self.gy = gy
	
		self.blocked = blocked
		self.explored = explored
		self.entities = []
		
		#by default, if a tile is blocked, it also blocks sight
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight
		
	def hold(self, entity):
		entity.set_context(self)
		self.entities.append(entity)
		
	def release(self, entity):
		self.entities.remove(entity)
	
	def get_xyz_local(self):
		return (self.x, self.y, self.z)
		
	def get_xy_global(self):
		return (self.gx, self.gy)
	
	def get_info(self):
		return {
			'xy_local':		(self.x, self.y),
			'xy_global':	(self.gx, self.gy),
			'altitude':		self.z,
			'block_sight':	self.block_sight,
			'block_move':	self.blocked,
			'explored':		self.explored,
			'entities':		self.entities
		}
	
	def copy(self, tile):
		tile.gx = self.gx
		tile.gy = self.gy
		tile.blocked = self.blocked
		tile.block_sight = self.block_sight
		tile.explored = self.explored
		tile.entities = self.entities
		tile.z = self.z
		return tile

class Planet(object):
	
	def __init__(self, size):
		self.name = 'Earth'
		self.neighborhood = dict.fromkeys(('here','NW','N','NE','E','SE','S','SW','W'), None)
		self.neighborhood['here'] = Region(size)
		
	def get_here(self):
		return self.neighborhood['here']

class Region(object):
	max_zoom = 10
	
	def __init__(self, length):
	
		self.length = length
		self.bounds = None
		
		#set planet seed. Needs to be stored later
		#self.seed = random.random()
		self.seed = 123
		
		#parameters for dungeon generator
		self.room_max_size = 10
		self.room_min_size = 6
		self.max_rooms = 160
		self.zoom = 0
		
		#cache stores the entire map at 0 and stacks sectors when zooming in 
		self.cache = [None for i in range(Region.max_zoom + 1)]	
		self.cache[self.zoom] = self.get_empty_region((0, 0))
		self.terrain = self.cache[self.zoom]
	
		self.seed_terrain()
		self.create_terrain(True)
		
		self.set_bounds()
		
		#self.create_dungeon(length, length)		
		self.fov_map = set_fov_map(self.terrain)
		self.fov = None
		
	def xy_global_to_local(self, gxy):
		gx, gy = gxy
		u = self.get_map_scale_unit()		
		return (int(math.floor((gx - self.bounds['W'][0]) / u)), int(math.floor((gy - self.bounds['N'][1]) / u)))
		
	def xy_local_to_global(self, lxy):
		lx, ly, lz = lxy
		u = self.get_map_scale_unit()
		return (lx + self.bounds['W'][0] * u, ly + self.bounds['N'][1] * u)
		
	def get_map_scale_unit(self):
		return int(math.pow(2, Region.max_zoom - self.zoom))

		
	def get_empty_region(self, xy):
		gx, gy = xy
		unit = self.get_map_scale_unit()
		#fill map with "blocked" tiles
		return [[ Tile(False, x, y, gx + x * unit, gy + y * unit)
			for x in range(self.length) ]
				for y in range(self.length) ]
		
	def distance_to_edges(self, x, y):
		pass
		
	def get_bounds(self):
		p = self.square_points(0, 0, self.length-1)
		# unpack
		cx, cy = p['CN']					
		nx, ny = p['N']
		ex, ey = p['E']
		sx, sy = p['S']
		wx, wy = p['W']
		nwx, nwy = p['NW'] 
		nex, ney = p['NE']
		sex, sey = p['SE']
		swx, swy = p['SW']
		# get coordinates
		c = self.get_tile(cx, cy)
		n = self.get_tile(nx, ny)
		e = self.get_tile(ex, ey)
		s = self.get_tile(sx, sy)
		w = self.get_tile(wx, wy)
		nw = self.get_tile(nwx, nwy)
		ne = self.get_tile(nex, ney)
		se = self.get_tile(sex, sey)
		sw = self.get_tile(swx, swy)
		# make dict	
		return {
			'C': (c.gx, c.gy),
			'N': (n.gx, n.gy),
			'E': (e.gx, e.gy),
			'S': (s.gx, s.gy),
			'W': (w.gx, w.gy),
			'NW': (nw.gx, nw.gy),
			'NE': (ne.gx, ne.gy),
			'SE': (se.gx, se.gy),
			'SW': (sw.gx, sw.gy)
		}
	
	def set_bounds(self):
		self.bounds = self.get_bounds()
			
	def get_fov_map(self):
		return self.fov_map
		
	def get_fov(self):
		return self.fov
		
	def get_tile(self, x, y):
		if x < 0 or y < 0:
			raise Exception("Tried to access tile {0}:{1}".format(x, y))
		return self.terrain[y][x]
		
	def get_terrain(self):
		return self.terrain
		
	def update_fov(self, x, y, radius):
		self.fov = map_compute_fov(self.fov_map, x, y, True, radius)
		return self.fov
	
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
		self.terrain[0][0].z = random.uniform(-1.0, 1.0)
		self.terrain[0][-1].z = random.uniform(-1.0, 1.0)
		self.terrain[-1][-1].z = random.uniform(-1.0, 1.0)
		self.terrain[-1][0].z = random.uniform(-1.0, 1.0)
		
	def create_terrain(self, wrap, i = 0, d = 128, h = .5):
	
		sq = int(math.pow(2, i))	#square divisions in this iteration: 1, 2, 4, 8, 16, 32, 64, ...
		ln = (self.length - 1) / sq	#square side length
		
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

				random.seed((self.terrain[nwy][nwx].z + self.terrain[ney][nex].z + self.terrain[sey][sex].z + self.terrain[swy][swx].z))								
				r = random.uniform(-d, d)

				#center										
				if self.terrain[cy][cx].z is None:
					c = (self.terrain[nwy][nwx].z + self.terrain[ney][nex].z + self.terrain[sey][sex].z + self.terrain[swy][swx].z) / 4	
					self.terrain[cy][cx].z = c + r
				#north
				if self.terrain[ny][nx].z is None:
					if nex == (self.length - 1) and self.terrain[ney][0].z is not None and wrap is True:
						n = (self.terrain[cy][cx].z + self.terrain[nwy][nwx].z + self.terrain[ney][0].z) / 3
					else:
						n = (self.terrain[cy][cx].z + self.terrain[nwy][nwx].z + self.terrain[ney][nex].z) / 3
					self.terrain[ny][nx].z = n + r
				#east
				if self.terrain[ey][ex].z is None:
					if ex == (self.length - 1) and self.terrain[ey][0].z is not None and wrap is True:
						e = self.terrain[ey][0].z
					else:
						e = (self.terrain[cy][cx].z + self.terrain[ney][nex].z + self.terrain[sey][sex].z) / 3
					self.terrain[ey][ex].z = e + r
				#south
				if self.terrain[sy][sx].z is None:
					if sex == (self.length - 1) and self.terrain[sey][0].z is not None and wrap is True:
						s = (self.terrain[cy][cx].z + self.terrain[sey][0].z + self.terrain[swy][swx].z) / 3
					else:
						s = (self.terrain[cy][cx].z + self.terrain[sey][sex].z + self.terrain[swy][swx].z) / 3
					self.terrain[sy][sx].z = s + r
				#west
				if self.terrain[wy][wx].z is None:
					w = (self.terrain[cy][cx].z + self.terrain[swy][swx].z + self.terrain[nwy][nwx].z) / 3
					self.terrain[wy][wx].z = w + r
			
				
		i += 1
		self.create_terrain(wrap, i, d, h)
		
	def get_length_zoom_area(self, f):
		return int((self.length - 1) / math.pow(2, f-1))
	
	def zoom_in(self, xy, f):
		if not self.zoom < Region.max_zoom: 
			return False
	
		self.zoom += 1
					
		x0,y0 = xy
		
		# lenght of sector to be zoomed
		l = self.get_length_zoom_area(f)
		s = (self.length - 1) / l

		# centering zoom area
		x0 -= l/2
		y0 -= l/2
		
		# keep zoom area inside defined map
		if x0 < 0: x0 = 0
		if y0 < 0: y0 = 0
		if (x0 + l) > (self.length): x0 = (self.length - 1) - l
		if (y0 + l) > (self.length): y0 = (self.length - 1) - l
			
		# feed new empty region with global coordinates origin
		origin_tile = self.get_tile(x0, y0)
		exp = self.get_empty_region((origin_tile.gx, origin_tile.gy));
		
		# translate small area tiles to wider area
		for y in range(y0, y0+l + 1):
			for x in range(x0, x0+l + 1):
				# translate small zoom area origin to wider map origin
				ox = x - x0
				oy = y - y0
				# tiles present in zoom area are copied to final zoomed map
				# copy method does not copy local coordinates
				cpy = self.terrain[y][x].copy(exp[oy * s][ox * s])
				exp[oy * s][ox * s] = cpy
	
		# store this view
		self.cache[self.zoom] = self.terrain
		
		self.terrain = exp
		
		# fill empty tiles on wide map
		self.create_terrain(False, 0, 128 * (2 / self.zoom), 0.8)
		
		# update region global bounds
		self.set_bounds()
	
		return True

	
	def zoom_out(self):
		if self.zoom == 0:
			return False
		else:
			self.terrain = self.cache[self.zoom]
			self.zoom -= 1
			# update region global bounds
			self.set_bounds()
			return True

