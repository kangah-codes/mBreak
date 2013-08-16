__author__ = "Olof Karlsson"
__license__ = "All Rights Reserved"

import pygame
import math
import random
import other.useful as useful
import objects.paddle as paddle
import objects.particle as particle
import objects.trace as trace
import objects.shadow as shadow
import objects.groups as groups
import settings.settings as settings
import settings.graphics as graphics

def convert():
	Ball.image.convert()

class Ball(pygame.sprite.Sprite):

	# Load the image file here, so any new instance of this class doesn't have to reload it every time, they can just copy the surface.
	image = pygame.image.load("res/ball/ball.png")

	# Initialize the mixer (so we can load a sound) and load the sound effect.
	pygame.mixer.init(44100, -16, 2, 2048)
	sound_effect = pygame.mixer.Sound("res/sounds/ball_hit_wall2.wav")

	# Standard values. These will be used unless any other values are specified per instance of this class.
	width = image.get_width() * settings.GAME_SCALE
	height = image.get_height() * settings.GAME_SCALE
	speed = 1 * settings.GAME_SCALE
	max_speed = 3 * settings.GAME_SCALE
	damage = 10
	spin_speed_strength = 0.05 # Not used, but exists for balancing purposes.
	spin_angle_strength = 0.09
	least_allowed_vertical_angle = 0.21 # Exists to prevent the balls from getting stuck bouncing up and down in the middle of the gamefield.
	trace_spawn_rate = 32
	particle_spawn_amount = 3

	# Scale image to match the game scale.
	image = pygame.transform.scale(image, (width, height))

	def __init__(self, x, y, angle, owner):
		# We start by calling the superconstructor.
		pygame.sprite.Sprite.__init__(self)

		# Create the rect used for collision detection, position etc.
		self.rect = pygame.rect.Rect(x, y, Ball.width, Ball.height)

		# Keep track of x and y as floats, for preciseness sake (rect keeps track of x,y as ints)
		self.x = x
		self.y = y

		# Keep track of the balls position in the previous frame, used for collision handling.
		self.previous = pygame.rect.Rect(self.x, self.y, Ball.width, Ball.height)

		# Set the angle variable.
		self.angle = angle

		# Set maximum speed of the ball.
		self.max_speed = Ball.max_speed

		# Set the speed variable.
		self.speed = Ball.speed
		
		# Store the owner.
		self.owner = owner

		# Create the image attribute that is drawn to the surface.
		self.image = Ball.image.copy()

		# Colorize the image. We save a reference to the parents color in our own variable, so  that 
		# classes and modules that want to use our color do not have to call us.owner.color
		self.color = self.owner.color
		useful.colorize_image(self.image, self.color)

		# If collided is True, the ball sound is played.
		self.collided = False

		# Setup the trace time keeping variable.
		self.trace_spawn_time = 0
		
		# Create a shadow.
		self.shadow = shadow.Shadow(self)

		# Store the ball in the owners ball_group and the main ball_group.
		self.owner.ball_group.add(self)
		groups.Groups.ball_group.add(self)

		# Create an effect group to handle effects on this ball.
		self.effect_group = pygame.sprite.Group()

	def destroy(self):
		# This should be called when the ball is to be destroyed. It will take care of killing itself and anything affecting it completely.
		self.kill()
		self.shadow.kill()
		for effect in self.effect_group:
			effect.kill()

	def update(self, main_clock):
		self.collided = False

		# Check collision with paddles.
		self.check_collision_paddles()
				
		# Check collision with other balls.
		self.check_collision_balls()

		# Check collision with blocks.
		self.check_collision_blocks()

		# Check collision with powerups.
		self.check_collision_powerups()

		# Here we check if the angle of the ball is in the restricted areas. We do this to make sure that the balls don't get stuck
		# bouncing up and down in the middle of the gamefield, since that makes for a very boring game.
		if self.angle > (math.pi / 2) - Ball.least_allowed_vertical_angle and self.angle < (math.pi / 2) + Ball.least_allowed_vertical_angle:
			if self.angle > (math.pi / 2):
				self.angle = (math.pi / 2) + Ball.least_allowed_vertical_angle
			elif self.angle < (math.pi / 2):
				self.angle = (math.pi / 2) - Ball.least_allowed_vertical_angle
			else:
				# If the angle is EXACTLY pi/2, we just randomly decide what angle to "nudge" the ball to.
				self.angle += random.randrange(-1, 2, 2) * Ball.least_allowed_vertical_angle
		elif self.angle > ((3 * math.pi) / 2) - Ball.least_allowed_vertical_angle and self.angle < ((3 * math.pi) / 2) + Ball.least_allowed_vertical_angle:			
			if self.angle > ((3 * math.pi) / 2):
				self.angle = ((3 * math.pi) / 2) + Ball.least_allowed_vertical_angle
			elif self.angle < ((3 * math.pi) / 2):
				self.angle = ((3 * math.pi) / 2) - Ball.least_allowed_vertical_angle
			else:
				# If the angle is EXACTLY 3pi/2, we just randomly decide what angle to "nudge" the ball to.
				self.angle += random.randrange(-1, 2, 2) * Ball.least_allowed_vertical_angle

		# Constrain angle to 0 < angle < 2pi. Even though angles over 2pi or under 0 work fine when translating the angles to x and y positions, 
		# such angles mess with our ability to calculate other stuff. So we just make sure that the angle is between 0 and 2pi.
		if self.angle > (2 * math.pi):
			self.angle = self.angle - (2 * math.pi)
		elif self.angle < 0:
			self.angle = (2 * math.pi) + self.angle

		# Make sure that speed isn't over max_speed.
		if self.speed > self.max_speed:
			self.speed = self.max_speed

		# Move the ball with speed in consideration.
		self.x = self.x + (math.cos(self.angle) * self.speed)
		self.y = self.y + (math.sin(self.angle) * self.speed)
		self.rect.x = self.x
		self.rect.y = self.y

		# Check collision with x-edges.
		if self.rect.x < settings.LEVEL_X:
			self.hit_wall()

			# Reverse angle on x-axis.
			self.angle = math.pi - self.angle

			# Constrain ball to screen size.
			self.x = settings.LEVEL_X
			self.rect.x = self.x
		elif self.rect.x + self.rect.width > settings.LEVEL_MAX_X:
			self.hit_wall()

			# Reverse angle on x-axis.
			self.angle = math.pi - self.angle

			# Constrain ball to screen size.
			self.x = settings.LEVEL_MAX_X - self.rect.width			
			self.rect.x = self.x

		# Check collision with y-edges.
		if self.rect.y < settings.LEVEL_Y:
			self.hit_wall()

			# Reverse angle on y-axis.
			self.angle = -self.angle

			# Constrain ball to screen size.
			self.y = settings.LEVEL_Y
			self.rect.y = self.y
		elif self.rect.y + self.rect.height > settings.LEVEL_MAX_Y:
			self.hit_wall()
			# Reverse angle on y-axis.
			self.angle = -self.angle

			# Constrain ball to screen size.
			self.y = settings.LEVEL_MAX_Y - self.rect.height
			self.rect.y = self.y

		# If it's time, spawn a trace.
		self.trace_spawn_time += main_clock.get_time()
		if self.trace_spawn_time >= Ball.trace_spawn_rate:
			if graphics.TRACES:
				trace.Trace(self)
				self.trace_spawn_time = 0

		# If we have collided with anything, play the sound effect.
		if self.collided:
			Ball.sound_effect.play()

	def hit_wall(self):
		# Spawn some particles.
		self.spawn_particles()

		# Tell all the effects that we've just hit a wall.
		for effect in self.effect_group:
			effect.on_hit_wall()

		self.collided = True

	def calculate_spin(self, paddle):
		# We determine the velocity of the paddle with regards to the game scale.
		velocity_y = paddle.velocity_y / settings.GAME_SCALE

		# Use the velocity to calculate the spin.
		if self.angle <= (math.pi / 2):
			self.angle = self.angle - (velocity_y * Ball.spin_angle_strength)
		elif self.angle <= math.pi:
			self.angle = self.angle + (velocity_y * Ball.spin_angle_strength)
		elif self.angle <= (3 * math.pi) / 2:
			self.angle = self.angle + (velocity_y * Ball.spin_angle_strength)
		elif self.angle <= (2 * math.pi):
			self.angle = self.angle - (velocity_y * Ball.spin_angle_strength)

	def place_left_of(self, other):
		self.x = other.rect.left - self.rect.width - 1
		self.rect.x = self.x

	def place_right_of(self, other):
		self.x = other.rect.right + 1
		self.rect.x = self.x

	def place_over(self, other):
		self.y = other.rect.top - self.rect.height - 1
		self.rect.y = self.y

	def place_below(self, other):
		self.y = other.rect.bottom + 1
		self.rect.y = self.y

	def spawn_particles(self):
		for _ in range(0, Ball.particle_spawn_amount):
			angle = self.angle + random.uniform(-0.20, 0.20)
			retardation = self.speed / 24.0
			alpha_step = 5
			particle.Particle(self.x + self.rect.width / 2, self.y + self.rect.height / 2, self.rect.width / 4, self.rect.height / 4, angle, self.speed, retardation, self.color, alpha_step)

	def check_collision_paddles(self):
		paddle_collide_list = pygame.sprite.spritecollide(self, groups.Groups.paddle_group, False)
		for paddle in paddle_collide_list:
			self.hit_paddle(paddle)
			if self.rect.bottom >= paddle.rect.top and self.rect.top < paddle.rect.top:
				# Top side of paddle collided with. Compare with edges:
				if paddle.rect.left - self.rect.left > paddle.rect.top - self.rect.top:
					# The ball collides more with the left side than top side.
					self.hit_left_side_of_paddle(paddle)
				elif self.rect.right - paddle.rect.right > paddle.rect.top - self.rect.top:
					# The ball collides more with the right side than top side.
					self.hit_right_side_of_paddle(paddle)
				else:
					# The ball collides more with the top side than any other side.
					if self.angle < math.pi:
						self.angle = -self.angle

					# Place ball on top of the paddle.
					self.place_over(paddle)
			elif self.rect.top <= paddle.rect.bottom and self.rect.bottom > paddle.rect.bottom:
				# Bottom side of paddle collided with. Compare with edges:
				if paddle.rect.left - self.rect.left > self.rect.bottom - paddle.rect.bottom:
					# The ball collides more with the left side than top side.
					self.hit_left_side_of_paddle(paddle)
				elif self.rect.right - paddle.rect.right > self.rect.bottom - paddle.rect.bottom:
					# The ball collides more with the right side than top side.
					self.hit_right_side_of_paddle(paddle)
				else:
					# The ball collides more with the bottom side than any other side.
					if self.angle > math.pi:
						self.angle = -self.angle

					# Place ball beneath the paddle.
					self.place_below(paddle)
			elif self.rect.right >= paddle.rect.left and self.rect.left < paddle.rect.left:
				# Left side of paddle collided with.
				self.hit_left_side_of_paddle(paddle)
			elif self.rect.left <= paddle.rect.right and self.rect.right > paddle.rect.right:
				# Right side of paddle collided with.
				self.hit_right_side_of_paddle(paddle)

	def hit_paddle(self, paddle):
		self.spawn_particles()

		# Tell all the effects that we've just hit a paddle.
		for effect in self.effect_group:
			effect.on_hit_paddle(paddle)

		self.collided = True

	def hit_left_side_of_paddle(self, paddle):
		# Calculate spin, and then reverse angle.
		self.calculate_spin(paddle)
		if self.angle < (math.pi / 2) or self.angle > ((3 * math.pi) / 2):
			self.angle = math.pi - self.angle

		# Place ball to the left of the paddle.
		self.place_left_of(paddle)

	def hit_right_side_of_paddle(self, paddle):
		# Calculate spin, and then reverse angle.
		self.calculate_spin(paddle)
		if self.angle > (math.pi / 2) and self.angle < ((3 * math.pi) / 2):
			self.angle = math.pi - self.angle

		# Place ball to the right of the paddle.
		self.place_right_of(paddle)

	def check_collision_balls(self):
		groups.Groups.ball_group.remove(self)
		ball_collide_list = pygame.sprite.spritecollide(self, groups.Groups.ball_group, False)
		for ball in ball_collide_list:
			self.spawn_particles()
			self.hit_ball(ball)
			if self.rect.bottom >= ball.rect.top and self.rect.top < ball.rect.top:
				# Top side of ball collided with. Compare with edges:
				if ball.rect.left - self.rect.left > ball.rect.top - self.rect.top:
					# The ball collides more with the left side than top side.
					# Place ball to the left of the ball.
					self.place_left_of(ball)
				elif self.rect.right - ball.rect.right > ball.rect.top - self.rect.top:
					# The ball collides more with the right side than top side.
					# Place ball to the right of the ball.
					self.place_right_of(ball)
				else:
					# Place ball on top of the ball.
					self.place_over(ball)
			elif self.rect.top <= ball.rect.bottom and self.rect.bottom > ball.rect.bottom:
				# Bottom side of ball collided with.
				if ball.rect.left - self.rect.left > self.rect.bottom - ball.rect.bottom:
					# The ball collides more with the left side than top side.
					# Place ball to the left of the ball.
					self.place_left_of(ball)
				elif self.rect.right - ball.rect.right > self.rect.bottom - ball.rect.bottom:
					# The ball collides more with the right side than top side.
					# Place ball to the right of the ball.
					self.place_right_of(ball)
				else:
					# The ball collides more with the bottom side than any other side.
					# Place ball beneath the ball.
					self.place_below(ball)
			elif self.rect.right >= ball.rect.left and self.rect.left < ball.rect.left:
				# Left side of ball collided with.
				# Place ball to the left of the ball.
				self.place_left_of(ball)
			elif self.rect.left <= ball.rect.right and self.rect.right > ball.rect.right:
				# Right side of ball collided with.
				# Place ball to the right of the ball.
				self.place_right_of(ball)

			# Handle self.
			delta_x = self.rect.centerx - ball.rect.centerx
			delta_y = self.rect.centery - ball.rect.centery
			self.angle = math.atan2(delta_y, delta_x)

			# Handle other ball.
			delta_x = ball.rect.centerx - self.rect.centerx
			delta_y = ball.rect.centery - self.rect.centery
			ball.angle = math.atan2(delta_y, delta_x)
		groups.Groups.ball_group.add(self)

	def hit_ball(self, ball):
		# Tell all the effects that we've just hit another ball.
		for effect in self.effect_group:
			effect.on_hit_ball(ball)

		self.collided = True

	def check_collision_blocks(self):
		blocks_collided_with = pygame.sprite.spritecollide(self, groups.Groups.block_group, False)
		block_information = {}
		for block in blocks_collided_with:
			# Determine what side of the block we've collided with.
			if self.rect.bottom >= block.rect.top and self.rect.top < block.rect.top:
				# Top side of block collided with. Compare with edges:
				if block.rect.left - self.rect.left > block.rect.top - self.rect.top:
					# The ball collides more with the left side than top side.
					block_information[block] = "left"
				elif self.rect.right - block.rect.right > block.rect.top - self.rect.top:
					# The ball collides more with the right side than top side.
					block_information[block] = "right"
				else:
					# The ball collides more with the top side than any other side.
					block_information[block] = "top"
			elif self.rect.top <= block.rect.bottom and self.rect.bottom > block.rect.bottom:
				# Bottom side of block collided with.
				if block.rect.left - self.rect.left > self.rect.bottom - block.rect.bottom:
					# The ball collides more with the left side than top side.
					block_information[block] = "left"
				elif self.rect.right - block.rect.right > self.rect.bottom - block.rect.bottom:
					# The ball collides more with the right side than top side.
					block_information[block] = "right"
				else:
					# The ball collides more with the bottom side than any other side.
					block_information[block] = "bottom"
			elif self.rect.right >= block.rect.left and self.rect.left < block.rect.left:
				# Left side of block collided with.
				block_information[block] = "left"
			elif self.rect.left <= block.rect.right and self.rect.right > block.rect.right:
				# Right side of block collided with.
				block_information[block] = "right"

		# If we've only hit one block, we don't need to check so much. Just check which side we've collided with and act accordingly.
		if len(block_information) == 1:
			# Check what side we've hit that block and act accordingly.
			for block, side in block_information.iteritems():
				if side == "top":
					self.hit_top_side_of_block(block)
				elif side == "left":
					self.hit_left_side_of_block(block)
				elif side == "right":
					self.hit_right_side_of_block(block)
				elif side == "bottom":
					self.hit_bottom_side_of_block(block)
		# If we've hit two blocks, we need to check what combination of sides we've hit, to determine how to act.
		elif len(block_information) == 2:
			# Setup a few help lists to more easily determine how to act.
			block_list = []
			side_list = []
			for block, side in block_information.iteritems():
				block_list.append(block)
				side_list.append(side)

			# Are the two hit blocks side by side?
			if block_list[0].y == block_list[1].y:
				# Check if we've hit the top side of either block.
				if "top" in side_list:
					self.hit_top_side_of_block(block_list[0])
				elif "bottom" in side_list:
					self.hit_bottom_side_of_block(block_list[0])
			# Are the two blocks hit above/below each other?
			elif block_list[0].x == block_list[1].x:
				# Check what side we've hit, and act accordingly.
				if "left" in side_list:
					self.hit_left_side_of_block(block_list[0])
				elif "right" in side_list:
					self.hit_right_side_of_block(block_list[0])
			# Are the two blocks hit diagonal of each other?
			else:
				for block, side in block_information.iteritems():
					if side == "top":
						self.hit_top_side_of_block(block)
					elif side == "left":
						self.hit_left_side_of_block(block)
					elif side == "right":
						self.hit_right_side_of_block(block)
					elif side == "bottom":
						self.hit_bottom_side_of_block(block)
		# If we've hit three blocks, it's a little bit more complex. We have a lot of cases to handle.
		elif len(block_information) == 3:
			# Setup a few help lists to more easily determine how to act.
			block_list = []
			side_list = []
			for block, side in block_information.iteritems():
				block_list.append(block)
				side_list.append(side)

			# Here we're meticulously going through every possible combination and acting accordingly.
			# We also damage each block separately, since we cannot be sure what block we've "really"
			# hit until we've checked.
			if block_list[0].y == block_list[1].y:
				self.check_block_collisions(block_list[0], block_list[1], block_list[2], side_list[2])
			elif block_list[1].y == block_list[2].y:
				self.check_block_collisions(block_list[1], block_list[2], block_list[0], side_list[0])
			elif block_list[2].y == block_list[0].y:
				self.check_block_collisions(block_list[2], block_list[0], block_list[1], side_list[1])

	def check_block_collisions(self, block_one, block_two, block_three, block_three_side):
		if block_three_side == "left":
			self.hit_left_side_of_block(block_three)
		else:
			self.hit_right_side_of_block(block_three)

		if block_three.y > block_one.y:
			if block_one.x > block_two.x:
				self.hit_bottom_side_of_block(block_one)
			else:
				self.hit_bottom_side_of_block(block_two)
		else:
			if block_one.x > block_two.x:
				self.hit_top_side_of_block(block_one)
			else:
				self.hit_top_side_of_block(block_two)

	def hit_block(self, block):
		# We've hit a block, so spawn a particle, damage that block and set collision to True.
		self.spawn_particles()

		# If the block owner and the ball owner is the same, we deal a reduced amount of damage (for balance purposes).
		if block.owner == self.owner:
			block.on_hit(Ball.damage / 2.0)
		else:
			block.on_hit(Ball.damage)

		# Tell all the effects that we've just hit a block.
		for effect in self.effect_group:
			effect.on_hit_block(block)

		self.collided = True

	def hit_top_side_of_block(self, block):
		# Reverse angle.
		if self.angle < math.pi:
			self.hit_block(block)
			self.angle = -self.angle

		# Place ball on top of the block.
		self.place_over(block)

	def hit_left_side_of_block(self, block):
		# Reverse angle.
		if self.angle < (math.pi / 2) or self.angle > ((3 * math.pi) / 2):
			self.hit_block(block)
			self.angle = math.pi - self.angle

		# Place ball to the left of the block.
		self.place_left_of(block)

	def hit_right_side_of_block(self, block):
		# Reverse angle.
		if self.angle > (math.pi / 2) and self.angle < ((3 * math.pi) / 2):
			self.hit_block(block)
			self.angle = math.pi - self.angle

		# Place ball to the right of the block.
		self.place_right_of(block)

	def hit_bottom_side_of_block(self, block):
		# Reverse angle.
		if self.angle > math.pi:
			self.hit_block(block)
			self.angle = -self.angle

		# Place ball below the block.
		self.place_below(block)

	def check_collision_powerups(self):
		powerup_collide_list = pygame.sprite.spritecollide(self, groups.Groups.powerup_group, False)
		for powerup in powerup_collide_list:
			powerup.hit(self)
