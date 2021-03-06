__author__ = "Olof Karlsson"
__license__ = "All Rights Reserved"

import pygame
from pygame.locals import *
import gui.textitem as textitem
import gui.logo as logo
import gui.listmenu as listmenu
import gui.transition as transition
import settings.settings as settings
import screens.scene as scene

# These are the screens we can reach directly from the main menu, so we import them here.
import screens.aboutmenu as aboutmenu
import screens.graphicsmenu as graphicsmenu
import screens.soundmenu as soundmenu

"""

This is the main menu of the game. From here, we can either continue to the preparation menu, we can change a few graphic options,
or we can reach the help menu or the about menu. We can also quit the game, of course.

The main menu is easily added upon. It has an active_menu object that makes sure that we only display and update/handle the currently active
submenu.

If either the quit button is activated or the ESCAPE key is pressed, we quit the game.

"""

class OptionsMenu(scene.Scene):

	def __init__(self, window_surface, main_clock, title_logo = None):
		# Call the superconstructor.
		scene.Scene.__init__(self, window_surface, main_clock)

		# The next screen to be started when the gameloop ends.
		self.next_screen = None

		# Setup the logo and the variables needed to handle the animation of it.
		self.setup_logo(title_logo)
		self.logo_desired_position = ((settings.SCREEN_WIDTH - self.title_logo.get_width()) / 2, ((settings.SCREEN_HEIGHT - self.title_logo.get_height()) / 4))
		self.logo_transition = transition.Transition()
		self.logo_transition.speed = 120 * settings.GAME_SCALE

		# Setup all the menu buttons.
		self.setup_options_menu()

		# Setup the menu transitions.
		self.transition.setup_odd_even_transition(self.options_menu, True, True, False, False)

		# And finally, start the gameloop!
		self.gameloop()

	def setup_options_menu(self):
		self.options_menu = self.setup_menu()
		self.options_menu.add(textitem.TextItem("Graphics"), self.graphics)
		self.options_menu.add(textitem.TextItem("Sound"), self.sound)
		self.options_menu.add(textitem.TextItem("About"), self.about)
		self.options_menu.add(textitem.TextItem("Back"), self.back)
		self.options_menu.items[0].selected = True
		self.menu_list.append(self.options_menu)

	def graphics(self, item):
		graphicsmenu.GraphicsMenu(self.window_surface, self.main_clock, self.title_logo)
		self.transition.setup_odd_even_transition(self.options_menu, True, True, False, False)

	def sound(self, item):
		soundmenu.SoundMenu(self.window_surface, self.main_clock, self.title_logo)
		self.transition.setup_odd_even_transition(self.options_menu, True, True, False, False)

	def about(self, item):
		aboutmenu.AboutMenu(self.window_surface, self.main_clock)
		self.transition.setup_odd_even_transition(self.options_menu, True, True, False, False)

	def setup_logo(self, title_logo):
		if title_logo == None:
			# If the title_logo object doesn't exists, creates it and positions it.
			self.title_logo = logo.Logo()
			
			self.title_logo.x = (settings.SCREEN_WIDTH - self.title_logo.get_width()) / 2
			self.title_logo.y = ((settings.SCREEN_HEIGHT - self.title_logo.get_height()) / 4)
			
			self.title_logo.play()
		else:
			# Otherwise, we just save the given title_logo object
			self.title_logo = title_logo
	
	def setup_menu(self):
		# Returns a menu that is positioned in the center of the screen.
		return listmenu.ListMenu(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2)

	def back(self, item):
		self.done = True
		
		# Restore the logo's position.
		self.logo_desired_position = ((settings.SCREEN_WIDTH - self.title_logo.get_width()) / 2, ((settings.SCREEN_HEIGHT - self.title_logo.get_height()) / 4))

	def event(self, event):
		if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == JOYBUTTONDOWN and event.button in settings.JOY_BUTTON_BACK):
			# If the ESCAPE key or back button on gamepad is pressed, we go back a level in the menu system.
			self.back(None)

	def update(self):
		# Makes sure that the logo always moves to the desired posisition, and stays there.
		self.logo_transition.move_item_to_position(self.title_logo, self.logo_desired_position, self.main_clock)

		#  If the logo is in place, show the menu.
		if self.title_logo.x == self.logo_desired_position[0] and self.title_logo.y == self.logo_desired_position[1]:
			# Updates the menu transitions, and the currently active menu.
			self.transition.update(self.main_clock)
			self.options_menu.update(self.main_clock)

	def draw(self):
		# Every frame begins by filling the whole screen with the background color.
		self.window_surface.fill(settings.BACKGROUND_COLOR)

		# Draw the title logo.
		self.title_logo.draw(self.window_surface)

		# If the logo is in place, draw the currently active menu to the screen.
		if self.title_logo.x == self.logo_desired_position[0] and self.title_logo.y == self.logo_desired_position[1]:
			self.options_menu.draw(self.window_surface)

	def on_exit(self):
		if self.next_screen == aboutmenu.AboutMenu:
			# We start the help screen or the about screen and send them a reference to this instance, so they can return to it later.
			# We also setup the transitions, so when they return they transition in.
			self.transition.setup_odd_even_transition(self.options_menu, True, True, False, False)
			self.next_screen(self.window_surface, self.main_clock)

		# Else, we do nothing. This returns to the scene that created this scene.