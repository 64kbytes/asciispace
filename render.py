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
