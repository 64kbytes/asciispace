import libtcodpy as ltc
import config as cfg

VIEW = {
	'Ego': {
		'fcolor': ltc.green,
		'bcolor': ltc.BKGND_NONE 
	},
	'NPC': {
		'fcolor': ltc.yellow,
		'bcolor': ltc.purple 
	}
}

def render(con, gm):
	
	color_dark_wall = ltc.Color(0, 0, 100)
	color_dark_ground = ltc.Color(50, 50, 150)

	for y in range(cfg.MAP_HEIGHT):
		for x in range(cfg.MAP_WIDTH):
			wall = gm.world[x][y].block_sight
			if wall:
				ltc.console_set_char_background(con, x, y, color_dark_wall, ltc.BKGND_SET )
			else:
				ltc.console_set_char_background(con, x, y, color_dark_ground, ltc.BKGND_SET )
		
	for cha in gm.cast:
		typ = cha.attr['type']
		ltc.console_set_default_foreground(con, VIEW[typ]['fcolor'])
		ltc.console_set_char_background(con, cha.x, cha.y, VIEW[typ]['bcolor'], ltc.BKGND_SET )
		ltc.console_put_char(con, cha.x, cha.y, '@', VIEW[typ]['bcolor'])
	
	ltc.console_blit(con, 0, 0, cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT, 0, 0, 0)
	
def render_ui(con, msg):
    ltc.console_set_default_foreground(con, ltc.white)
    ltc.console_print_ex(con, 1, 0, ltc.BKGND_NONE, ltc.LEFT, msg)
	
def clear(con, gm):
	for cha in gm.cast:
		ltc.console_put_char(con, cha.x, cha.y, ' ', ltc.BKGND_NONE)
		
		
con = None
mouse = None
key = None

def init():
	pass
	""""
	global con, mouse, key, cfg
	w = cfg.SCREEN_WIDTH
	h = cfg.SCREEN_HEIGHT
	ltc.sys_set_fps(cfg.FPS)
	
	#FONT_LAYOUT_ASCII_INCOL : characters in ASCII order, code 0-15 in the first column
	#FONT_LAYOUT_ASCII_INROW : characters in ASCII order, code 0-15 in the first row
	#FONT_LAYOUT_TCOD : simplified layout. See examples below.
	#FONT_TYPE_GREYSCALE
	
	ltc.console_set_custom_font(cfg.TILE_SET, ltc.FONT_LAYOUT_ASCII_INROW | ltc.FONT_TYPE_GREYSCALE)
	ltc.console_init_root(w, h, cfg.TITLE, False)
	con = ltc.console_new(w, h)
	mouse = ltc.Mouse()
	key = ltc.Key()
	
	gm.init(cfg)
	"""
	
	
def look_tile():
    global con, mouse
    #return a string with the names of all objects under the mouse
    (x, y) = (mouse.cx, mouse.cy)
    names = [obj.name for obj in gm.cast
		if obj.x == x and obj.y == y and True]
    names = ', '.join(names)
    render_ui(con, names)
	
def handle_ui():
	global key, mouse
		
	# special keys
	#key = ltc.console_check_for_keypress()
	if key.vk == ltc.KEY_ENTER and key.lalt:
		ltc.console_set_fullscreen(not ltc.console_is_fullscreen())
	elif key.vk == ltc.KEY_ESCAPE:
		return True
	
	dx = dy = 0
	
	# ego movement
	if ltc.console_is_key_pressed(ltc.KEY_UP): dy = -1
	if ltc.console_is_key_pressed(ltc.KEY_DOWN): dy = 1
	if ltc.console_is_key_pressed(ltc.KEY_LEFT): dx = -1
	if ltc.console_is_key_pressed(ltc.KEY_RIGHT): dx = 1
		
	gm.ego.move((dx, dy, 0))
	
	
init()

while not ltc.console_is_window_closed():
	break
	""""
	ltc.console_clear(con)
	
	ltc.sys_check_for_event(ltc.EVENT_KEY_PRESS | ltc.EVENT_MOUSE, key, mouse)
	
	
	look_tile()
	
	#clear(con, gm)

	exit = handle_ui()
	
	if exit:
		break
		
	render(con, gm)
	ltc.console_flush()
	"""



