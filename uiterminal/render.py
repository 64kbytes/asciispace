import tty, termios, sys
import config

KEYBOARD_MAP = {
	'ESCAPE':	'q',
	'UP':		'w',
	'DOWN':		's',
	'LEFT':		'a',
	'RIGHT':	'd'
}

#delete
def set_fov_map(arg):
	pass
def set_light_map(arg):
	pass
#delete - end of block


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
	
	board = [[0 for y in range(config.MAP_WIDTH)] for x in range(config.MAP_HEIGHT)]
		
	for x in range(config.MAP_WIDTH):
		for y in range(config.MAP_HEIGHT):
			if world[x][y].block_sight:
				board[y][x] = unichr(0x2588)
			else:
				board[y][x] = ' '
				
	board[snapshot['ego'].y][snapshot['ego'].x] = '@'
					
	for y in range(config.MAP_HEIGHT):
		print ''.join(board[y])
		
	

	return True
	   
def cleanup():
	clear()
	    
