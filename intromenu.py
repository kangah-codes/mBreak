__author__ = "Olof Karlsson"
__version__ = "0.1"
__license__ = "All Rights Reserved"

import pygame, sys
from pygame.locals import *
from libs import pyganim
import useful
import textitem
import logo
import debug
import math
from settings import *

# Import any needed game screens here.
import game

def setup_logo():
	# Create the logo
	temp_logo = logo.Logo()

	# Set the logo so it displays in the middle of the screen.
	x = (BASE_WIDTH - temp_logo.get_width()) / 2
	y = ((BASE_HEIGHT - temp_logo.get_height()) / 2) - 30
	temp_logo.x = x
	temp_logo.y = y

	# At last, return the surface so we can blit it to the window_surface.
	return temp_logo

def setup_message(x, y):
	text = "Press ENTER to start"
	font_path = "fonts/8-BIT WONDER.TTF"
	font_size = 18
	font_color = (255, 255, 255)
	alpha_value = 255

	text = textitem.TextItem(text, font_path, font_size, font_color, alpha_value)

	text.x = (BASE_WIDTH - text.get_width()) // 2
	text.y = y + 150

	return text

def setup_music():
	pygame.mixer.music.load(TITLE_MUSIC)
	pygame.mixer.music.play()

def main(window_surface, game_surface, main_clock, debug_font):
	# Setup the logo and store the surface of the logo.
	title_logo = setup_logo()
	title_logo.play()

	# Setup the message beneath the logo and store the surface of the message.
	title_message = setup_message(title_logo.x, title_logo.y)
	# Sets the blink rate of the message.
	title_message_blink_rate = 750

	# Setup and play music.
	setup_music()
		
	# Keeps track of how much time has passed.
	time_passed = 0

	while True:
		# Every frame begins by filling the whole screen with the background color.
		window_surface.fill(BACKGROUND_COLOR)
		game_surface.fill(BACKGROUND_COLOR)
		
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				# If the ESCAPE key is pressed or the window is closed, the game is shut down.
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN and event.key == K_RETURN:
				# If ENTER is pressed, proceed to the next screen, and end this loop.
				pygame.mixer.music.stop()
				game.main(window_surface, game_surface, main_clock, debug_font)
		
		# If the music isn't playing, start it.
		if not pygame.mixer.music.get_busy():
			pygame.mixer.music.play()

		# Draw the logo.
		title_logo.draw(game_surface)

		# Increment the time passed.
		time_passed += main_clock.get_time()
		# Blinks the title message.
		time_passed = title_message.blink(time_passed, title_message_blink_rate)

		# Draw the title message.
		title_message.draw(game_surface)
		
		if DEBUG_MODE:
			# Display various debug information.
			debug.display(game_surface, main_clock, debug_font)

		#window_surface.blit(game_surface, ((SCREEN_WIDTH - BASE_WIDTH) / 2, (SCREEN_HEIGHT - BASE_HEIGHT) / 2))
		temp_surface = pygame.transform.scale(game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
		window_surface.blit(temp_surface, (0, 0))

		pygame.display.update()
		
		# Finally, constrain the game to a set maximum amount of FPS.
		main_clock.tick(MAX_FPS)