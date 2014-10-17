import tty, termios, sys
import config
import math

KEYBOARD_MAP = {
	'ESCAPE':	'q',
	'UP':		'w',
	'DOWN':		's',
	'LEFT':		'a',
	'RIGHT':	'd'
}

FOV_MAP = None
SIGHT_MAP = None

#Bresenham
def get_line(x1, y1, x2, y2):
	points = []
	issteep = abs(y2-y1) > abs(x2-x1)
	if issteep:
		x1, y1 = y1, x1
		x2, y2 = y2, x2
	rev = False
	if x1 > x2:
		x1, x2 = x2, x1
		y1, y2 = y2, y1
		rev = True
	deltax = x2 - x1
	deltay = abs(y2-y1)
	error = int(deltax / 2)
	y = y1
	ystep = None
	if y1 < y2:
		ystep = 1
	else:
		ystep = -1
	for x in range(x1, x2 + 1):
		if issteep:
			points.append((y, x))
		else:
			points.append((x, y))
		error -= deltay
		if error < 0:
			y += ystep
			error += deltax
	# Reverse the list if the coordinates were reversed
	if rev:
		points.reverse()
	return points
	
#Pythagoras
def distance(p0, p1):
	dx = p1[0] - p0[0]
	dy = p1[1] - p0[1]
	return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

def set_fov_map(world):
	global FOV_MAP, SIGHT_MAP
	fov_map = [[1 for y in range(config.MAP_HEIGHT)] for x in range(config.MAP_WIDTH)]
	
	for y in range(config.MAP_HEIGHT):
		for x in range(config.MAP_WIDTH):
			if world[x][y].block_sight:
				fov_map[x][y] = 0
			else:
				fov_map[x][y] = 1

	FOV_MAP = fov_map	
	SIGHT_MAP = fov_map
	
def set_light_map(snapshot):
	pass

def map_compute_fov(x0, y0, light_walls = False, radius = 10, fix = True):
	global FOV_MAP, SIGHT_MAP
	
	SIGHT_MAP = [[0 for y in range(radius * 2)] for x in range(radius * 2)]
	
	ox = x0 - radius
	oy = y0 - radius
	
	for q in range(4):
			
		for n in range(radius * 2):
		
			if q == 0:
				line = get_line(x0, y0, ox + n, oy + 0)
			elif q == 1: 
				line = get_line(x0, y0, ox + n, oy + (radius * 2) - 1)
			elif q == 2: 
				line = get_line(x0, y0, ox + 0, oy + n)
			elif q == 3: 
				line = get_line(x0, y0, ox + (radius * 2) - 1, oy + n)
					
			for square in line:
				if (square[0] >= config.MAP_WIDTH) or (square[1] >= config.MAP_HEIGHT) or (square[0] < 0 )or (square[1] < 0):
					break
				
				#artifact fix. Is straight vertical or horizontal
				if n == radius and fix:
					#is horizontal
					if q == 0 or q == 1:
						SIGHT_MAP[square[0] - ox - 1][square[1] - oy] = 1
						SIGHT_MAP[square[0] - ox + 1][square[1] - oy] = 1
					#is vertical
					if q == 2 or q == 3:	
						SIGHT_MAP[square[0] - ox][square[1] - oy + 1] = 1
						SIGHT_MAP[square[0] - ox][square[1] - oy - 1] = 1
				
				
				if FOV_MAP[square[0]][square[1]] < 1:
					if light_walls:
						SIGHT_MAP[square[0] - ox][square[1] - oy] = 1		
					break
				
				SIGHT_MAP[square[0] - ox][square[1] - oy] = 1
				
def init():
	global KEYBOARD_MAP
	KEYBOARD_MAP = dict([[v, k] for k, v in KEYBOARD_MAP.items()])
	sys.stdout.write("\x1b]2;" + config.TITLE + "\x07")
	clear()
	   
def intro():
	pass
	
def options():
	print "Press 'q' to quit"   

def clear(snapshot = None):
	sys.stderr.write("\x1b[2J\x1b[H")
   
def render(snapshot):
	pass
	
def get_keyboard():
   #Returns a single character from standard input
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   
   try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   
   return KEYBOARD_MAP.get(ch, None)
   
def render(snapshot):
	clear()
	world = snapshot['world']
	
	radius = 10
	
	if not snapshot['ego'].is_updated:
		map_compute_fov(snapshot['ego'].x, snapshot['ego'].y, True, radius)
	
	board = [[' ' for y in range(config.MAP_WIDTH)] for x in range(config.MAP_HEIGHT)]
	
	ox = snapshot['ego'].x - radius
	oy = snapshot['ego'].y - radius
	
	#explored
	for x in range(config.MAP_WIDTH):
		for y in range(config.MAP_HEIGHT):
		
			if world[x][y].explored:
				if world[x][y].block_sight:
					board[y][x] =  unichr(0x2591) #shaded full block #circle unichr(0x0A66)
				else:
					board[y][x] =  ' '
			
			# in FOV area
			if (ox < x < ox + (radius * 2)) and (oy < y < oy + (radius * 2)):
				# in FOV
				if SIGHT_MAP[x - ox][y - oy] == 1:
					snapshot['world'][x][y].explored = True
					if world[x][y].block_sight:
						board[y][x] = unichr(0x2588) #full block
					else:
						board[y][x] = unichr(0x02D1) #small dot
				
		
					
	board[snapshot['ego'].y][snapshot['ego'].x] = '@'
					
	for y in range(config.MAP_HEIGHT):
		print ''.join(board[y])
			
			
		
	"""		
	for x in range(radius * 2):
		if (ox + x >= config.MAP_WIDTH) or (ox + x < 0):
			continue
			
		for y in range(radius * 2):
			if oy + y >= config.MAP_HEIGHT or (oy + y < 0):
				continue

			# in FOV
			if SIGHT_MAP[x][y] == 1:
				snapshot['world'][ox + x][oy + y].explored = True
				if world[ox + x][oy + y].block_sight:
					board[oy + y][ox + x] = unichr(0x2588)
				else:
					board[oy + y][ox + x] = '.'
			# out of FOV
			else:
				board[oy + y][ox + x] = '?' 
				
	board[snapshot['ego'].y][snapshot['ego'].x] = '@'
					
	for y in range(config.MAP_HEIGHT):
		print ''.join(board[y])
	"""
		
	

	return True
	   
def cleanup():
	clear()
	    
