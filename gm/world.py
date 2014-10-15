import random

#parameters for dungeon generator
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
PLAYER_XYZ = None
LIGHTS = []

class Tile:
	#a tile of the map and its properties
	def __init__(self, blocked, block_sight = None, explored = False):
		self.blocked = blocked
		self.explored = explored
		#by default, if a tile is blocked, it also blocks sight
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight
		 
class Rect:
	#a rectangle on the map. used to characterize a room.
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h
		
	def center(self):
		center_x = (self.x1 + self.x2) / 2
		center_y = (self.y1 + self.y2) / 2
		return (center_x, center_y)

	def intersect(self, other):
		#returns true if this rectangle intersects with another one
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
			self.y1 <= other.y2 and self.y2 >= other.y1)

def create_room(room, world):
	#go through the tiles in the rectangle and make them passable
	for x in range(room.x1 + 1, room.x2):
		for y in range(room.y1 + 1, room.y2):
			world[x][y].blocked = False
			world[x][y].block_sight = False
			
	return world
	
def create_h_tunnel(x1, x2, y, world):
	#horizontal tunnel. min() and max() are used in case x1>x2
	for x in range(min(x1, x2), max(x1, x2) + 1):
		world[x][y].blocked = False
		world[x][y].block_sight = False
	return world
	
def create_v_tunnel(y1, y2, x, world):
	#vertical tunnel
	for y in range(min(y1, y2), max(y1, y2) + 1):
		world[x][y].blocked = False
		world[x][y].block_sight = False
	return world

def make_map(width, height, world):
	global PLAYER_XYZ
	#fill map with "blocked" tiles
	world = [[ Tile(True)
		for y in range(height) ]
			for x in range(width) ]

	rooms = []
	num_rooms = 0

	for r in range(MAX_ROOMS):
		#random width and height
		w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
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
			world = create_room(new_room, world)
			(new_x, new_y) = new_room.center()
			LIGHTS.append((new_x, new_y))
			if num_rooms == 0:
				PLAYER_XYZ = (new_x, new_y, 0)
			else:
				(prev_x, prev_y) = rooms[num_rooms-1].center()
				if random.randint(0, 1) == 1:
					world = create_h_tunnel(prev_x, new_x, prev_y, world)
					world = create_v_tunnel(prev_y, new_y, new_x, world)
				else:
					world = create_v_tunnel(prev_y, new_y, prev_x, world)
					world = create_h_tunnel(prev_x, new_x, new_y, world)
			rooms.append(new_room)
			num_rooms += 1
	return world