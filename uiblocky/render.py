import config
import libtcodpy as ltc
import symbols as sym
import math
from algorithms.fov import *
from algorithms.geometry import in_circle

DARK_WALL = ltc.grey
DARK_GROUND = ltc.black
EXPLORED_WALL = ltc.black
EXPLORED_GROUND = ltc.darkest_grey * .5

LIGHT_WALL = ltc.Color(130, 110, 50)
LIGHT_GROUND = ltc.Color(200, 180, 50)

SNAPSHOT		= None
CON				= None
UI				= None
MOUSE			= None
KEY				= None
KEYBOARD_MAP	= {
	'NONE':			ltc.KEY_NONE,
	'ESCAPE':		ltc.KEY_ESCAPE,
	'UP':			ltc.KEY_UP,
	'DOWN':			ltc.KEY_DOWN,
	'LEFT':			ltc.KEY_LEFT,
	'RIGHT':		ltc.KEY_RIGHT
}

idx = [ 0, 10, 50, 100, 255 ] # indexes of the keys
col = [ 
		ltc.Color( 255, 255, 153 ), 
		ltc.Color( 102, 204, 0 ),
		ltc.Color( 153, 76, 0 ), 
		ltc.Color( 102, 51, 0 ),  
		ltc.Color(255,255,255) ] # colors : black, red, white
land_colors = ltc.color_gen_map(col, idx)

idx = [ 0, 255 ] # indexes of the keys
col = [ ltc.Color( 153, 255, 255 ), ltc.Color( 0, 25, 51 ) ] # colors : black, red, white
sea_colors = ltc.color_gen_map(col, idx)

def init():
	global SYMBOL_MAP, KEYBOARD_MAP, CON, UI, MOUSE, KEY
	w = config.SCREEN_WIDTH
	h = config.SCREEN_HEIGHT
	ltc.sys_set_fps(config.FPS)
	
	#ltc.console_set_custom_font(config.TILE_SET, ltc.FONT_LAYOUT_ASCII_INROW | ltc.FONT_TYPE_GREYSCALE, 16, 16)
	ltc.console_set_custom_font(config.TILE_SET, ltc.FONT_LAYOUT_TCOD | ltc.FONT_TYPE_GREYSCALE, 32, 8)	
	ltc.console_init_root(w, h, config.TITLE, False)
	
	KEYBOARD_MAP = dict([[v, k] for k, v in KEYBOARD_MAP.items()])
	CON = ltc.console_new(w, h)
	UI = ltc.console_new(w, h)
	ltc.console_set_key_color(UI, ltc.purple)
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
	return MOUSE

def clear():
	global SNAPSHOT
	for cha in SNAPSHOT['cast']:
		ltc.console_set_char_background(CON, cha.x, cha.y, ltc.BKGND_NONE, ltc.BKGND_SET)
		ltc.console_put_char(CON, cha.x, cha.y, ' ', ltc.BKGND_NONE)

def handle_user_input(ui, VP, GM):
	
	#mouse
	m = get_mouse()
	
	if m.lbutton_pressed:
		pos = (m.cx, m.cy)
		VP.zoom_in(pos, 2)
		
	if m.rbutton_pressed:
		VP.zoom_out()
		
	
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

def render_UI(VP):
	global SNAPSHOT

	ltc.console_clear(UI)
	
	#return a string with the names of all objects under the MOUSE
	(x, y) = (MOUSE.cx, MOUSE.cy)
	
	lx, ly = VP.screen_to_map(x, y)
		
	if lx < 0 or ly < 0:
		return
	
	names = [obj.name + " | G({0}:{1}) | L({2}:{3})".format(obj.gx, obj.gy, obj.x, obj.y) for obj in SNAPSHOT['cast']
		if obj.x == lx and obj.y == ly and True]
		
	names = ' | ' + ', '.join(names)
		
	if lx < SNAPSHOT['region'].length and ly < SNAPSHOT['region'].length:
	
		tile = SNAPSHOT['region'].get_tile(lx, ly).get_info()
		tgx, tgy = tile['xy_global']
		tlx, tly = tile['xy_local']
	
		info = "G({0}:{1}) | L({2}:{3}) | Z: {4}".format(tgx, tgy, tlx, tly, int(tile['altitude'])) + names		
		
	else: info = '-'
	
	ltc.console_set_default_background(UI, ltc.BKGND_NONE)
	ltc.console_set_default_foreground(UI, ltc.white)
	ltc.console_print_ex(UI, 0, 0, ltc.BKGND_SET, ltc.LEFT, info)
	ltc.console_set_default_background(UI, ltc.purple)
	
	zoomx = 50
	zoomy = 40
	
	for zy in range(zoomy):
		for zx in range(zoomx):	
			ltc.console_set_char_background(UI, zx + (x - zoomx / 2), zy + (y - zoomy / 2), ltc.BKGND_LIGHTEN, ltc.BKGND_SET)
	
	ltc.console_set_char_background(UI, x, y, ltc.white, ltc.BKGND_SET)
	
	ltc.console_blit(UI, 0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 0, 0, 0, 1, .5)

def set_snapshot(snapshot):
	global SNAPSHOT
	SNAPSHOT = snapshot

