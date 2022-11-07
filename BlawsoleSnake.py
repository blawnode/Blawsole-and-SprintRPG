# Built upon: https://gist.github.com/rajatdiptabiswas/bd0aaa46e975a4da5d090b801aba0611


import sys, time, random
from BlawsoleUtility import *


game_window = None
fps_controller = None
snakeScore = 0


def SnakeDrawGameOver():
	my_font = pygame.font.SysFont('times new roman', 90)
	game_over_surface = my_font.render('YOU DIED', True, red)
	game_over_rect = game_over_surface.get_rect()
	game_over_rect.midtop = (frame_size_x*0.5, frame_size_y*0.25)
	game_window.fill(black)
	game_window.blit(game_over_surface, game_over_rect)
	SnakeShowScore(red, 'times', 20, (frame_size_x*0.5, frame_size_y*0.8))
	pygame.display.flip()


def SnakeGameOver():
	SnakeDrawGameOver()
	
	time.sleep(1)
	ShowTextCustom(game_window, "Press any key to quit.", color=white, scale=2, pos=(frame_size_x/2, frame_size_y * 0.2))
	flicker_last_time = (pygame.time.get_ticks()) / 1000
	flicker_is_showing = True
	
	pygame.display.update()  # Refresh game screen
	
	while True:
		for event in pygame.event.get():
			# Whenever a key is pressed down
			if event.type == pygame.KEYDOWN:
				#pygame.quit()
				#sys.exit()
				return
		if (pygame.time.get_ticks()) / 1000 - flicker_last_time > 1:
			SnakeDrawGameOver()
			flicker_is_showing = not flicker_is_showing
			if flicker_is_showing:
				ShowTextCustom(game_window, "Press any key to quit.", color=white, scale=2, pos=(frame_size_x/2, frame_size_y * 0.2))
			pygame.display.update()  # Refresh game screen
			flicker_last_time = (pygame.time.get_ticks()) / 1000


# Score
def SnakeShowScore(color, font, size, pos=(frame_size_x * 0.5, frame_size_y * 0.5)):
	ShowText(game_window, 'Score : ' + str(snakeScore), color, font, size, pos)


# <gameParameters> is redundant in here.
# 	It is here because of Blawsole.py.
def start_snake_game(new_game_window, new_fps_controller, gameParameters):
	# Main logic
	global snakeScore, directionVectors, game_window, fps_controller
	game_window, fps_controller = new_game_window, new_fps_controller
	
	# Game variables
	snake_pos = [100, 50]
	snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
	
	food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
	food_spawn = True
	
	direction = 'DOWN'
	change_to = direction
	snakeScore = 0
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			# Whenever a key is pressed down
			elif event.type == pygame.KEYDOWN:
					# W -> Up; S -> Down; A -> Left; D -> Right
				if event.key == pygame.K_UP or event.key == ord('w'):
					change_to = 'UP'
				if event.key == pygame.K_DOWN or event.key == ord('s'):
					change_to = 'DOWN'
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					change_to = 'LEFT'
				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					change_to = 'RIGHT'
				# Esc -> Create event to quit the game
				if event.key == pygame.K_ESCAPE:
					pygame.event.post(pygame.event.Event(pygame.QUIT))
	
		# Making sure the snake cannot move in the opposite direction instantaneously
		if change_to == 'UP' and direction != 'DOWN':
			direction = 'UP'
		if change_to == 'DOWN' and direction != 'UP':
			direction = 'DOWN'
		if change_to == 'LEFT' and direction != 'RIGHT':
			direction = 'LEFT'
		if change_to == 'RIGHT' and direction != 'LEFT':
			direction = 'RIGHT'
	
		# Moving the snake
		if direction == 'UP':
			snake_pos[1] -= 10
		if direction == 'DOWN':
			snake_pos[1] += 10
		if direction == 'LEFT':
			snake_pos[0] -= 10
		if direction == 'RIGHT':
			snake_pos[0] += 10
	
		# Snake body growing mechanism
		snake_body.insert(0, list(snake_pos))
		if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
			snakeScore += 1
			food_spawn = False
		else:
			snake_body.pop()
	
		# Spawning food on the screen
		if not food_spawn:
			food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
		food_spawn = True
	
		# GFX
		game_window.fill(black)
		for pos in snake_body:
			# Snake body
			# .draw.rect(play_surface, color, xy-coordinate)
			# xy-coordinate -> .Rect(x, y, size_x, size_y)
			pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
	
		# Snake food
		pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
	
		# Game Over conditions
		# Getting out of bounds
		if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
			SnakeGameOver()
			return
		if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
			SnakeGameOver()
			return
		# Touching the snake body
		for block in snake_body[1:]:
			if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
				SnakeGameOver()
				return
	
		SnakeShowScore(white, 'consolas', 20, (frame_size_x/2, frame_size_y/1.25))
		pygame.display.update()  # Refresh game screen
		fps_controller.tick(FPS)  # Refresh rate
