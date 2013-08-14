__author__ = "Olof Karlsson"
__version__ = "0.1"
__license__ = "All Rights Reserved"

import pygame
import other.useful as useful
import objects.blocks.block as block
import objects.shadow as shadow
import objects.groups as groups
import settings.settings as settings

def convert():
	NormalBlock.image.convert()

class NormalBlock(block.Block):

	# Load the image file here, so any new instance of this class doesn't have to reload it every time, they can just copy the surface.
	image = pygame.image.load("res/block/block.png")

	# Standard values. These will be used unless any other values are specified per instance of this class.
	width = image.get_width() * settings.GAME_SCALE
	height = image.get_height() * settings.GAME_SCALE
	health = 20

	# Scale image to settings.GAME_SCALE.
	image = pygame.transform.scale(image, (width, height))

	def __init__(self, x, y, owner):
		# We start by calling the superconstructor.
		block.Block.__init__(self, owner, x, y, NormalBlock.width, NormalBlock.height, NormalBlock.health)	

		# Create the image attribute that is drawn to the surface.
		self.image = NormalBlock.image.copy()

		# Colorize the block.
		self.color = self.owner.color
		useful.colorize_image(self.image, self.color)	
