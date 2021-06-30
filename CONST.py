import math
import pygame


WIDTH, HEIGHT = 900, 800
SCALE = 40

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255, 255)
GRAY = []
for i in range(256):
	GRAY.append((i, i, i))
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
BACKGROUND = GRAY[51]


class CreateVector(object):
	def __init__(self, x, y, z = 0):
		self.x = x
		self.y = y
		self.z = z

	def copy(self):
		return CreateVector(self.x, self.y)

	def add(self, v):
		if type(v) is int:
			self.x += v
			self.y += v 
			self.z += v
			return
		elif type(v) is tuple or type(v) is list:
			if len(v) == 1:
				v = v[0]
				self.x += v
				self.y += v 
				self.z += v
				return 
			elif len(v) == 2:
				self.x += v[0]
				self.y += v[1]
				return
			elif len(v) == 3:
				self.x += v[0]
				self.y += v[1]
				self.z += v[2]
				return

		elif type(v) is CreateVector:
			self.x += v.x 
			self.y += v.y 
			self.z += v.z
			return

	def rem(self, v):
		if type(v) is int:
			self.x %= v
			self.y %= v 
			self.z %= v
			return
		elif type(v) is tuple or type(v) is list:
			if len(v) == 1:
				v = v[0]
				self.x %= v
				self.y %= v 
				self.z %= v
				return
			
			elif len(v) == 2:
				self.x %= v[0]
				self.y %= v[1]
				self.z %= 1
				return
			elif len(v) == 3:
				self.x %= v[0]
				self.y %= v[1]
				self.z %= v[2]
				return

		elif type(v) is CreateVector:
			self.x %= v.x 
			self.y %= v.y 
			self.z %= v.z
			return

	def sub(self, v):
		if type(v) is int:
			self.x -= v
			self.y -= v 
			self.z -= v
			return
		elif type(v) is tuple or type(v) is list:
			if len(v) == 1:
				v = v[0]
				self.x -= v
				self.y -= v 
				self.z -= v
				req
			
			if len(v) == 2:
				self.x -= v[0]
				self.y -= v[1]
				self.z -= 0
				return
			if len(v) == 3:
				self.x -= v[0]
				self.y -= v[1]
				self.z -= v[2]
				return

		elif type(v) is CreateVector:
			self.x -= v.x 
			self.y -= v.y 
			self.z -= v.z
			return

	def mul(self, v):
		if type(v) is int:
			self.x *= v
			self.y *= v 
			self.z *= v
			return
		elif type(v) is tuple or type(v) is list:
			if len(v) == 1:
				v = v[0]
				self.x *= v
				self.y *= v 
				self.z *= v
				return
			
			elif len(v) == 2:
				self.x *= v[0]
				self.y *= v[1]
				self.z *= 1
				return

			elif len(v) == 3:
				self.x *= v[0]
				self.y *= v[1]
				self.z *= v[2]
				return

		elif type(v) is CreateVector:
			self.x *= v.x 
			self.y *= v.y 
			self.z *= v.z
			return


	def div(self, v):
		try:
			if type(v) is int:
				self.x /= v
				self.y /= v 
				self.z /= v
				return
			elif type(v) is tuple or type(v) is list:
				if len(v) == 1:
					v = v[0]
					self.x /= v
					self.y /= v 
					self.z /= v
					return
				
				if len(v) == 2:
					self.x /= v[0]
					self.y /= v[1]
					self.z /= 1
					return
				if len(v) == 3:
					self.x /= v[0]
					self.y /= v[1]
					self.z /= v[2]
					return

			elif type(v) is CreateVector:
				self.x /= v.x 
				self.y /= v.y 
				self.z /= v.z
				return
		except:
			print("valid number")

	def mag(self, base = (0, 0)):
		return ((self.x-base[0])*(self.x-base[0]) + (self.y-base[1])*(self.y-base[1]))**.5
	
	def magSq(self, base = (0, 0)):
		return ((self.x-base[0])*(self.x-base[0]) + (self.y-base[1])*(self.y-base[1]))

	def dot(self, v):
		return (self.x*v.x) + (self.y*v.y)

	def dist(self, v):
		return ((self.x-v.x)*(self.x-v.x) + (self.y-v.y)*(self.y-v.y)) ** .5 

	def normalize(self, base = (0, 0)):
		angle = self.heading(base)
		x = 1*math.cos(angle)+base[0]
		y = -1*math.sin(angle)+base[1]
		self.x = x
		self.y = y

	def limit(self, max_size, base = (0, 0)):
		angle = self.heading(base)
		x1 = max_size*math.cos(angle)+base[0]
		y1 = -max_size*math.sin(angle)+base[1]
		new_v = CreateVector(x1, y1)
		if self.magSq(base = base) > new_v.magSq(base = base):
			x = x1
			y = y1

			self.x = x 
			self.y = y 


	def setMag(self, size, base = (0, 0)):
		angle = self.heading(base)
		x = size*math.cos(angle)+base[0]
		y = -size*math.sin(angle)+base[1]

		self.x = x
		self.y = y

	def heading(self, base = (0, 0)):
		angle = math.atan2(-(self.y-base[1]), self.x-base[0])
		return angle

	def set_heading(self, angle, base = (0, 0)):
		r = self.mag(base = base)
		self.x = r*math.cos(angle) + base[0]
		self.y = -r*math.sin(angle) + base[1]

	def rotate(self, angle, base = (0, 0)):
		head = self.heading(base = base)
		r = self.mag(base = base)
		self.x = r*math.cos(head-angle) + base[0]
		self.y = -r*math.sin(head-angle) + base[1]

	def angleBetween(self, v):
		return abs(self.heading()-v.heading())

	def lerp(self, v, amount):
		dist = self.dist(v)
		x = amount*(v.x-self.x) + self.x
		y = amount*(v.y-self.y) + self.y
		v0 = CreateVector(x, y)
		return v0

	def reflect(slef, n):
		pass

	def array(self):
		return [self.x, self.y, self.z]

	def equals(self, v):
		return (self.x == v.x and self.y==v.y and self.z==v.z)

	def __repr__(self):
		return str(self.x) + " " + str(self.y)
	
	def set(self, x, y, z = 0):
		self.x = x
		self.y = y 
		self.z = z

def fromAngle(angle, mag = 1, base = (0,0)):
	x = mag * math.cos(angle) + base[0]
	y = -mag * math.sin(angle) + base[1]
	return CreateVector(x, y)

def fromAngles():
	pass

def random2D():
	import random
	angle = random.uniform(0, 2*math.pi)
	x = math.cos(angle)
	y = -math.sin(angle)

	return CreateVector(x, y)


def random3D():
	pass

def rotate(surface, angle):
	rotated_surface = pygame.transform.rotozoom(surface, angle, 1)
	rotated_rect = rotated_surface.get_rect(center = (200, 200))
	return rotated_surface, rotated_rect