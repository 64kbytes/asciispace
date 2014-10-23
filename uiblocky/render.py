import config
import libtcodpy as ltc
import symbols as sym
import math
from algorithms.fov import *

DARK_WALL = ltc.grey
DARK_GROUND = ltc.black
EXPLORED_WALL = ltc.black
EXPLORED_GROUND = ltc.darkest_grey * .5

LIGHT_WALL = ltc.Color(130, 110, 50)
LIGHT_GROUND = ltc.Color(200, 180, 50)

VWP		= None
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
	
	ltc.console_blit(UI, 0, 0, config.SCREEN_WIDTH, 1, 0, 0, 0, 1, .5)

def render(VP, snapshot):

	region	= snapshot['region']
	ego		= snapshot['ego']
	cast	= snapshot['cast']
	terrain	= region.get_terrain()
	fov		= region.get_fov()
	
	ltc.console_clear(CON)
	
	radius = 20
	
	#recompute FOV if needed (the player moved or something)
	if not ego.is_updated or fov is None:
		fov = region.update_fov(ego.x, ego.y, radius)
		ego.is_updated = True
	
	#ego fov origin	
	ox = ego.x - radius
	oy = ego.y - radius
	
	#viewport origin
	ovx = VP.x
	ovy = VP.y
	
	#explored
	for y in range(config.SCREEN_HEIGHT):
		vy = y + ovy
		if (vy > region.height - 1) or vy < 0:
			break
		for x in range(config.SCREEN_WIDTH):
			vx = x + ovx
			if (vx > region.width - 1) or vx < 0:
				break
				
			if terrain[vy][vx].height < -990:
				ltc.console_set_char_background(CON, x, y, ltc.Color(255, 0, 0), ltc.BKGND_SET)
				continue
			
			h = int(terrain[vy][vx].height)
							
			ltc.console_set_char_background(CON, x, y, ltc.Color(0, h, 0), ltc.BKGND_SET)
			
			"""	
			if terrain[vy][vx].explored:
				if terrain[vy][vx].block_sight:
					ltc.console_set_char_background(CON, x, y, EXPLORED_WALL, ltc.BKGND_SET)
				else:
					ltc.console_set_char_background(CON, x, y, EXPLORED_GROUND, ltc.BKGND_SET)
			
			# in FOV area
			if (ox < vx < ox + (radius * 2)) and (oy < vy < oy + (radius * 2)):
				# in FOV
				if fov[vy - oy][vx - ox] > 0:
					terrain[vy][vx].explored = True
					if terrain[vy][vx].block_sight:
						ltc.console_set_char_background(CON, x, y, LIGHT_WALL * fov[vy - oy][vx - ox], ltc.BKGND_SET )
					else:
						ltc.console_set_char_background(CON, x, y, LIGHT_GROUND * fov[vy - oy][vx - ox], ltc.BKGND_SET )
			"""
	
	#render characters
	for cha in cast:
		symbol = sym.get_symbol(cha)
		ltc.console_set_default_foreground(CON, symbol.front_color)
		ltc.console_set_char_background(CON, cha.x - ovx, cha.y - ovy, symbol.back_color, ltc.BKGND_SET )
		ltc.console_put_char(CON, cha.x - ovx, cha.y - ovy, symbol.char, ltc.BKGND_SET)
			
	ltc.console_blit(CON, 0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 0, 0, 0)
	
	render_UI(snapshot)
	
	ltc.console_flush()

	
def cleanup():
	global CON
	ltc.console_clear(CON)
		
