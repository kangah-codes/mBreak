__author__ = "Olof Karlsson"
__version__ = "0.1"
__license__ = "All Rights Reserved"

import pygame
import math
import shadow
import useful
from settings import *

class Particle(pygame.sprite.Sprite):

	def __init__(self, x, y, width, height, angle, speed, retardation, color, alpha_step = 0):
		# We start by calling the superconstructor.
		pygame.sprite.Sprite.__init__(self)
		
		# Create the rect used for drawing the particle.
		self.rect = pygame.rect.Rect(x, y, width, height)

		# Keep track of x and y as floats, for preciseness sake (rect keeps track of x,y as ints)
		self.x = x
		self.y = y

		# Setup speed, angle and retardation values, used when moving the particle.
		self.angle = angle
		self.speed = speed
		self.retardation = retardation

		# Setup alpha values.
		self.alpha_step = alpha_step
		self.alpha = 255

		# Setup the color values, used for drawing the particle.
		self.color = pygame.Color(color.r, color.g, color.b, color.a)

		# Setup shadow color value, used for coloring the shadow.
		self.shadow_blend_color = pygame.Color(100, 100, 100, 255)
		self.shadow_color = useful.blend_colors(self.color, self.shadow_blend_color)

		# Create a shadow.
		self.shadow = shadow.Shadow(self, SHADOW_OFFSET_X, SHADOW_OFFSET_Y, True, True, self.shadow_color)

	def update(self):
		# Update speed, and kill self if speed gets to or under 0.
		self.speed = self.speed - self.retardation
		if self.speed <= 0:
			self.kill()

		# Update the alpha in the RGBA color value.
		if self.alpha_step > 0:
			if self.color.a - self.alpha_step < 0:
				self.kill()
			else:
				self.color.a = self.color.a - self.alpha_step

		# Finally, move the particle with speed in consideration.
		self.x = self.x + (math.cos(self.angle) * self.speed)
		self.y = self.y + (math.sin(self.angle) * self.speed)
		self.rect.x = self.x
		self.rect.y = self.y