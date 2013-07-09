__author__ = "Olof Karlsson"
__version__ = "0.1"
__license__ = "All Rights Reserved"

import pygame, sys
from pygame.locals import *
import math
import random
import debug
import ball
import paddle
import player
import multiball
import block
import groupholder
from settings import *

def create_block(x, y, owner):
	health = 2

	return block.Block(x, y, health, owner)

def setup_gamefield(player_left, player_right):
	x_amount = 4
	y_amount = (LEVEL_HEIGHT - (block.Block.height * 2)) / block.Block.height

	for i in range(0, x_amount):
		for j in range(0, y_amount):
			create_block(LEVEL_X + (block.Block.width * 2) + (block.Block.width * i), LEVEL_Y + block.Block.height + (block.Block.height * j), player_left)
			# Create a flipped right block.Block.
			temp_block_right = create_block(LEVEL_MAX_X - (block.Block.width * 3) - (block.Block.width * i), LEVEL_Y + block.Block.height + (block.Block.height * j), player_right)
			temp_block_right.image = pygame.transform.flip(temp_block_right.image, True, False)

	# Create and store the paddle.
	left_paddle_x = LEVEL_X + (x_amount * block.Block.width) + (block.Block.width * 3)
	left_paddle_y = (LEVEL_Y + LEVEL_HEIGHT - block.Block.height) / 2
	player_left.paddle_group.add(paddle.Paddle(left_paddle_x, left_paddle_y, player_left))

	right_paddle_x = LEVEL_MAX_X - (x_amount * block.Block.width) - (block.Block.width * 4)
	right_paddle_y = (LEVEL_Y + LEVEL_HEIGHT - block.Block.height) / 2
	paddle_right = paddle.Paddle(right_paddle_x, right_paddle_y, player_right)
	paddle_right.image = pygame.transform.flip(paddle_right.image, True, False)
	player_right.paddle_group.add(paddle_right)

def create_player_left():
	name = PLAYER_LEFT_NAME
	key_up = PLAYER_LEFT_KEY_UP
	key_down = PLAYER_LEFT_KEY_DOWN
	color = pygame.Color(255, 0, 0, 255)

	player_left = player.Player(name, key_up, key_down, color)

	return player_left

def create_player_right():
	name = PLAYER_RIGHT_NAME
	key_up = PLAYER_RIGHT_KEY_UP
	key_down = PLAYER_RIGHT_KEY_DOWN
	color = pygame.Color(0, 0, 255, 255)

	player_right = player.Player(name, key_up, key_down, color)
	
	return player_right

"""
I should come up with a good way to handle the sprite groups and stick to it.
I can either pass the groups to each method/class as they are needed, or I can have 
a global groupholder module that holds all the groups.
"""
def destroy_groups():
	groupholder.ball_group.empty()
	groupholder.particle_group.empty()
	groupholder.block_group.empty()
	groupholder.powerup_group.empty()
	groupholder.paddle_group.empty()
	groupholder.player_group.empty()
	groupholder.shadow_group.empty()

def main(window_surface, main_clock, debug_font):
	# Variable to keep the gameloop going. Setting this to True will end the gameloop and return to the screen that started this gameloop.
	done = False

	# Setup the background images.
	floor_surface = pygame.image.load("res/background/planks/planks_floor.png")
	floor_surface = pygame.transform.scale(floor_surface, (floor_surface.get_width() * GAME_SCALE, floor_surface.get_height() * GAME_SCALE)).convert()

	wall_vertical = pygame.image.load("res/background/planks/planks_wall_vertical.png")
	wall_vertical = pygame.transform.scale(wall_vertical, (wall_vertical.get_width() * GAME_SCALE, wall_vertical.get_height() * GAME_SCALE)).convert()
	wall_horizontal = pygame.image.load("res/background/planks/planks_wall_horizontal.png")
	wall_horizontal = pygame.transform.scale(wall_horizontal, (wall_horizontal.get_width() * GAME_SCALE, wall_horizontal.get_height() * GAME_SCALE)).convert()
	corner_top_left = pygame.image.load("res/background/planks/planks_corner_top_left.png")
	corner_top_left = pygame.transform.scale(corner_top_left, (corner_top_left.get_width() * GAME_SCALE, corner_top_left.get_height() * GAME_SCALE)).convert()
	corner_top_right = pygame.image.load("res/background/planks/planks_corner_top_right.png")
	corner_top_right = pygame.transform.scale(corner_top_right, (corner_top_right.get_width() * GAME_SCALE, corner_top_right.get_height() * GAME_SCALE)).convert()

	# Setup the objects.
	block.convert()
	paddle.convert()
	ball.convert()
	multiball.convert()

	# Create the left player.
	player_left = create_player_left()
	
	# Create the right player.
	player_right = create_player_right()

	# Setup the game world.
	setup_gamefield(player_left, player_right)

	while not done:
		# Begin a frame by blitting the background to the game_surface.
		window_surface.fill(BACKGROUND_COLOR)
		window_surface.blit(floor_surface, (LEVEL_X, LEVEL_Y))
		
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				# Return to intromenu.
				destroy_groups()
				done = True
			elif event.type == KEYDOWN and event.key == K_l:
				debug.create_ball_left(player_left)
			elif event.type == KEYDOWN and event.key == K_r:
				debug.create_ball_right(player_right)
			elif event.type == KEYDOWN and event.key == K_p:
				debug.create_powerup()
		
		# If debug mode is enabled, allow certain commands. This is all done in the debug module.
		if DEBUG_MODE:
			debug.update(player_left, player_right)

		# Update the balls.
		groupholder.ball_group.update()
		
		# Update the particles.
		groupholder.particle_group.update()
		
		# Update the players.
		groupholder.player_group.update()
		
		# Update the shadows.
		groupholder.shadow_group.update(main_clock)

		# Draw the shadows.
		for shadow in groupholder.shadow_group:
			shadow.blit_to(window_surface)

		# Draw the blocks.
		groupholder.block_group.draw(window_surface)

		# Draw the paddles.
		groupholder.paddle_group.draw(window_surface)

		# Draw the powerups.
		groupholder.powerup_group.draw(window_surface)

		# Draw the particles.
		for particle in groupholder.particle_group:
			window_surface.fill(particle.color, particle.rect)

		# Draw the balls.
		groupholder.ball_group.draw(window_surface)

		# Draw the background walls and overlying area.
		window_surface.blit(wall_horizontal, (LEVEL_X, LEVEL_Y - (4 * GAME_SCALE)))
		window_surface.blit(wall_horizontal, (LEVEL_X, LEVEL_MAX_Y))
		window_surface.blit(wall_vertical, (LEVEL_X - (4 * GAME_SCALE), LEVEL_Y))
		window_surface.blit(wall_vertical, (LEVEL_MAX_X, LEVEL_Y))
		window_surface.blit(corner_top_left, (LEVEL_X - (4 * GAME_SCALE), LEVEL_Y - (4 * GAME_SCALE)))
		window_surface.blit(corner_top_left, (LEVEL_MAX_X, LEVEL_MAX_Y))
		window_surface.blit(corner_top_right, (LEVEL_MAX_X, LEVEL_Y - (4 * GAME_SCALE)))
		window_surface.blit(corner_top_right, (LEVEL_X - (4 * GAME_SCALE), LEVEL_MAX_Y))

		# Draw the players.
		# groupholder.player_group.draw(window_surface)

		if DEBUG_MODE:
			# Display various debug information.
			debug.display(window_surface, main_clock, debug_font)
		
		pygame.display.update()
		
		# Finally, constrain the game to a set maximum amount of FPS.
		main_clock.tick(MAX_FPS)