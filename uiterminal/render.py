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
		
	radius = 20
		
	#recompute FOV if needed (the player moved or something)
	if not ego.is_updated or fov is None:
		fov = region.update_fov(ego.x, ego.y, radius)
		ego.is_updated = True
	
	#ego fov origin	
	ox = ego.x - radius
	oy = ego.y - radius
	
	#viewport origin
	ofx, ofy = VP.get_screen_offset()
	ovx, ovy = VP.get_map_offset()
	
	board = [[' ' for y in range(config.SCREEN_WIDTH)] for x in range(config.SCREEN_HEIGHT)]
	
	#explored
	for y in range(VP.height):	
		vy = y + ovy		
		for x in range(VP.width):
			vx = x + ovx
						
			h = int(terrain[vy][vx].z)	
			
			if h < 0:
				board[y][x] =  '~'				
			
			""""
			if terrain[vy][vx].explored:
				if terrain[vy][vx].block_sight:
					board[y][x] =  unichr(0x2591) #shaded full block #circle unichr(0x0A66)
				else:
					board[y][x] =  ' '
			"""

	
			# in FOV area
			if geometry.in_circle(ego.x, ego.y, radius, vx, vy):
				board[y][x] = unichr(0x2588) #full block
				
				""""
				# in FOV
				if fov[vy - oy][vx - ox] > 0:
					terrain[vy][vx].explored = True
					if terrain[vy][vx].block_sight:
						board[y][x] = unichr(0x2588) #full block
					else:
						board[y][x] = unichr(0x02D1) #small dot
				"""
			
	
	chax,chay = snapshot['region'].xy_global_to_local((ego.gx, ego.gy))
								
	board[chay + ofy - ovy][chax + ofx - ovx] = '@'
					
	for y in range(config.SCREEN_HEIGHT):
		print ''.join(board[y])
						
	return True
	   
def cleanup():
	clear()
	    
