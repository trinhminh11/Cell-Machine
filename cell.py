import pygame, math, random
from CONST import *
import numpy as np



class Rectangle(object):
	def __init__(self, i, j):
		self.i = i
		self.j = j
		self.x = j * SCALE
		self.y = i * SCALE
		self.width = SCALE
		self.vel = SCALE
		self.block = {'up': False, 'down': False, 'left': False, 'right': False}

	def findNeighbors(self, grid):
		i, j = self.i, self.j
		neighbors = {'left': 0, 'up': 0, 'right': 0,'down': 0} # Left, Top, Right, Bottom
		if j > 0:
			neighbors['left'] = grid[i][j-1]
		if i > 0:
			neighbors['up'] = grid[i-1][j]
		if j < len(grid[0])-1:
			neighbors['right'] = grid[i][j+1]
		if i < len(grid)-1:
			neighbors['down'] = grid[i+1][j]


		return neighbors

	def check_block(self, grid, neighbors):
		if type(self) == Block_Cell:
			self.block = {'up': True, 'down': True, 'left': True, 'right': True}

		if type(self) != Block_Cell:
			for direction, neighbor in neighbors.items():
				if neighbor == 0:
					self.block[direction] = False
				else:
					if neighbor.block[direction]:
						self.block[direction] = True
					else:
						self.block[direction] = False

		if type(self) == Wall_Cell:
			if self.verticle:
				self.block['left'] = True
				self.block['right'] = True
				for direction in ['up', 'down']:
					if neighbors[direction] == 0:
						self.block[direction] = False
					else:
						if neighbors[direction].block[direction]:
							self.block[direction] = True
						else:
							self.block[direction] = False
			else:
				self.block['up'] = True
				self.block['down'] = True
				for direction in ['left', 'right']:
					if neighbors[direction] == 0:
						self.block[direction] = False
					else:
						if neighbors[direction].block[direction]:
							self.block[direction] = True
						else:
							self.block[direction] = False

		if type(self) == Wall_Cell:
			print(self.block)



	def push(self, neighbors, grid, direction, current):
		if not (type(self) == Wall_Cell and (self.verticle and (direction == 'left' or direction == 'right') or not self.verticle and ((direction == 'up' or direction == 'down')))):
			if type(neighbors[direction]) != int and type(neighbors[direction]) != Enemy_Cell:
				neighbors[direction].move(current, grid)

	def move(self, other, grid):
		neighbors = self.findNeighbors(grid)
		self.push(neighbors, grid, other.direction, other)
		self.check_block(grid, neighbors)
		if not self.block[other.direction]:
			if other.direction == 'left':
				self.x -= self.vel

			elif other.direction == 'right':
				self.x += self.vel

			elif other.direction == "down":
				self.y += self.vel

			elif other.direction == 'up':
				self.y -= self.vel

		grid[self.i][self.j] = 0

		self.update_index(grid)
		if type(self) != Pusher_Cell:
			self.draw()

	def draw_background(self, color):
		pygame.draw.rect(screen, color, (self.x, self.y, self.width	, self.width))
		pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width	, self.width), width = 1)

	def update_index(self, grid):
		self.i = self.y // SCALE
		self.j = self.x // SCALE
		grid[self.i][self.j] = self

	def kill(self, enemy, cells):
		if type(self) == Normal_Cell:
			for cell in cells[-1]:
				if cell.i == self.i and cell.j == self.j:
					cells[-1].remove(cell)
					cells[-2].remove(enemy)
					break
		if type(self) == Pusher_Cell:
			for cell in cells[0]:
				if cell.i == self.i and cell.j == self.j:
					cells[0].remove(cell)
					cells[-2].remove(enemy)
					break
		if type(self) == Generator_Cell:
			for cell in cells[1]:
				if cell.i == self.i and cell.j == self.j:
					cells[1].remove(cell)
					cells[-2].remove(enemy)
					break

		if type(self) == Wall_Cell:
			for cell in cells[2]:
				if cell.i == self.i and cell.j == self.j:
					cells[2].remove(cell)
					cells[-2].remove(enemy)
					break

		if type(self) == Rotate_Cell:
			for cell in cells[3]:
				if cell.i == self.i and cell.j == self.j:
					cells[3].remove(cell)
					cells[-2].remove(enemy)
					break