def render(VP):
	global land_colors, sea_colors, SNAPSHOT

	region	= SNAPSHOT['region']
	ego		= SNAPSHOT['ego']
	cast	= SNAPSHOT['cast']
	terrain	= region.get_terrain()
	fov		= region.get_fov()
	
	ltc.console_clear(CON)
	
	radius = 40
	
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
		
	#maxh = 0
	#minh = 0
	
	#explored
	for y in range(VP.height):	
		vy = y + ovy		
		for x in range(VP.width):
			vx = x + ovx
						
			h = int(terrain[vy][vx].z)
			haze = 1;
			rgb_land = land_colors[h]
			rgb_sea = sea_colors[-h]
			
			
			if h > ego.z > 0:
				continue
			if h < ego.z:
				haze = .9
			
			"""
			# no fov
			if h < 0:
				ltc.console_set_char_background(CON, ofx + x, ofy + y, rgb_sea, ltc.BKGND_SET)
				#ltc.console_set_char_background(CON, x, y, ltc.red, ltc.BKGND_SET)
				#ltc.console_set_default_foreground(CON, ltc.cyan)
				#ltc.console_put_char(CON, x, y, "~", ltc.BKGND_SET)
			else:
				ltc.console_set_char_background(CON, ofx + x, ofy + y, rgb_land, ltc.BKGND_SET)
			"""
			
			# LAST WORKING CODE
			# in FOV area
			if (ox < vx < ox + (radius * 2)) and (oy < vy < oy + (radius * 2)) and in_circle(ego.x, ego.y, radius, vx, vy):
				# in FOV
				if fov[vy - oy][vx - ox] > 0:
					terrain[vy][vx].explored = True
					if h < 0:
						ltc.console_set_char_background(CON, ofx + x, ofy + y, rgb_sea * fov[vy - oy][vx - ox], ltc.BKGND_SET)
						#ltc.console_set_char_background(CON, x, y, ltc.red, ltc.BKGND_SET)
						#ltc.console_set_default_foreground(CON, ltc.cyan)
						#ltc.console_put_char(CON, x, y, "~", ltc.BKGND_SET)
					else:
						ltc.console_set_char_background(CON, ofx + x, ofy + y, rgb_land * fov[vy - oy][vx - ox], ltc.BKGND_SET)
						
			
			
			
			"""
			# DELETE THIS
			if in_circle(ego.x, ego.y, radius, vx, vy):
				if h < 0:
					ltc.console_set_char_background(CON, ofx + x, ofy + y, rgb_sea * fov[vy - oy][vx - ox], ltc.BKGND_SET)
					#ltc.console_set_char_background(CON, x, y, ltc.red, ltc.BKGND_SET)
					#ltc.console_set_default_foreground(CON, ltc.cyan)
					#ltc.console_put_char(CON, x, y, "~", ltc.BKGND_SET)
				else:
					ltc.console_set_char_background(CON, ofx + x, ofy + y, rgb_land * fov[vy - oy][vx - ox], ltc.BKGND_SET)
			"""
			"""	
				for entity in terrain[vy][vx].entities:
					symbol = sym.get_symbol(entity)
					ltc.console_set_default_foreground(CON, symbol.front_color)
					ltc.console_set_char_background(CON, ofx + x, ofy + y, symbol.back_color, ltc.BKGND_SET )
					ltc.console_put_char(CON,  ofx + x, ofy + y, symbol.char, ltc.BKGND_SET)
			
				if terrain[vy][vx].explored:
					if terrain[vy][vx].block_sight:
						ltc.console_set_char_background(CON, x, y, EXPLORED_WALL, ltc.BKGND_SET)
					else:
						ltc.console_set_char_background(CON, x, y, EXPLORED_GROUND, ltc.BKGND_SET)
			"""
			"""
			# in FOV area
			if (ox < vx < ox + (radius * 2)) and (oy < vy < oy + (radius * 2)):
				# in FOV
				if fov[vy - oy][vx - ox] > 0:
					terrain[vy][vx].explored = True
					if terrain[vy][vx].block_sight:
						ltc.console_set_char_background(CON, x, y, LIGHT_WALL * fov[vy - oy][vx - ox], ltc.BKGND_SET )
					else:
						ltc.console_set_char_background(CON, x, y, LIGHT_GROUND * fov[vy - oy][vx - ox], ltc.BKGND_SET )
			# DELETE THIS -- END OF BLOCK
			"""
			
			
	#print minh, maxh

	#render entities
	for cha in cast:
		chax,chay = SNAPSHOT['region'].xy_global_to_local((cha.gx, cha.gy))
		
		symbol = sym.get_symbol(cha)
		ltc.console_set_default_foreground(CON, symbol.front_color)
		
		ltc.console_set_char_background(CON, chax + ofx - ovx, chay + ofy - ovy, symbol.back_color, ltc.BKGND_SET )
		
		ltc.console_put_char(CON, chax + ofx - ovx, chay + ofy - ovy, symbol.char, ltc.BKGND_SET)
	
			
	ltc.console_blit(CON, 0, 0, ofx + VP.width, ofy + VP.height, 0, 0, 0)
	
	render_UI(VP)
	
	ltc.console_flush()

	
def cleanup():
	global CON
	ltc.console_clear(CON)
		
