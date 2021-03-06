__author__ = "Olof Karlsson"
__license__ = "All Rights Reserved"

import pygame, sys
import random
from pygame.locals import *
import gui.textitem as textitem
import gui.logo as logo
import gui.listmenu as listmenu
import gui.transition as transition
import settings.settings as settings
import settings.graphics as graphics
import screens.scene as scene

# These are the screens we can reach directly from the main menu, so we import them here.
import screens.preparemenu as preparemenu
import screens.helpmenu as helpmenu
import screens.optionsmenu as optionsmenu

"""

This is the main menu of the game. From here, we can either continue to the preparation menu, we can change a few graphic options,
or we can reach the help menu or the about menu. We can also quit the game, of course.

The main menu is easily added upon. It has an active_menu object that makes sure that we only display and update/handle the currently active
submenu.

If either the quit button is activated or the ESCAPE key is pressed, we quit the game.

"""

class MainMenu(scene.Scene):

	def __init__(self, window_surface, main_clock, title_logo = None):
		# Call the superconstructor.
		scene.Scene.__init__(self, window_surface, main_clock)

		# The next screen to be started when the gameloop ends.
		self.next_screen = preparemenu.PrepareMenu

		# Setup the logo and the variables needed to handle the animation of it.
		self.setup_logo(title_logo)

		# Setup all the menu buttons.
		self.setup_main_menu()

		# Setup the menu transitions.
		self.transition.setup_odd_even_transition(self.main_menu, True, True, False, False)

		# Setup and play music.
		self.setup_music()

		# And finally, start the gameloop!
		self.gameloop()

	def setup_main_menu(self):
		self.main_menu = listmenu.ListMenu(settings.SCREEN_WIDTH / 2.0, settings.SCREEN_HEIGHT / 2.0)
		self.main_menu.add(textitem.TextItem("Start"), self.start)
		self.main_menu.add(textitem.TextItem("Options"), self.options)
		self.main_menu.add(textitem.TextItem("Help"), self.help)
		self.main_menu.add(textitem.TextItem("Quit"), self.quit)
		self.main_menu.items[0].selected = True
		self.menu_list.append(self.main_menu)

	def options(self, item):
		optionsmenu.OptionsMenu(self.window_surface, self.main_clock, self.title_logo)
		self.transition.setup_odd_even_transition(self.main_menu, True, True, False, False)

	def help(self, item):
		helpmenu.HelpMenu(self.window_surface, self.main_clock)
		self.transition.setup_odd_even_transition(self.main_menu, True, True, False, False)

	def setup_logo(self, title_logo):
		if title_logo is None:
			# If the title_logo object doesn't exists, creates it and positions it.
			self.title_logo = logo.Logo()
			
			self.title_logo.x = (settings.SCREEN_WIDTH - self.title_logo.get_width()) / 2
			self.title_logo.y = ((settings.SCREEN_HEIGHT - self.title_logo.get_height()) / 4)
			
			self.title_logo.play()
		else:
			# Otherwise, we just save the given title_logo object
			self.title_logo = title_logo
		
		self.logo_desired_position = ((settings.SCREEN_WIDTH - self.title_logo.get_width()) / 2, ((settings.SCREEN_HEIGHT - self.title_logo.get_height()) / 4))
		self.logo_transition = transition.Transition()
		self.logo_transition.speed = 120 * settings.GAME_SCALE

	def setup_music(self):
		self.__class__.music_list = settings.TITLE_MUSIC
		if not pygame.mixer.music.get_busy():
			# We only care about loading and playing the music if it isn't already playing.
			self.play_music()

	def start(self, item):
		self.done = True
		self.next_screen = preparemenu.PrepareMenu

	def back(self, item):
		self.transition.setup_odd_even_transition(self.main_menu, True, True, False, False)
		
		# Restore the logo's position.
		self.logo_desired_position = ((settings.SCREEN_WIDTH - self.title_logo.get_width()) / 2, ((settings.SCREEN_HEIGHT - self.title_logo.get_height()) / 4))
		
	def quit(self, item):
		# Sets next_screen to None so we just quit the game when the gameloop is over.
		self.done = True
		self.next_screen = None

	def event(self, event):
		if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == JOYBUTTONDOWN and event.button in settings.JOY_BUTTON_BACK):
			# If the ESCAPE key or back button on gamepad is pressed, we select the last item in the main menu, which should be the QUIT button.
			for item in self.main_menu.items:
				item.selected = False
			self.main_menu.items[-1].selected = True

	def update(self):
		# Makes sure that the logo always moves to the desired posisition, and stays there.
		self.logo_transition.move_item_to_position(self.title_logo, self.logo_desired_position, self.main_clock)

		#  If the logo is in place, show the menu.
		if self.title_logo.x == self.logo_desired_position[0] and self.title_logo.y == self.logo_desired_position[1]:
			# Updates the menu transitions, and the currently active menu.
			self.transition.update(self.main_clock)
			self.main_menu.update(self.main_clock)

	def draw(self):
		# Every frame begins by filling the whole screen with the background color.
		self.window_surface.fill(settings.BACKGROUND_COLOR)

		# Draw the title logo.
		self.title_logo.draw(self.window_surface)

		# If the logo is in place, draw the currently active menu to the screen.
		if self.title_logo.x == self.logo_desired_position[0] and self.title_logo.y == self.logo_desired_position[1]:
			self.main_menu.draw(self.window_surface)

	def on_exit(self):
		if self.next_screen is None:
			# We save the settings before we quit.
			settings.save()
			graphics.save()
			pygame.quit()
			sys.exit()
		elif self.next_screen is helpmenu.HelpMenu:
			# We start the help screen or the about screen and send them a reference to this instance, so they can return to it later.
			# We also setup the transitions, so when they return they transition in.
			self.transition.setup_odd_even_transition(self.main_menu, True, True, False, False)
			self.next_screen(self.window_surface, self.main_clock, self)
		elif not self.next_screen is None:
			# Else, we just start the next screen with the default parameters.
			self.next_screen(self.window_surface, self.main_clock)

		# Otherwise we simply let this scene end.