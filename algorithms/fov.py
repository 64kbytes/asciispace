import math

#Bresenham
def get_line(x1, y1, x2, y2):
	points = []
	issteep = abs(y2-y1) > abs(x2-x1)
	if issteep:
		x1, y1 = y1, x1
		x2, y2 = y2, x2
	rev = False
	if x1 > x2:
		x1, x2 = x2, x1
		y1, y2 = y2, y1
		rev = True
	deltax = x2 - x1
	deltay = abs(y2-y1)
	error = int(deltax / 2)
	y = y1
	ystep = None
	if y1 < y2:
		ystep = 1
	else:
		ystep = -1
	for x in range(x1, x2 + 1):
		if issteep:
			points.append((y, x))
		else:
			points.append((x, y))
		error -= deltay
		if error < 0:
			y += ystep
			error += deltax
	# Reverse the list if the coordinates were reversed
	if rev:
		points.reverse()
	return points
	
#Pythagoras
def distance(p0, p1):
	dx = p1[0] - p0[0]
	dy = p1[1] - p0[1]
	return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
	
def set_fov_map(terrain):
	fov_map = [[1 for x in range(len(terrain[0]))] for y in range(len(terrain))]

	for y in range(len(terrain)):
		for x in range(len(terrain[0])):
			if terrain[y][x].block_sight:
				fov_map[y][x] = 0
			else:
				fov_map[y][x] = 1
	return fov_map

		    
def set_light_map(world):
	pass

def map_compute_fov(fov_map, x0, y0, light_walls = False, radius = 10, fix = True):
	
	fov = [[0 for x in range(radius * 2)] for y in range(radius * 2)]
	
	ox = x0 - radius
	oy = y0 - radius
	
	for q in range(4):
			
		for n in range(radius * 2):
		
			if q == 0:
				line = get_line(x0, y0, ox + n, oy + 0)
			elif q == 1: 
				line = get_line(x0, y0, ox + n, oy + (radius * 2) - 1)
			elif q == 2: 
				line = get_line(x0, y0, ox + 0, oy + n)
			elif q == 3: 
				line = get_line(x0, y0, ox + (radius * 2) - 1, oy + n)
				
			
			s = 1.0 / float(len(line))
			d = 0
			
			for square in line:
				d += s
				light = 1 - math.pow(d, 2) + .1
				#light = 1
				
				if (square[0] >= len(fov_map[0])) or (square[1] >= len(fov_map)) or (square[0] < 0 )or (square[1] < 0):
					break

				#artifact fix. Is straight vertical or horizontal
				if n == radius and fix:
					#is horizontal
					if q == 0 or q == 1:
						fov[square[1] - oy][square[0] - ox - 1] = light
						fov[square[1] - oy][square[0] - ox + 1] = light
					#is vertical
					if q == 2 or q == 3:	
						fov[square[1] - oy + 1][square[0] - ox] = light
						fov[square[1] - oy - 1][square[0] - ox] = light
				
				
				if fov_map[square[1]][square[0]] < 1:
					if light_walls:
						fov[square[1] - oy][square[0] - ox] = light
					break
				
				fov[square[1] - oy][square[0] - ox] = light
				
	return fov

