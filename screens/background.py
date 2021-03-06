__author__ = "Olof Karlsson"
__license__ = "All Rights Reserved"

import pygame
import objects.camera as camera
import settings.settings as settings
import settings.graphics as graphics

"""

This class handles the background images in the game. It requires a folder_name, and in that folder it looks for a few images
that is uses to build up the background. The images in the given folder must have names matching those below.

In order to display the background images, simply call the draw method where you want to draw them.

"""

class Background:
	
	def __init__(self, folder_name):
		# Setup the background surfaces.
		self.floor_surface = pygame.image.load("res/background/" + folder_name + "/floor.png")
		self.floor_surface = pygame.transform.scale(self.floor_surface, (self.floor_surface.get_width() * settings.GAME_SCALE, self.floor_surface.get_height() * settings.GAME_SCALE))
		self.wall_vertical_left = pygame.image.load("res/background/" + folder_name + "/wall_vertical_left.png")
		self.wall_vertical_left = pygame.transform.scale(self.wall_vertical_left, (self.wall_vertical_left.get_width() * settings.GAME_SCALE, self.wall_vertical_left.get_height() * settings.GAME_SCALE))
		self.wall_vertical_right = pygame.image.load("res/background/" + folder_name + "/wall_vertical_right.png")
		self.wall_vertical_right = pygame.transform.scale(self.wall_vertical_right, (self.wall_vertical_right.get_width() * settings.GAME_SCALE, self.wall_vertical_right.get_height() * settings.GAME_SCALE))
		self.wall_horizontal_top = pygame.image.load("res/background/" + folder_name + "/wall_horizontal_top.png")
		self.wall_horizontal_top = pygame.transform.scale(self.wall_horizontal_top, (self.wall_horizontal_top.get_width() * settings.GAME_SCALE, self.wall_horizontal_top.get_height() * settings.GAME_SCALE))
		self.wall_horizontal_bottom = pygame.image.load("res/background/" + folder_name + "/wall_horizontal_bottom.png")
		self.wall_horizontal_bottom = pygame.transform.scale(self.wall_horizontal_bottom, (self.wall_horizontal_bottom.get_width() * settings.GAME_SCALE, self.wall_horizontal_bottom.get_height() * settings.GAME_SCALE))
		self.corner_top_left = pygame.image.load("res/background/" + folder_name + "/corner_top_left.png")
		self.corner_top_left = pygame.transform.scale(self.corner_top_left, (self.corner_top_left.get_width() * settings.GAME_SCALE, self.corner_top_left.get_height() * settings.GAME_SCALE))
		self.corner_bottom_right = pygame.image.load("res/background/" + folder_name + "/corner_bottom_right.png")
		self.corner_bottom_right = pygame.transform.scale(self.corner_bottom_right, (self.corner_bottom_right.get_width() * settings.GAME_SCALE, self.corner_bottom_right.get_height() * settings.GAME_SCALE))
		self.corner_top_right = pygame.image.load("res/background/" + folder_name + "/corner_top_right.png")
		self.corner_top_right = pygame.transform.scale(self.corner_top_right, (self.corner_top_right.get_width() * settings.GAME_SCALE, self.corner_top_right.get_height() * settings.GAME_SCALE))
		self.corner_bottom_left = pygame.image.load("res/background/" + folder_name + "/corner_bottom_left.png")
		self.corner_bottom_left = pygame.transform.scale(self.corner_bottom_left, (self.corner_bottom_left.get_width() * settings.GAME_SCALE, self.corner_bottom_left.get_height() * settings.GAME_SCALE))

		# Convert the surfaces, for performances sake.
		self.floor_surface.convert()
		self.wall_vertical_left.convert()
		self.wall_vertical_right.convert()
		self.wall_horizontal_top.convert()
		self.wall_horizontal_bottom.convert()
		self.corner_top_left.convert()
		self.corner_top_right.convert()
		self.corner_bottom_left.convert()
		self.corner_bottom_right.convert()

		# Setup the rects used to display a white border around the level if graphics.BACKGROUND is False.
		self.wall_horizontal_top_rect = pygame.Rect(settings.LEVEL_X - self.wall_vertical_left.get_width(), settings.LEVEL_Y - self.wall_horizontal_top.get_height(), self.wall_horizontal_top.get_width() + (2 * self.wall_vertical_left.get_width()), self.wall_horizontal_top.get_height())
		self.wall_horizontal_bottom_rect = pygame.Rect(settings.LEVEL_X - self.wall_vertical_left.get_width(), settings.LEVEL_MAX_Y, self.wall_horizontal_bottom.get_width() + (2 * self.wall_vertical_right.get_width()), self.wall_horizontal_bottom.get_height())
		self.wall_vertical_left_rect = pygame.Rect(settings.LEVEL_X - self.wall_vertical_left.get_width(), settings.LEVEL_Y, self.wall_vertical_left.get_width(), self.wall_vertical_left.get_height())
		self.wall_vertical_right_rect = pygame.Rect(settings.LEVEL_MAX_X, settings.LEVEL_Y, self.wall_vertical_right.get_width(), self.wall_vertical_right.get_height())

	def draw(self, surface):
		# We either blit the background images or fill the rects, depending on graphics.BACKGROUND.
		if graphics.BACKGROUND:
			surface.blit(self.wall_horizontal_top, (settings.LEVEL_X - camera.CAMERA.x, settings.LEVEL_Y - camera.CAMERA.y - self.wall_horizontal_top.get_height()))
			surface.blit(self.wall_horizontal_bottom, (settings.LEVEL_X - camera.CAMERA.x, settings.LEVEL_MAX_Y - camera.CAMERA.y))
			surface.blit(self.wall_vertical_left, (settings.LEVEL_X - camera.CAMERA.x - self.wall_vertical_left.get_width(), settings.LEVEL_Y - camera.CAMERA.y))
			surface.blit(self.wall_vertical_right, (settings.LEVEL_MAX_X - camera.CAMERA.x, settings.LEVEL_Y - camera.CAMERA.y))
			surface.blit(self.corner_top_left, (settings.LEVEL_X - camera.CAMERA.x - self.wall_vertical_left.get_width(), settings.LEVEL_Y - camera.CAMERA.y - self.wall_horizontal_top.get_height()))
			surface.blit(self.corner_bottom_right, (settings.LEVEL_MAX_X - camera.CAMERA.x, settings.LEVEL_MAX_Y - camera.CAMERA.y))
			surface.blit(self.corner_top_right, (settings.LEVEL_MAX_X - camera.CAMERA.x, settings.LEVEL_Y - camera.CAMERA.y - self.wall_horizontal_top.get_height()))
			surface.blit(self.corner_bottom_left, (settings.LEVEL_X - camera.CAMERA.x - self.wall_vertical_left.get_width(), settings.LEVEL_MAX_Y - camera.CAMERA.y))
		else:
			surface.fill(settings.BORDER_COLOR, (self.wall_horizontal_top_rect.x - camera.CAMERA.x, self.wall_horizontal_top_rect.y - camera.CAMERA.y, self.wall_horizontal_top_rect.width, self.wall_horizontal_top_rect.height))
			surface.fill(settings.BORDER_COLOR, (self.wall_horizontal_bottom_rect.x - camera.CAMERA.x, self.wall_horizontal_bottom_rect.y - camera.CAMERA.y, self.wall_horizontal_bottom_rect.width, self.wall_horizontal_bottom_rect.height))
			surface.fill(settings.BORDER_COLOR, (self.wall_vertical_left_rect.x - camera.CAMERA.x, self.wall_vertical_left_rect.y - camera.CAMERA.y, self.wall_vertical_left_rect.width, self.wall_vertical_left_rect.height))
			surface.fill(settings.BORDER_COLOR, (self.wall_vertical_right_rect.x - camera.CAMERA.x, self.wall_vertical_right_rect.y - camera.CAMERA.y, self.wall_vertical_right_rect.width, self.wall_vertical_right_rect.height))
