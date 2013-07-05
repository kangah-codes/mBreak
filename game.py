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
from settings import *

def create_ball(owner):
	width = 16
	height = 16
	x = random.uniform(0, SCREEN_WIDTH)
	y = random.uniform(0, SCREEN_HEIGHT)
	speed = random.uniform(3, 8)
	max_speed = 8
	angle = random.uniform(0, 2*math.pi)
	image_path = ("res/ball/ball.png")

	return ball.Ball(x, y, width, height, angle, speed, max_speed, image_path, owner)

def create_paddle(x, y):
	width = 16
	height = 64
	acceleration = 2
	retardation = 4
	max_speed = 8
	image_path = ("res/paddle/paddle.png")

	return paddle.Paddle(x, y, width, height, acceleration, retardation, max_speed, image_path)

def create_player_left(paddle):
	name = PLAYER_LEFT_NAME
	key_up = PLAYER_LEFT_KEY_UP
	key_down = PLAYER_LEFT_KEY_DOWN

	player_left = player.Player(name, key_up, key_down)

	player_left.add_paddle(paddle)

	return player_left

def create_player_right(paddle):
	name = PLAYER_RIGHT_NAME
	key_up = PLAYER_RIGHT_KEY_UP
	key_down = PLAYER_RIGHT_KEY_DOWN

	player_right = player.Player(name, key_up, key_down)
	
	player_right.add_paddle(paddle)

	return player_right

def main(window_surface, main_clock, debug_font):
	# Variable to keep the gameloop going.
	done = False

	# Define the group that contains all the balls.
	ball_group = pygame.sprite.Group()

	# Define the group that contains all the blocks.
	block_group = pygame.sprite.Group()

	# Define the group that contains all the paddles.
	paddle_group = pygame.sprite.Group()

	# Define the group that contains all the players.
	player_group = pygame.sprite.Group()

	# Create the players.
	paddle_left = create_paddle(100, SCREEN_HEIGHT / 2)
	paddle_group.add(paddle_left)
	player_left = create_player_left(paddle_left)
	player_group.add(player_left)

	paddle_right = create_paddle(SCREEN_WIDTH - 100, SCREEN_HEIGHT / 2)
	paddle_group.add(paddle_right)
	player_right = create_player_right(paddle_right)
	player_group.add(player_right)

	while not done:
		# Every frame begins by filling the whole screen with the background color.
		window_surface.fill(BACKGROUND_COLOR)
		
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				# Return to intromenu.
				done = True
			elif event.type == KEYDOWN and event.key == K_RETURN:
				if random.randint(0, 1) == 0:
					temp_ball = create_ball(player_left)
					player_left.add_ball(temp_ball)
					temp_ball.owner = player_left
					if DEBUG_MODE:
						print("Ball added to Player Left.")
				else:
					temp_ball = create_ball(player_right)
					player_right.add_ball(temp_ball)
					temp_ball.owner = player_right
					if DEBUG_MODE:
						print("Ball added to Player Right.")
				ball_group.add(temp_ball)

		if pygame.key.get_pressed()[K_SPACE]:
			if random.randint(0, 1) == 0:
				temp_ball = create_ball(player_left)
				player_left.add_ball(temp_ball)
				temp_ball.owner = player_left
				if DEBUG_MODE:
					print("Ball added to Player Left.")
			else:
				temp_ball = create_ball(player_right)
				player_right.add_ball(temp_ball)
				temp_ball.owner = player_right
				if DEBUG_MODE:
					print("Ball added to Player Right.")
			ball_group.add(temp_ball)

		# Update the balls.
		ball_group.update(ball_group, paddle_group, block_group)

		# Update the players.
		player_group.update()

		# Draw the balls.
		ball_group.draw(window_surface)

		# Draw the paddles.
		paddle_group.draw(window_surface)

		# Draw the players.
		# player_group.draw(window_surface)

		if DEBUG_MODE:
			# Display various debug information.
			debug.display(window_surface, main_clock, debug_font)
		
		pygame.display.update()
		
		# Finally, constrain the game to a set maximum amount of FPS.
		main_clock.tick(MAX_FPS)