import pygame, math, random, time
import numpy as np
from CONST import *
from cell import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font('OpenSans.ttf', 30)
font_dont = pygame.font.Font('OpenSans.ttf', 50)

hold = False
selected = None
menu = True
total_level = 17
total_level += 1
movable_area = []
for i in range(total_level):
	movable_area.append(0)
movable_area[0] = (1, 1, 12, 12)
movable_area[1] = (1, 1, 4, 5)
movable_area[2] = (1, 1, 5, 7)
movable_area[3] = (1, 1, 4, 5)
movable_area[4] = (1, 1, 4, 3)
movable_area[5] = (1, 1, 10, 3)
movable_area[6] = (1, 1, 4, 5)
movable_area[7] = (1, 1, 5, 6)
movable_area[8] = (8, 7, 9, 4)
movable_area[9] = (1, 1, 18, 3)
movable_area[10] = (1, 5, 5, 5)
movable_area[11] = (1, 1, 5, 12)
movable_area[12] = (1, 7, 3, 7)
movable_area[13] = (1, 1, 6, 5)
movable_area[14] = (8, 1, 5, 4)
movable_area[15] = (6, 1, 18, 2)
movable_area[16] = (4, 1, 8, 4)
movable_area[17] = (1, 1, 5, 5)
ROWS = [14, 7, 9, 7, 5, 10, 7, 13, 13, 12, 7, 14, 9, 14, 13, 14, 9, 16]
COLS = [14, 10, 12, 10, 12, 15, 10, 14, 17, 20, 15, 15, 17, 20, 15, 20, 12, 20]
def level_setup(n):
	set_up = [
			[
				# 0
				[], # Normal
				[], # Wall
				[], # Block
				[], # Rotate
				[], # Pushser
				[], # Generator
				[]  # Enemy
			],
			[
				# 1
				[],
				[],
				[],
				[],
				[Pusher_Cell(2, 2, 'right')],
				[],
				[Enemy_Cell(4, 7)]
			],
			[
				# 2
				[Normal_Cell(7, 1), Normal_Cell(6, 2)],
				[],
				[],
				[],
				[Pusher_Cell(4, 2, 'right')],
				[],
				[Enemy_Cell(2, 7), Enemy_Cell(2, 8), Enemy_Cell(2, 9)]
			],
			[
				# 3
				[],
				[],
				[],
				[Rotate_Cell(4, 1, 'right')],
				[Pusher_Cell(2, 4, 'up')],
				[],
				[Enemy_Cell(3, 7)]
			],
			[
				# 4
				[Normal_Cell(2, 3)],
				[],
				[],
				[],
				[],
				[Generator_Cell(3, 2, 'right')],
				[Enemy_Cell(2, 8), Enemy_Cell(2, 9), Enemy_Cell(2, 10)]
			],
			[
				# 5
				[Normal_Cell(1, 1)],
				[Wall_Cell(7, 3)],
				[],
				[],
				[Pusher_Cell(1, 5, 'down'), Pusher_Cell(7, 2, 'right')],
				[],
				[Enemy_Cell(7, 12), Enemy_Cell(7, 13)]
			],
			[
				# 6
				[],
				[],
				[],
				[],
				[Pusher_Cell(5, 2, 'right')],
				[Generator_Cell(3, 4, 'down')],
				[Enemy_Cell(2, 7), Enemy_Cell(4, 7)]
			],
			[
				# 7
				[Normal_Cell(3, 3)],
				[Wall_Cell(2, 1)],
				[],
				[],
				[Pusher_Cell(4, 2, 'right'), Pusher_Cell(4, 5, 'down'), Pusher_Cell(5, 3, 'down')],
				[],
				[Enemy_Cell(10, 11)]
			],
			[
				# 8
				[Normal_Cell(8, 7), Normal_Cell(10, 12), Normal_Cell(9, 12), Normal_Cell(9, 14), Normal_Cell(11, 8)],
				[],
				[],
				[],
				[Pusher_Cell(9, 9, 'left')],
				[Generator_Cell(9, 7, 'up')],
				[Enemy_Cell(10, 2), Enemy_Cell(10, 3), Enemy_Cell(8, 2), Enemy_Cell(2, 8)]
			],
			[	
				# 9
				[Normal_Cell(5, 2)],
				[Wall_Cell(1, 3, False)],
				[],
				[Rotate_Cell(5, 3), Rotate_Cell(5, 4), Rotate_Cell(5, 5), Rotate_Cell(5, 6), Rotate_Cell(5, 7), Rotate_Cell(2, 3)],
				[Pusher_Cell(5, 1, 'right'), Pusher_Cell(1, 5, 'down'), Pusher_Cell(1, 7, 'down')],
				[],
				[Enemy_Cell(9, 9)]
			],
			[	
				# 10
				[],
				[Wall_Cell(3, 5)],
				[],
				[],
				[],
				[Generator_Cell(2, 7, 'right'), Generator_Cell(5, 9, 'left')],
				[Enemy_Cell(3, 3), Enemy_Cell(3, 12)]
			],
			[	
				# 11
				[Normal_Cell(3, 3)],
				[Wall_Cell(10, 5)],
				[Block_Cell(2, 2), Block_Cell(7, 4)],
				[Rotate_Cell(12, 2)],
				[Pusher_Cell(1, 4, 'up'), Pusher_Cell(5, 2, 'up'), Pusher_Cell(9, 5, 'up'), Pusher_Cell(10, 2, 'up'), Pusher_Cell(10, 4, 'up')],
				[],
				[Enemy_Cell(3, 11), Enemy_Cell(4, 11), Enemy_Cell(5, 11), Enemy_Cell(6, 11)]
			],
			[	
				# 12
				[Normal_Cell(1, 8), Normal_Cell(7, 7)],
				[],
				[],
				[Rotate_Cell(3, 9, 'right')],
				[],
				[Generator_Cell(4, 7, 'right')],
				[Enemy_Cell(4, 1), Enemy_Cell(4, 2), Enemy_Cell(4, 3), Enemy_Cell(4, 4), Enemy_Cell(4, 5), Enemy_Cell(4, 11), Enemy_Cell(4, 12), Enemy_Cell(4, 13), Enemy_Cell(4, 14),Enemy_Cell(4, 15)]
			],
			[	
				# 13
				[],
				[Wall_Cell(2, 3, False), Wall_Cell(8, 1, False)],
				[],
				[],
				[Pusher_Cell(1, 3, 'down'), Pusher_Cell(1, 5, 'right'), Pusher_Cell(4, 2, 'right')],
				[Generator_Cell(5, 4, 'right'), Generator_Cell(8, 2, 'right')],
				[Enemy_Cell(10, 10), Enemy_Cell(10, 11), Enemy_Cell(10, 12), Enemy_Cell(10, 13), Enemy_Cell(10, 14), Enemy_Cell(10, 15), Enemy_Cell(10, 16), Enemy_Cell(10, 17), Enemy_Cell(10, 18)]
			],
			[	
				# 14
				[Normal_Cell(8, 3)],
				[],
				[],
				[],
				[],
				[Generator_Cell(8, 1, 'right'), Generator_Cell(9, 1, 'right'), Generator_Cell(8, 4, 'up')],
				[]
			],
			[	
				# 15
				[Normal_Cell(7, 10), Normal_Cell(6, 12)],
				[Wall_Cell(6, 17,False), Wall_Cell(6, 18, False), Wall_Cell(7, 17, False), Wall_Cell(7, 18, False)],
				[],
				[Rotate_Cell(6, 2), Rotate_Cell(6, 4)],
				[Pusher_Cell(6, 3, 'right'), Pusher_Cell(7, 3, 'right')],
				[Generator_Cell(6, 9, 'up'), Generator_Cell(7, 14, 'down')],
				[]
			],
			[	
				# 16
				[Normal_Cell(4, 2), Normal_Cell(4, 4)],
				[Wall_Cell(4, 5, False)],
				[],
				[Rotate_Cell(5, 3, 'left')],
				[Pusher_Cell(5, 5, 'left')],
				[Generator_Cell(6, 1, 'right')],
				[Enemy_Cell(2, 3), Enemy_Cell(6, 10)]
			],
			[	
				# 17
				[],
				[],
				[],
				[],
				[],
				[Generator_Cell(1, 1, 'right'), Generator_Cell(1, 2, 'right'), Generator_Cell(1, 3, 'down'), Generator_Cell(1, 4, 'left')],
				[]
			],
			[	
				# 13
				[],
				[],
				[],
				[],
				[],
				[],
				[]
			]
	]
	grid = []
	create_grid(grid, ROWS[n], COLS[n])
	if n == 7:
		for i in range(7):
			for j in range(7):
				set_up[n][2].append(Block_Cell(i+1, j+6))

	if n == 14:
		for i in range(7):
			for j in range(7):
				set_up[n][2].append(Block_Cell(i+1, j+1))

		for i in range(5):
			for j in range(6):
				set_up[n][-1].append(Enemy_Cell(i+1, j+8))

	if n == 15:
		for i in range(9):
			set_up[n][-1].append(Enemy_Cell(4, i+8))
			set_up[n][-1].append(Enemy_Cell(9, i+8))

	if n == 17:
		for i in range(5):
			for j in range(10):
				set_up[n][2].append(Block_Cell(i+6, j+1))

		for i in range(4):
			for j in range(7):
				set_up[n][-1].append(Enemy_Cell(i+11, j+1))

	NormalC, WallC, BlockC, RotateC, PusherC, GeneratorC, EnemyC = set_up[n]

	for cell in EnemyC:
		cell.update_index(grid)
	for cell in NormalC:
		cell.update_index(grid)
	for cell in BlockC:
		cell.update_index(grid)
	for cell in GeneratorC:
		cell.update_index(grid)
	for cell in PusherC:
		cell.update_index(grid)
	for cell in WallC:
		cell.update_index(grid)
	for cell in RotateC:
		cell.update_index(grid)

	for i in range(ROWS[n]):
		BlockC.append(Block_Cell(i, 0))
		BlockC.append(Block_Cell(i, COLS[n]-1))
		if i == 0 or i == ROWS[n]-1:
			for j in range(1, COLS[n]-1):
				BlockC.append(Block_Cell(i, j))
	
	cells = [PusherC, GeneratorC, WallC, RotateC, BlockC, EnemyC, NormalC]

	return grid, cells

