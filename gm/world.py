#color_dark_wall = libtcod.Color(0, 0, 100)
#color_dark_ground = libtcod.Color(50, 50, 150)

class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
 
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
		
def create_room(room, world):
    #go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            world[x][y].blocked = False
            world[x][y].block_sight = False

def make_map(w, h, world):
 
    #fill map with "blocked" tiles
    world = [[ Tile(True)
        for y in range(h) ]
            for x in range(w) ]
 
    #create two rooms
    room1 = Rect(20, 15, 10, 15)
    room2 = Rect(50, 15, 10, 15)
    create_room(room1, world)
    create_room(room2, world)
    
    return world
