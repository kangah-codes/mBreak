__author__ = "Olof Karlsson"
__license__ = "All Rights Reserved"

import pygame
import objects.groups as groups
import objects.effects.flash as flash
import settings.settings as settings

"""

A simple "dummy" object that can act as a "parent" for effects, used when displaying effects that are not attached to other
"real" objects.

"""

class Dummy(pygame.sprite.Sprite):

	def __init__(self, duration, x, y, width, height):
		# We start by calling the superconstructor.
		pygame.sprite.Sprite.__init__(self)

		# We store the amount of time passed. When time passed is greater than timeout time, the dummy is killed.
		self.time_passed = 0

		# Store the duration. The dummy will be killed when time_passed is greater than duration.
		self.duration = duration

		# Create the rect used for collision detection, position etc.
		self.rect = pygame.rect.Rect(x, y, width, height)
		
		# Store self in the main dummy_group.
		groups.Groups.dummy_group.add(self)

		# Create an effect group to handle effects on this dummy.
		self.effect_group = pygame.sprite.Group()

	def add_flash(self, start_color, final_color, tick_amount):
		self.effect_group.add(flash.Flash(self, start_color, final_color, tick_amount))

	def update(self, main_clock):
		self.time_passed += main_clock.get_time()
		if self.time_passed >= self.duration:
			# When the duration runs out, we destroy ourselves.
			self.destroy()

	def destroy(self):
		self.kill()
		for effect in self.effect_group:
			effect.destroy()