__author__ = "Olof Karlsson"
__license__ = "All Rights Reserved"

import pygame, sys
from pygame.locals import *
import other.debug as debug
import other.useful as useful
import gui.textitem as textitem
import gui.logo as logo
import gui.menu as menu
import gui.gridmenu as gridmenu
import gui.coloritem as coloritem
import gui.transition as transition
import gui.traversal as traversal
import objects.groups as groups
import settings.settings as settings
import settings.graphics as graphics

class ConfirmationMenu:

	tint_color = pygame.Color(255, 255, 255, 128)

	def __init__(self, window_surface, main_clock, function_to_call, function_argument):
		# Store the game variables.
		self.window_surface = window_surface
		self.main_clock = main_clock

		# This is the function that will be called if the dialog is accepted.
		self.function_to_call = function_to_call

		# The argument we will use to call the function_to_call.
		self.function_argument = function_argument

		# If this is true when the gameloop ends, function_to_call will be called.
		self.accepted = False

		# Tint the window surface and set it as the background surface.
		self.background_surface = window_surface.copy()

		# The next screen to be started when the gameloop ends.
		self.next_screen = None

		# Configure the GUI.
		self.setup_menu()

		# Setup the menu transitions.
		self.setup_transitions()

		self.gameloop()

	def setup_menu(self):
		# Setup the menu.
		self.confirmation_menu = menu.Menu()
		self.confirmation_menu.add(textitem.TextItem("Yes"), self.accept)
		self.confirmation_menu.add(textitem.TextItem("No"), self.refuse)
		self.confirmation_menu.x = settings.SCREEN_WIDTH / 2
		self.confirmation_menu.y = (settings.SCREEN_HEIGHT - self.confirmation_menu.get_height()) / 2
		self.confirmation_menu.cleanup()

		# Set the default action to be to refuse.
		self.confirmation_menu.items[1].selected = True

		# Setup the textitem.
		self.confirmation_text = textitem.TextItem("Are you sure", pygame.Color(255, 255, 255))
		self.confirmation_text.x = (settings.SCREEN_WIDTH - self.confirmation_text.get_width()) / 2
		self.confirmation_text.y = self.confirmation_menu.y - (2 * self.confirmation_text.get_height())

	def setup_transitions(self):
		self.transitions = transition.Transition()
		self.transitions.setup_single_item_transition(self.confirmation_text, True, True, True, False)
		self.transitions.setup_single_item_transition(self.confirmation_menu.items[0], True, True, False, False)
		self.transitions.setup_single_item_transition(self.confirmation_menu.items[1], True, True, False, True)

	def accept(self, item):
		self.done = True
		self.accepted = True

	def refuse(self, item):
		self.done = True
		self.accepted = False

	def gameloop(self):
		self.done = False

		while not self.done:
			# Begin every frame by blitting the background surface.
			self.window_surface.blit(self.background_surface, (0, 0))
			
			for event in pygame.event.get():
				if event.type == QUIT:
					# If the window is closed, the game is shut down.
					sys.exit()
					pygame.quit()
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					# If the escape key is pressed, we call refuse.
					self.refuse(None)
				else:
					traversal.traverse_menus(event, [self.confirmation_menu])

			# Update and show the menu.
			self.show_menu()

			if settings.DEBUG_MODE:
				# Display various debug information.
				debug.Debug.display(self.window_surface, self.main_clock)

			pygame.display.update()
			
			# Finally, constrain the game to a set maximum amount of FPS.
			self.main_clock.tick(graphics.MAX_FPS)

		# The gameloop is over, so we either start the next screen or quit the game.
		self.on_exit()

	def show_menu(self):
		# Handle all transitions.
		self.transitions.update()

		# Draw the confirmation text.
		self.confirmation_text.draw(self.window_surface)

		# Update and draw the confirmation menu.
		self.confirmation_menu.update()
		self.confirmation_menu.draw(self.window_surface)

	def on_exit(self):
		# We're done, so we call the function_to_call if we should, otherwise we do nothing.
		if self.accepted:
			self.function_to_call(self.function_argument)