import tty, termios, sys
import config
from algorithms import *
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
				
def init():
	global KEYBOARD_MAP
	KEYBOARD_MAP = dict([[v, k] for k, v in KEYBOARD_MAP.items()])
	sys.stdout.write("\x1b]2;" + config.TITLE + "\x07")
	clear()
	   
def intro():
	pass
	
def options():
	print "UP: w\nDOWN: s\nLEFT: a\nRIGHT: d\nPress 'q' to quit\nPress any key"   

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
	world = snapshot['world'].terrain
	fov = snapshot['world'].get_fov()
	
	radius = 10
	
	if not snapshot['ego'].is_updated:
		fov = snapshot['world'].update_fov(snapshot['ego'].x, snapshot['ego'].y, radius)
	
	board = [[' ' for y in range(config.MAP_WIDTH)] for x in range(config.MAP_HEIGHT)]
	
	ox = snapshot['ego'].x - radius
	oy = snapshot['ego'].y - radius
	
	#explored
	for y in range(config.MAP_HEIGHT):
		for x in range(config.MAP_WIDTH):
		
			if world[y][x].explored:
				if world[y][x].block_sight:
					board[y][x] =  unichr(0x2591) #shaded full block #circle unichr(0x0A66)
				else:
					board[y][x] =  ' '
			
			# in FOV area
			if (ox < x < ox + (radius * 2)) and (oy < y < oy + (radius * 2)):
				# in FOV
				if fov[y - oy][x - ox] > 0:
					world[y][x].explored = True
					if world[y][x].block_sight:
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
	    
