import config
import libtcodpy as ltc
import symbols as sym
import math

#DARK_WALL = ltc.Color(0, 0, 100)
#DARK_GROUND = ltc.Color(50, 50, 150)

DARK_WALL = ltc.black
DARK_GROUND = ltc.black
EXPLORED_WALL = ltc.darkest_grey
EXPLORED_GROUND = ltc.grey

LIGHT_WALL = ltc.Color(130, 110, 50)
LIGHT_GROUND = ltc.Color(200, 180, 50)

CON		= None
UI		= None
MOUSE	= None
KEY		= None
KEYBOARD_MAP = {
	'NONE':			ltc.KEY_NONE,
	'ESCAPE':		ltc.KEY_ESCAPE,
	'UP':			ltc.KEY_UP,
	'DOWN':			ltc.KEY_DOWN,
	'LEFT':			ltc.KEY_LEFT,
	'RIGHT':		ltc.KEY_RIGHT
}
FOV_RECOMPUTE = False
FOV_MAP = None
FOV_ALGO = 0  #default FOV algorithm
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

def init():
	global SYMBOL_MAP, KEYBOARD_MAP, CON, UI, MOUSE, KEY
	
	w = config.SCREEN_WIDTH
	h = config.SCREEN_HEIGHT
	ltc.sys_set_fps(config.FPS)
	ltc.console_set_custom_font(config.TILE_SET, ltc.FONT_TYPE_GREYSCALE | ltc.FONT_LAYOUT_TCOD)
	ltc.console_init_root(w, h, config.TITLE, False)
	
	KEYBOARD_MAP = dict([[v, k] for k, v in KEYBOARD_MAP.items()])
	CON = ltc.console_new(w, h)
	UI = ltc.console_new(w, 10)
	MOUSE = ltc.Mouse()
	KEY = ltc.Key()
		
def intro():
	pass

def options():
	pass

def get_keyboard():
	
	if ltc.console_is_window_closed():
		return False
		
	ltc.sys_check_for_event(ltc.EVENT_KEY_PRESS|ltc.EVENT_MOUSE,KEY,MOUSE)
	
	if KEY.vk == ltc.KEY_ENTER and KEY.lalt:
		ltc.console_set_fullscreen(not ltc.console_is_fullscreen())
		
	for k,v in KEYBOARD_MAP.iteritems():
		if ltc.console_is_key_pressed(k):
			return v

def get_mouse():
	(x, y) = (MOUSE.cx, MOUSE.cy)
	return (x, y)

def clear(snapshot):
	for cha in snapshot['cast']:
		ltc.console_set_char_background(CON, cha.x, cha.y, ltc.BKGND_NONE, ltc.BKGND_SET)
		ltc.console_put_char(CON, cha.x, cha.y, ' ', ltc.BKGND_NONE)

def all_subclasses(cls):
	return cls.__subclasses__() + [g for s in cls.__subclasses__()
		for g in all_subclasses(s)]

def render_UI(snapshot):

	ltc.console_clear(UI)
	
	#return a string with the names of all objects under the MOUSE
	(x, y) = (MOUSE.cx, MOUSE.cy)
	names = [obj.name for obj in snapshot['cast']
		if obj.x == x and obj.y == y and True]
	names = ', '.join(names)
	
	ltc.console_set_default_background(UI, ltc.white)
	ltc.console_set_default_foreground(UI, ltc.black)
	ltc.console_print_ex(UI, 0, 0, ltc.BKGND_NONE, ltc.LEFT, names)
	
	ltc.console_blit(UI, 0, 0, config.SCREEN_WIDTH, 10, 0, 0, 0, 1, .5)

def render(snapshot):

	world = snapshot['world']
	
	#go through all tiles, and set their background color according to the FOV
	for y in range(config.MAP_HEIGHT):
		for x in range(config.MAP_WIDTH):
			visible = ltc.map_is_in_fov(FOV_MAP, x, y)
			wall = world[x][y].block_sight
			explored = world[x][y].explored
			if not visible:
				#it's out of the player's FOV
				if wall:
					if explored:
						ltc.console_set_char_background(CON, x, y, EXPLORED_WALL, ltc.BKGND_SET)
					else:
						ltc.console_set_char_background(CON, x, y, DARK_WALL, ltc.BKGND_SET)
				else:
					if explored:
						ltc.console_set_char_background(CON, x, y, EXPLORED_GROUND, ltc.BKGND_SET)
					else:
						ltc.console_set_char_background(CON, x, y, DARK_GROUND, ltc.BKGND_SET)
			else:
			#it's visible
				world[x][y].explored = True
				if wall:
					ltc.console_set_char_background(CON, x, y, LIGHT_WALL, ltc.BKGND_SET )
				else:
					ltc.console_set_char_background(CON, x, y, LIGHT_GROUND, ltc.BKGND_SET )
	
		
	#recompute FOV if needed (the player moved or something)
	if not snapshot['ego'].is_updated:		
		ltc.map_compute_fov(FOV_MAP, snapshot['ego'].x, snapshot['ego'].y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
		snapshot['ego'].is_updated = True
		
	#render characters
	for cha in snapshot['cast']:
		symbol = sym.get_symbol(cha)
		ltc.console_set_default_foreground(CON, symbol.front_color)
		ltc.console_set_char_background(CON, cha.x, cha.y, symbol.back_color, ltc.BKGND_SET )
		ltc.console_put_char(CON, cha.x, cha.y, symbol.char, ltc.BKGND_SET)
			
	ltc.console_blit(CON, 0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 0, 0, 0)
	
	render_UI(snapshot)
	
	ltc.console_flush()
	
	

def set_fov_map(world):
	global FOV_MAP
	FOV_MAP = ltc.map_new(config.MAP_WIDTH, config.MAP_HEIGHT)
	for y in range(config.MAP_HEIGHT):
		for x in range(config.MAP_WIDTH):
		    ltc.map_set_properties(FOV_MAP, x, y, not world[x][y].block_sight, not world[x][y].blocked)
    
def cleanup():
	global CON
	ltc.console_clear(CON)
	 
