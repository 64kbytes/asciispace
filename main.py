#!/usr/bin/python
import libtcodpy as ltc
import config as cfg
import gm.gm as gm
from render import *

con = None
mouse = None
key = None

def init():
	global con, mouse, key, cfg
	w = cfg.SCREEN_WIDTH
	h = cfg.SCREEN_HEIGHT
	ltc.sys_set_fps(cfg.FPS)
	"""
	FONT_LAYOUT_ASCII_INCOL : characters in ASCII order, code 0-15 in the first column
	FONT_LAYOUT_ASCII_INROW : characters in ASCII order, code 0-15 in the first row
	FONT_LAYOUT_TCOD : simplified layout. See examples below.
	FONT_TYPE_GREYSCALE
	"""
	ltc.console_set_custom_font(cfg.TILE_SET, ltc.FONT_LAYOUT_ASCII_INROW | ltc.FONT_TYPE_GREYSCALE)
	ltc.console_init_root(w, h, cfg.TITLE, False)
	con = ltc.console_new(w, h)
	mouse = ltc.Mouse()
	key = ltc.Key()
	
	gm.init(cfg)
	
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
	ltc.console_clear(con)
	
	ltc.sys_check_for_event(ltc.EVENT_KEY_PRESS | ltc.EVENT_MOUSE, key, mouse)
	
	
	look_tile()
	
	#clear(con, gm)

	exit = handle_ui()
	
	if exit:
		break
		
	render(con, gm)
	ltc.console_flush()


