#!/usr/bin/python
import libtcodpy as libtcod

TILE_SET = 'terminal.png'

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

MAP_WIDTH = 80
MAP_HEIGHT = 45

color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)

player_x = SCREEN_WIDTH / 2
player_y = SCREEN_HEIGHT / 2

libtcod.sys_set_fps(LIMIT_FPS)

libtcod.console_set_custom_font(TILE_SET, libtcod.FONT_LAYOUT_ASCII_INROW | libtcod.FONT_TYPE_GREYSCALE)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Space Thing', False)

con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

class Tile:
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight
		
def make_map():
	return [[ Tile(False) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH) ]
	
themap = make_map()
	
	

themap[20][20].blocked = True
themap[20][20].block_sight = True
themap[50][22].blocked = True
themap[50][22].block_sight = True


class Object:
	def __init__(self, x, y, char, color):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
	
	def move(self, dx, dy):
		if not themap[self.x + dx][self.y + dy].blocked:
			self.x += dx
			self.y += dy
	
	def draw(self):
		if self.color is not None:
			libtcod.console_set_default_foreground(con, self.color)
			
		libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
	
	def clear(self):
		libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)
		
ego = Object(MAP_WIDTH / 2, MAP_HEIGHT / 2, '@', libtcod.white)
npc = Object(MAP_WIDTH / 2 - 5, MAP_HEIGHT / 2, 255, None)

objects = [npc, ego]

def render_all():
	for obj in objects:
		obj.draw()

	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			wall = themap[x][y].block_sight
			if wall:
				libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET )
			else:
				libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET )
	
	libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
	
	

def handle_keys():
	global ego
	
	# special keys
	key = libtcod.console_check_for_keypress()
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
	elif key.vk == libtcod.KEY_ESCAPE:
		return True
	
	dx = dy = 0
	
	# ego movement
	if libtcod.console_is_key_pressed(libtcod.KEY_UP):
		dy = -1
	if libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
		dy = 1
	if libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
		dx = -1
	if libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
		dx = 1
		
	ego.move(dx, dy)
	
for y in xrange(32):
	for x in xrange(12):
		libtcod.console_put_char(con, x, y, y * 12 + x)	
	
while not libtcod.console_is_window_closed():
	#libtcod.console_clear(con)
	for obj in objects:
		obj.clear()
	
	exit = handle_keys()
	
	render_all()
	
	
	libtcod.console_flush()

	if exit:
		break