class Normal_Cell(Rectangle):
	def __init__(self, i, j):
		super().__init__(i, j)

	# def update(self, grid, neighbors = None):
	# 	self.update_index(grid)

	def draw(self):
		self.draw_background(YELLOW)
		pygame.draw.line(screen, WHITE, (self.x + 12, self.y + 5), (self.x + 12, self.y + self.width - 5), width = 5)
		pygame.draw.line(screen, WHITE, (self.x + self.width - 12, self.y + 5), (self.x + self.width - 12, self.y + self.width - 5), width = 5)
		pygame.draw.line(screen, WHITE, (self.x + 5, self.y + 12), (self.x + self.width - 5, self.y + 12), width = 5)
		pygame.draw.line(screen, WHITE, (self.x + 5, self.y + self.width - 12), (self.x + self.width - 5, self.y + self.width - 12), width = 5)

class Block_Cell(Rectangle):
	def __init__(self, i, j):
		super().__init__(i, j)

	def draw(self):
		self.draw_background(BLACK)

class Pusher_Cell(Rectangle):
	def __init__(self, i, j, facing, run = True):
		super().__init__(i, j)
		self.direction = facing
		self.run = run

	def update(self, grid, run = True):
		neighbors = self.findNeighbors(grid)
		self.push(neighbors, grid, self.direction, self)
		self.check_block(grid, neighbors)
		grid[self.i][self.j] = 0
		if run:
			if self.run:
				if not self.block[self.direction]:
					if self.direction == 'left':
						self.x -= self.vel
					elif self.direction	== 'right':
						self.x += self.vel
					elif self.direction	== "down":
						self.y += self.vel
					elif self.direction	== 'up':
						self.y -= self.vel
			else:
				self.run = True

		self.update_index(grid)


	def draw(self):
		self.draw_background((37, 150, 255))
		if self.direction == 'left':
			pygame.draw.polygon(screen, WHITE, ((self.x + self.width - 10, self.y + 10), (self.x + self.width - 10, self.y + self.width - 10), (self.x + 8, self.y + self.width//2)))

		elif self.direction	== 'right':
			pygame.draw.polygon(screen, WHITE, ((self.x + 10, self.y + 10), (self.x + 10, self.y + self.width - 10), (self.x + self.width - 8, self.y + self.width//2)))
			
		elif self.direction	== "down":
			pygame.draw.polygon(screen, WHITE, ((self.x + self.width - 10, self.y + 10), (self.x + 10, self.y + 10), (self.x + self.width//2, self.y + self.width - 8)))
			
		elif self.direction	== 'up':
			pygame.draw.polygon(screen, WHITE, ((self.x + self.width - 10, self.y + self.width - 10), (self.x + 10, self.y + self.width - 10), (self.x + self.width//2, self.y + 8)))


class Generator_Cell(Rectangle):
	def __init__(self, i, j, facing, run = True):
		super().__init__(i, j)
		self.direction = facing
		self.run = run

	def update(self, grid, cells):
		i, j = self.i, self.j
		grid[i][j] = 0
		if self.run:
			neighbors = self.findNeighbors(grid)
			if self.direction == 'up':
				if type(neighbors['down']) != int and type(neighbors['down'])!=Enemy_Cell and type(neighbors['down'])!=Block_Cell:
					if neighbors['up'] != 0:
						self.push(neighbors, grid, self.direction, self)
					neighbors = self.findNeighbors(grid)
					if neighbors['up'] == 0 or type(neighbors['up']) == Enemy_Cell:
						cell = neighbors['down']
						if type(cell) == Normal_Cell:
							generator = Normal_Cell(i - 1, j)
							cells[-1].append(generator)
							generator.update_index(grid)
							generator.draw()

						if type(cell) == Pusher_Cell:
							generator = Pusher_Cell(i - 1, j, cell.direction, False)
							cells[0].append(generator)
							generator.update(grid, False)
							generator.draw()

						if type(cell) == Generator_Cell:
							generator = Generator_Cell(i-1, j, cell.direction, False)
							cells[1].append(generator)
							generator.update_index(grid)
							generator.draw()

						if type(cell) == Wall_Cell:
							generator = Wall_Cell(i-1, j, cell.verticle)
							cells[2].append(generator)
							generator.update_index(grid)
							generator.draw()

						if type(cell) == Rotate_Cell:
							generator = Rotate_Cell(i-1, j, cell.direction, run = False)
							cells[3].append(generator)
							generator.update_index(grid)
							generator.draw()

			if self.direction == 'down':
				if type(neighbors['up']) != int and type(neighbors['up'])!=Enemy_Cell and type(neighbors['up'])!=Block_Cell:
					if neighbors['down'] != 0:
						self.push(neighbors, grid, self.direction, self)
					neighbors = self.findNeighbors(grid)
					if neighbors['down'] == 0 or type(neighbors['down']) == Enemy_Cell:
						cell = neighbors['up']
						if type(cell) == Normal_Cell:
							generator = Normal_Cell(i + 1, j)
							cells[-1].append(generator)
							generator.update_index(grid)
							generator.draw()

						if type(cell) == Pusher_Cell:
							generator = Pusher_Cell(i + 1, j, cell.direction, False)
							cells[0].append(generator)
							generator.update(grid, False)
							generator.draw()

						if type(cell) == Generator_Cell:
							generator = Generator_Cell(i+1, j, cell.direction, False)
							cells[1].append(generator)
							generator.update_index(grid)
							generator.draw()

						if type(cell) == Wall_Cell:
							generator = Wall_Cell(i+1, j, cell.verticle)
							cells[2].append(generator)
							generator.update_index(grid)
							generator.draw()

						if type(cell) == Rotate_Cell:
							generator = Rotate_Cell(i+1, j, cell.direction, run = False)
							cells[3].append(generator)
							generator.update_index(grid)
							generator.draw()

			if self.direction == 'left':
				if type(neighbors['right']) != int and type(neighbors['right'])!=Enemy_Cell and type(neighbors['right'])!=Block_Cell:
					if neighbors['left'] != 0:
						self.push(neighbors, grid, self.direction, self)
					neighbors = self.findNeighbors(grid)
					if neighbors['left'] == 0 or type(neighbors['left']) == Enemy_Cell:
						cell = neighbors['right']
						if type(cell) == Normal_Cell:
							generator = Normal_Cell(i, j-1)
							cells[-1].append(generator)
							generator.update_index(grid)
							generator.draw()

						if type(cell) == Pusher_Cell:
							generator = Pusher_Cell(i, j-1, cell.direction, False)
							cells[0].append(generator)
							generator.update(grid, False)
							generator.draw()

						if type(cell) == Generator_Cell:
							generator = Generator_Cell(i, j-1, cell.direction, False)
							cells[1].append(generator)
							generator.update_index(grid)
							generator.draw()

						if type(cell) == Wall_Cell:
							generator = Wall_Cell(i, j-1, cell.verticle)
							cells[2].append(generator)
							generator.update_index(grid)
							generator.draw()

						if type(cell) == Rotate_Cell:
							generator = Rotate_Cell(i, j-1, cell.direction,run = False)
							cells[3].append(generator)
							generator.update_index(grid)
							generator.draw()

			if self.direction == 'right':
				if type(neighbors['left']) != int and type(neighbors['left'])!=Enemy_Cell and type(neighbors['left'])!=Block_Cell:
					if neighbors['right'] != 0:
						self.push(neighbors, grid, self.direction, self)
					neighbors = self.findNeighbors(grid)
					if neighbors['right'] == 0 or type(neighbors['right']) == Enemy_Cell:
						cell = neighbors['left']
						if type(cell) == Normal_Cell:
							generator = Normal_Cell(i, j+1)
							cells[-1].append(generator)
							generator.update_index(grid)
							generator.draw()

						if type(cell) == Pusher_Cell:
							generator = Pusher_Cell(i, j+1, cell.direction, False)
							cells[0].append(generator)
							generator.update(grid, False)
							generator.draw()

						if type(cell) == Generator_Cell:
							generator = Generator_Cell(i, j+1, cell.direction, False)
							cells[1].append(generator)
							generator.update_index(grid)
							generator.draw()

						if type(cell) == Wall_Cell:
							generator = Wall_Cell(i, j+1, cell.verticle)
							cells[2].append(generator)
							generator.update_index(grid)
							generator.draw()

						if type(cell) == Rotate_Cell:
							generator = Rotate_Cell(i, j+1, cell.direction,run = False)
							cells[3].append(generator)
							generator.update_index(grid)
							generator.draw()
		else:
			self.run = True

		self.update_index(grid)

	def draw(self):
		self.draw_background(GREEN)
		if self.direction == 'left':
			pygame.draw.line(screen, WHITE, (self.x + self.width - 10, self.y + self.width//2), (self.x + self.width - 30, self.y + self.width//2), width = 5)
			pygame.draw.polygon(screen, WHITE, ((self.x + self.width - 25, self.y + 12), (self.x + self.width - 25, self.y + self.width - 12), (self.x + 8, self.y + self.width//2)))

		elif self.direction	== 'right':
			pygame.draw.line(screen, WHITE, (self.x + 30, self.y + self.width//2), (self.x + 10, self.y + self.width//2), width = 5)
			pygame.draw.polygon(screen, WHITE, ((self.x + 25, self.y + 12), (self.x + 25, self.y + self.width - 12), (self.x + self.width - 8, self.y + self.width//2)))
			
		elif self.direction	== "down":
			pygame.draw.line(screen, WHITE, (self.x + self.width//2, self.y + 30), (self.x + self.width//2, self.y + 10), width = 5)
			pygame.draw.polygon(screen, WHITE, ((self.x + self.width - 12, self.y + 25), (self.x + 12, self.y + 25), (self.x + self.width//2, self.y + self.width - 8)))
			
		elif self.direction	== 'up':
			pygame.draw.line(screen, WHITE, (self.x + self.width//2, self.y + self.width - 30), (self.x + self.width//2, self.y + self.width - 10), width = 5)
			pygame.draw.polygon(screen, WHITE, ((self.x + self.width - 12, self.y + self.width - 25), (self.x + 12, self.y + self.width - 25), (self.x + self.width//2, self.y + 8)))
		# pygame.draw.rect(screen, GREEN, (self.x, self.y))

class Enemy_Cell(Rectangle):
	def __init__(self, i, j):
		super().__init__(i, j)

	def draw(self):
		self.draw_background(RED)

class Wall_Cell(Rectangle):
	def __init__(self, i, j, verticle = True):
		super().__init__(i, j)
		self.verticle = verticle

	def draw(self):
		self.draw_background(YELLOW)

		if self.verticle:
			pygame.draw.line(screen, WHITE, (self.x + 15, self.y + 5), (self.x + 15, self.y + self.width - 5), width = 5)
			pygame.draw.line(screen, WHITE, (self.x + self.width - 15, self.y + 5), (self.x + self.width - 15, self.y + self.width - 5), width = 5)
		else:
			pygame.draw.line(screen, WHITE, (self.x + 5, self.y + 15), (self.x + self.width - 5, self.y + 15), width = 5)
			pygame.draw.line(screen, WHITE, (self.x + 5, self.y + self.width - 15), (self.x + self.width - 5, self.y + self.width - 15), width = 5)

class Rotate_Cell(Rectangle):
	def __init__(self, i, j, facing = 'right', run = True):
		super().__init__(i, j)
		self.direction = facing
		self.run = run

	def update(self, grid):
		i, j = self.i, self.j
		grid[i][j] = 0
		if self.run:
			neighbors = self.findNeighbors(grid)
			if self.direction == 'left':
				for direction, cell in neighbors.items():
					if type(cell) == Pusher_Cell or type(cell) == Generator_Cell:
						if cell.direction == 'left':
							cell.direction = 'down'
						elif cell.direction == 'down':
							cell.direction = 'right'
						elif cell.direction == 'right':
							cell.direction = 'up'
						elif cell.direction == 'up':
							cell.direction = 'left'
					if type(cell) == Wall_Cell:
						cell.verticle = not cell.verticle

			if self.direction == 'right':
				for direction, cell in neighbors.items():
					if type(cell) == Pusher_Cell or type(cell) == Generator_Cell:
						if cell.direction == 'left':
							cell.direction = 'up'
						elif cell.direction == 'up':
							cell.direction = 'right'
						elif cell.direction == 'right':
							cell.direction = 'down'
						elif cell.direction == 'down':
							cell.direction = 'left'
					if type(cell) == Wall_Cell:
						cell.verticle = not cell.verticle
		else:
			self.run = True

		self.update_index(grid)

	def draw(self):
		color = (255, 69, 0)
		self.draw_background(color)
		if self.direction == 'right':
			pygame.draw.circle(screen, WHITE, (self.x+self.width//2, self.y+self.width//2), 15, width = 3)
			pygame.draw.rect(screen, color, (self.x+self.width//2-5, self.y+self.width//2, 15, 20))
			pygame.draw.rect(screen, WHITE, (self.x+self.width//2+7, self.y+self.width//2, 3, 10))
			pygame.draw.rect(screen, WHITE, (self.x+self.width//2+7, self.y+self.width//2+8, 10, 3))


		elif self.direction == 'left':
			pygame.draw.circle(screen, WHITE, (self.x+self.width//2, self.y+self.width//2), 15, width = 3)
			pygame.draw.rect(screen, color, (self.x+self.width//2-10, self.y+self.width//2, 15, 20))
			pygame.draw.rect(screen, WHITE, (self.x+self.width//2-10, self.y+self.width//2, 3, 10))
			pygame.draw.rect(screen, WHITE, (self.x+self.width//2-17, self.y+self.width//2+8, 10, 3))
			