def create_grid(grid, ROWS, COLS):
	for i in range(ROWS + 1):
		grid.append([])
		for j in range(COLS + 1):
			grid[i].append(0)

def draw_grid(screen, ROWS, COLS):
	for i in range(COLS + 1):
		x = i * SCALE
		pygame.draw.line(screen, WHITE, (x, 0), (x, ROWS*SCALE), width = 3)

	for j in range(ROWS + 1):
		y = j * SCALE
		pygame.draw.line(screen, WHITE, (0, y), (COLS*SCALE, y), width = 3)

def Movable_area(screen, area):
	y, x, w, h = area
	pygame.draw.rect(screen, CYAN, (x * SCALE, y * SCALE, w * SCALE, h * SCALE))

def draw_playlist(screen):
	playlist_rect = []
	for i in range(total_level):
			playlist_rect.append((50*(2*(i%8)+1), 50 + 100*(i//8), 50, 50))

	for i in range(total_level):
		text = str(i)
		if i == 0:
			text = 'quit'
		text_surf = (font.render(text, False, WHITE))
		screen.blit(text_surf, (playlist_rect[i][0] + 25 - text_surf.get_width()//2, playlist_rect[i][1]+25-text_surf.get_height()//2))
		pygame.draw.rect(screen, WHITE, playlist_rect[i], width = 5)


	return playlist_rect

def inside(pos, rect):
	posX, posY = pos
	x, y, w, h = rect

	if posX >= x and posY >= y and posX < x + w and posY < y + h:
		return True

	return False

def back_to_menu(screen):
	x, y, width, height = WIDTH-100, 0, 100, 50
	pygame.draw.rect(screen, WHITE, (x, y, width, height), width = 2)
	text_surf = (font.render('menu', False, WHITE))
	screen.blit(text_surf, (x + 50 - text_surf.get_width()//2, y+25-text_surf.get_height()//2))
	mouse_pos = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if click[0] and inside(mouse_pos, (x, y, width, height)):
		return True
	return False

def reset_button(screen):
	x, y, width, height = WIDTH-50, 100, 50, 50
	pygame.draw.rect(screen, WHITE, (x, y, width, height), width = 2)

	pygame.draw.circle(screen, WHITE, (x+width//2, y+width//2), 15, width = 3)
	pygame.draw.rect(screen, BACKGROUND, (x+width//2-5, y + width//2, 15, 20))
	pygame.draw.rect(screen, WHITE, (x+width//2+7, y+width//2, 3, 10))
	pygame.draw.rect(screen, WHITE, (x+width//2+7, y+width//2+8, 10, 3))

	mouse_pos = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if click[0] and inside(mouse_pos, (x, y, width, height)):
		return True
	return False

def play_button(screen):
	x, y, width, height = WIDTH-50, 50, 50, 50
	pygame.draw.rect(screen, WHITE, (x, y, width, height), width = 2)

	pygame.draw.polygon(screen, WHITE, ((x + 10, y + 10), (x + 10, y + height - 10), (x + width - 8, y + height//2)) )

	mouse_pos = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if click[0] and inside(mouse_pos, (x, y, width, height)):
		return True
	return False

def draw_menu(screen):
	screen.fill(BLACK)
	playlist_rect = draw_playlist(screen)
	clicked = False
	mouse_pos = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if click[0]:
		for i in range(total_level):
			if inside(mouse_pos, playlist_rect[i]):
				return i

def draw_level(screen, grid, cells, pressed, n):
	global isclicked
	global clicked
	global hold
	global selected
	global menu
	global choice
	global play
	menu = False
	mouse_pos = pygame.mouse.get_pos()
	PusherC, GeneratorC, WallC, RotateC, BlockC, EnemyC, NormalC = cells
	screen.fill(BACKGROUND)
	if len(EnemyC) == 0:
		pressed = False
		text_surf = font_dont.render('level '+ str(n) + ' passed', False, WHITE)
		screen.blit(text_surf, (WIDTH//2 - text_surf.get_width()//2, HEIGHT - 3*text_surf.get_height()//2))
	
	Movable_area(screen, movable_area[n])
	if not hold:
		menu = back_to_menu(screen)
		play_option = play_button(screen)
		if play_option == True:
			play = True

		if selected:
			selected.i = selected.y//SCALE
			selected.j = selected.x//SCALE
			selected.x = selected.j * SCALE
			selected.y = selected.i * SCALE
			selected.update_index(grid)
		selected = None

	if not play:
		if not clicked and hold:
			mouseX, mouseY = mouse_pos
			mouseI = mouseY//SCALE
			mouseJ = mouseX//SCALE
			i, j, w, h = movable_area[n]
			if mouseI < i or mouseJ < j or mouseI >= i + h or mouseJ >= j + w or grid[mouseI][mouseJ] != 0:
				clicked = True
			if mouseI >= i and mouseJ >= j and mouseI < i + h and mouseJ < j + w and grid[mouseI][mouseJ] == 0:
				hold = False

		if clicked:
			mouseX, mouseY = mouse_pos
			mouseI = mouseY//SCALE
			mouseJ = mouseX//SCALE
			i, j, w, h = movable_area[n]
			try:
				cell = grid[mouseI][mouseJ]
			except:
				cell = 0
			if mouseI >= i and mouseJ >= j and mouseI < i + h and mouseJ < j + w:
				if cell != 0 and type(cell) != Block_Cell and type(cell) != Enemy_Cell and not hold:
					hold = True
					if type(cell) == Normal_Cell:
						for c in cells[-1]:
							if c.i == cell.i and c.j == cell.j:
								selected = c
								break
					elif type(cell) == Pusher_Cell:
						for c in cells[0]:
							if c.i == cell.i and c.j == cell.j:
								selected = c
								break
					elif type(cell) == Generator_Cell:
						for c in cells[1]:
							if c.i == cell.i and c.j == cell.j:
								selected = c
								break

					elif type(cell) == Wall_Cell:
						for c in cells[2]:
							if c.i == cell.i and c.j == cell.j:
								selected = c
								break

					elif type(cell) == Rotate_Cell:
						for c in cells[3]:
							if c.i == cell.i and c.j == cell.j:
								selected = c
								break
 
					grid[mouseI][mouseJ] = 0

			else:
				if not hold:
					clicked = False

			if (cell == 0 or type(cell) == Enemy_Cell or type(cell) == Block_Cell) and not hold :
				clicked = False

		if hold:
			pygame.draw.circle(screen, WHITE, mouse_pos, 5)

		if selected:
			selected.x, selected.y = mouse_pos

		for cell in EnemyC:
			cell.draw()

		for cell in GeneratorC:
			cell.draw()

		for cell in PusherC:
			cell.draw()

		for cell in NormalC:
			cell.draw()

		for cell in BlockC:
			cell.draw()

		for cell in WallC:
			cell.draw()

		for cell in RotateC:
			cell.draw()

	else:
		for cell in EnemyC:
			if type(grid[cell.i][cell.j]) != Enemy_Cell and type(grid[cell.i][cell.j]) != int:
				grid[cell.i][cell.j].kill(cell, cells)
			cell.update_index(grid)
			cell.draw()

		for cell in GeneratorC:
			if pressed:
				cell.update(grid, cells)
			cell.update_index(grid)
			cell.draw()

		for cell in RotateC:
			if pressed:
				cell.update(grid)
			cell.update_index(grid)
			cell.draw()

		for cell in PusherC:
			if pressed:
				cell.update(grid)	
			cell.update_index(grid)					
			cell.draw()

		for cell in WallC:
			cell.update_index(grid)
			cell.draw()

		for cell in NormalC:
			cell.update_index(grid)			
			cell.draw()


		for cell in BlockC:
			cell.update_index(grid)
			cell.draw()

	draw_grid(screen, ROWS[n], COLS[n])

def draw(screen, grid, cells, pressed):
	global clicked
	global hold
	global selected
	global menu
	global choice
	global play
	global run


	if menu:
		choice = draw_menu(screen)
		for i in range(1, total_level):
			grid[i], cells[i] = level_setup(i)
		hold = False
		clicked = False
		play = False

	if choice  == 0:
		run = False

	for i in range(1, total_level):
		if choice == i:
			draw_level(screen, grid[choice], cells[choice], pressed, choice)
			if not hold:
				return_option = reset_button(screen)
				if return_option:
					grid[choice], cells[choice] = level_setup(choice)
					hold = False
					clicked = False
					play = False

	pygame.display.update()

def main():
	global clicked
	global hold
	global play
	global run
	run = True
	grid = []
	cells = []
	for i in range(total_level):
		grid.append(0)
		cells.append(0)
	
	clicked = False
	play = False
	fps = 0
	while run:
		fps += 1
		pressed = False
		if fps == 30:
			pressed = True
			fps = 0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					clicked = not clicked
		draw(screen, grid, cells, pressed)
		clock.tick(120)


	pygame.quit()

main()
