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

def map_compute_fov(x0, y0, light_walls = False, radius = 10):
	global FOV_MAP, SIGHT_MAP
	SIGHT_MAP = [[0 for y in range(config.MAP_HEIGHT)] for x in range(config.MAP_WIDTH)]
	#raytrace
	for x in range(config.MAP_WIDTH):
		line = get_line(x0, y0, x, 0)
		for square in line:
			if distance((x0, y0), (square[0], square[1])) > radius:
				break		
			if FOV_MAP[square[0]][square[1]] < 1:
				if light_walls:
					SIGHT_MAP[square[0]][square[1]] = 1					
				break
			
			SIGHT_MAP[square[0]][square[1]] = 1
			
	for y in range(config.MAP_HEIGHT):
		line = get_line(x0, y0, config.MAP_WIDTH, y)
		for square in line:
			if distance((x0, y0), (square[0], square[1])) > radius:
				break		
			if FOV_MAP[square[0]][square[1]] < 1:
				if light_walls:
					SIGHT_MAP[square[0]][square[1]] = 1					
				break
			
			SIGHT_MAP[square[0]][square[1]] = 1
			
	for x in range(config.MAP_WIDTH):
		line = get_line(x0, y0, x, config.MAP_HEIGHT)
		for square in line:
			if distance((x0, y0), (square[0], square[1])) > radius:
				break		
			if FOV_MAP[square[0]][square[1]] < 1:
				if light_walls:
					SIGHT_MAP[square[0]][square[1]] = 1					
				break
			
			SIGHT_MAP[square[0]][square[1]] = 1
	
	for y in range(config.MAP_HEIGHT):
		line = get_line(x0, y0, 0, y)
		for square in line:
			if distance((x0, y0), (square[0], square[1])) > radius:
				break		
			if FOV_MAP[square[0]][square[1]] < 1:
				if light_walls:
					SIGHT_MAP[square[0]][square[1]] = 1					
				break
			
			SIGHT_MAP[square[0]][square[1]] = 1


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
	clear(snapshot)
	world = snapshot['world']
	
	if not snapshot['ego'].is_updated:
		map_compute_fov(snapshot['ego'].x, snapshot['ego'].y, True, 20)
	
	board = [[0 for y in range(config.MAP_WIDTH)] for x in range(config.MAP_HEIGHT)]
		
	for x in range(config.MAP_WIDTH):
		for y in range(config.MAP_HEIGHT):
			if SIGHT_MAP[x][y] == 1:
				if world[x][y].block_sight:
					board[y][x] = unichr(0x2588)
				else:
					board[y][x] = '.'
			else:
				board[y][x] = ' '
				
	board[snapshot['ego'].y][snapshot['ego'].x] = '@'
					
	for y in range(config.MAP_HEIGHT):
		print ''.join(board[y])
		
	

	return True
	   
def cleanup():
	clear()
	    
