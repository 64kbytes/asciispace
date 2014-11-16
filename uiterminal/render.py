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

def trunc(f, n):
	'''Truncates/pads a float f to n decimal places without rounding'''
	slen = len('%.*f' % (n, f))
	return str(f)[:slen]
				
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
	
def handle_user_input(ui, VP, GM):
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
   
def render(VP, snapshot):
	clear()
	
	region	= snapshot['region']
	ego		= snapshot['ego']
	cast	= snapshot['cast']
	terrain	= region.get_terrain()
	fov		= region.get_fov()
	
	radius = 10
	
	#recompute FOV if needed (the player moved or something)
	if not ego.is_updated or fov is None:
		fov = region.update_fov(ego.x, ego.y, radius)
		ego.is_updated = True
	
	board = [[' ' for y in range(config.SCREEN_WIDTH)] for x in range(config.SCREEN_HEIGHT)]
	
	#ego fov origin	
	ox = ego.x - radius
	oy = ego.y - radius
	
	#viewport origin
	ovx = VP.x
	ovy = VP.y
	
	#explored
	for y in range(config.SCREEN_HEIGHT):
		vy = y + ovy
		if (vy > region.length - 1) or vy < 0:
			break
		for x in range(config.SCREEN_WIDTH):
			vx = x + ovx
			if (vx > region.length - 1) or vx < 0:
				break

			if terrain[vy][vx].explored:
				if terrain[vy][vx].block_sight:
					board[y][x] =  unichr(0x2591) #shaded full block #circle unichr(0x0A66)
				else:
					board[y][x] =  ' '
			
			# in FOV area
			if (ox < vx < ox + (radius * 2)) and (oy < vy < oy + (radius * 2)):
				# in FOV
				if fov[vy - oy][vx - ox] > 0:
					terrain[vy][vx].explored = True
					if terrain[vy][vx].block_sight:
						board[y][x] = unichr(0x2588) #full block
					else:
						board[y][x] = unichr(0x02D1) #small dot
								
	board[ego.y - ovy][ego.x - ovx] = '@'
					
	for y in range(config.SCREEN_HEIGHT):
		print ''.join(board[y])
			
	return True
	   
def cleanup():
	clear()
	    
