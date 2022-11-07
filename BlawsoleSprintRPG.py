import pygame, sys
from time import time, sleep
import copy  # copy.deepcopy()
import pathlib  # pathlib.Path().resolve()
from BlawsoleUtility import *

game_window = None
fps_controller = None


def LoadLevel(levelID):
	levelPeasyDataText = """xxx
xEx
x x
xSx
xxx"""
	levelEmptyDataText = """xxxxxxx
x   xxx
x x xxx
xSx  Ex
xxxxxxx"""
	levelSimpleDataText = """xxxxxxx
x   xxx
x x xxx
xSx1 Ex
xxxxxxx"""

	levels={
		"1": levelPeasyDataText,
		"2": levelEmptyDataText,
		"3": levelSimpleDataText,
	}
	levelFiles={
		"premadeA": "Premade Level A.txt"
	}
	
	levelDataText = None
	
	if levelID is None:
		#levelDataText = levelSimpleDataText
		premadeLevelDataFile = open("Premade Level A.txt", "r")
		levelDataText = premadeLevelDataFile.read()
	elif levelID in levels.keys():
		levelDataText = levels[levelID]
	elif levelID in levelFiles.keys():
		premadeLevelDataFile = open(levelID, "r")
		levelDataText = premadeLevelDataFile.read()
	elif levelID.endswith(".txt"):
		# TODO OPTIONAL: Check that the file is an actual file.
		premadeLevelDataFile = open(levelID, "r")
		levelDataText = premadeLevelDataFile.read()
	else:
		raise Exception("Invalid level ID.")
	
	#levelDataTextSplit = levelDataText.splitlines()
	
	# TODO OPTIONAL: Ensure that the string is a valid level string.
	
	#levelDataMatrix = [[levelDataTextSplit[len(levelDataTextSplit)-j-1][i] for j in range(len(levelDataTextSplit))] for i in range(len(levelDataTextSplit[0]))]
	levelDataMatrix = MultilineStringToMatrix(levelDataText)
	# This way, I can access the matrix by x and y: levelDataMatrix[x][y]. And NOT be y and x.
	
	#printXYMatrix(levelDataMatrix)
	
	startPos = None
	directionVector = None
	exitPos = None
	
	# Find the start position, direction and exit position,
	# 	as well as validating level data.
	for y in range(len(levelDataMatrix[0])):
		for x in range(len(levelDataMatrix)):
			if ((x == 0 or x == len(levelDataMatrix) - 1 or
			y == 0 or y == len(levelDataMatrix[0]) - 1) and
			levelDataMatrix[x][y] != 'x'):
				raise Exception("INVALID LEVEL DATA: All edges of the level data must be 'x's.")
			if levelDataMatrix[x][y] == 'S':
				if startPos != None:
					raise Exception("INVALID LEVEL DATA: More than one start symbol ('S') were found.")
				startPos = (x, y)
				spacePos = None  # Only one nearby space is allowed.
				for deltaPos in directionVectors:
					testedPos = sumTuples(startPos, deltaPos)
					if levelDataMatrix[testedPos[0]][testedPos[1]] == ' ':
						if spacePos != None:
							raise Exception("INVALID LEVEL DATA: More than one space near the start were found.")
						spacePos = testedPos
						directionVector = deltaPos
				if spacePos == None:
					raise Exception("INVALID LEVEL DATA: No space near the start was found.")
			if levelDataMatrix[x][y] == 'E':
				if exitPos != None:
					raise Exception("INVALID LEVEL DATA: More than one exit symbol ('E') were found.")
				exitPos = (x, y)
	
	return levelDataMatrix, startPos, directionVector


def rotateDirection(directionVector, rotation):
	directionVectorIndex = directionVectors.index(directionVector)
	DIRECTION_AMOUNT = len(directionVectors)
	if rotation == "LEFT":
		directionVectorIndex = (directionVectorIndex - 1) % DIRECTION_AMOUNT
		return directionVectors[directionVectorIndex]
	elif rotation == "RIGHT":
		directionVectorIndex = (directionVectorIndex + 1) % DIRECTION_AMOUNT
		return directionVectors[directionVectorIndex]
	else:
		raise Exception("Invalid rotation value.")


class Enemy:	
	def __init__(self, moves, frames, default, far, specials=[]):
		# moves should be a list of either pygame keys, or ord('z')'s.
		self.moves = moves  # Possibly best implemented (performance-wise) by a queue.
		self.frames = frames
		self.SetImages(default, far, specials)
		self.currentFrame = 0
		self.pos = (-1, -1)
	
	# https://stackoverflow.com/questions/141545/how-to-overload-init-method-based-on-argument-type
	@classmethod
	# TODO OPTIONAL: Typechecking seems good here
	def fromenemy(cls, otherEnemy):
		"Initialize Enemy from another enemy"
		moves = copy.deepcopy(otherEnemy.moves)  # THIS enemy's moves will be altered.
		frames = otherEnemy.frames
		default = otherEnemy.spriteDefault
		far = otherEnemy.spriteFar
		specials = otherEnemy.spriteSpecials
		return cls(moves, frames, default, far, specials)
	
	def SetImages(self, default, far, specials=[]):
		self.spriteDefault = default
		self.spriteFar = far
		self.spriteSpecials = specials
	
	def GetCurrentSprite(self):
		#return self.spriteDefault if self.currentFrame == 0 else self.spriteSpecials[self.currentFrame - 1]
		return self.spriteDefault if self.frames[self.currentFrame] == 0 else self.spriteSpecials[self.frames[self.currentFrame - 1]]
	
	def PopMove(self):
		self.moves.pop(0)
		self.currentFrame += 1
	
	
	def SetPos(self, pos):
		self.pos = pos


def GameOver(victory, gameTimeElapsed):
	def DrawGameOver():
		game_window.fill(black)
		ShowTextCustom(game_window, "WIN!", white, fontPixel, 8, (frame_size_x*0.5, frame_size_y*0.25))
		ShowTextCustom(game_window, 'Time : ' + gameTimeElapsed, white, fontPixel, 2.5, (frame_size_x*0.5, frame_size_y*0.5))
		pygame.display.flip()
	
	def ShowPressAnyKey():
		ShowTextCustom(game_window, "Press any key to quit.", color=white, scale=1.75, pos=(frame_size_x*0.5, frame_size_y * 0.7))

	DrawGameOver()
	
	sleep(1)
	pygame.event.clear()  # Don't let any buffered inputs skip this screen!
	
	ShowPressAnyKey()
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
			DrawGameOver()
			flicker_is_showing = not flicker_is_showing
			if flicker_is_showing:
				ShowPressAnyKey()
			pygame.display.update()  # Refresh game screen
			flicker_last_time = (pygame.time.get_ticks()) / 1000


def start_sprint_game(new_game_window, new_fps_controller, gameParameters):
	# --- Initialize game data ---
	
	global game_window, fps_controller
	game_window, fps_controller = new_game_window, new_fps_controller
	
	levelDataMatrix, startPos, directionVector\
		= LoadLevel(gameParameters["level"] if "level" in gameParameters.keys() else None)
	
	FORWARD_KEYS = [pygame.K_UP, ord('w')]
	TURN_LEFT_KEYS = [pygame.K_LEFT, ord('a')]
	TURN_RIGHT_KEYS = [pygame.K_RIGHT, ord('d')]
	ATTACK_KEYS = [pygame.K_SPACE]
	DEFEND_KEYS = [ord('c'), ord('v'), ord('b'), ord('n'), ord('m')]
	
	BASE_IMAGE_SIZE = (400, 400)
	# assumed tile size: 400x400 (og is 40x40)
	imgPos = (120,120)  # calculation: (640-400)/2
	
	tileSpaceImg = loadImageScaled("TileSpace.png", BASE_IMAGE_SIZE)
	tileRightImg = loadImageScaled('TileRight.png', BASE_IMAGE_SIZE)
	tileLeftImg = loadImageScaled('TileLeft.png', BASE_IMAGE_SIZE)
	tileFrontRightImg = loadImageScaled('TileFrontRight.png', BASE_IMAGE_SIZE)
	tileFrontLeftImg = loadImageScaled('TileFrontLeft.png', BASE_IMAGE_SIZE)
	
	# In the perfect project, all the enemies would be placed in a folder.
	# 	For each enemy in the folder, an image would be added to a list.
	# 	Similarly the same about the tiles.
	
	enemiFarImg = loadImageScaled('EnemiFar.png', BASE_IMAGE_SIZE)
	enemiImg = loadImageScaled('Enemi.png', BASE_IMAGE_SIZE)
	
	brutoFarImg = loadImageScaled('BrutoFar.png', BASE_IMAGE_SIZE)
	brutoImg = loadImageScaled('Bruto.png', BASE_IMAGE_SIZE)
	brutoWeakImg = loadImageScaled('BrutoWeak.png', BASE_IMAGE_SIZE)
	
	tileToEnemy = {
		"1" : Enemy([ATTACK_KEYS], [0], enemiImg, enemiFarImg),
		"2": Enemy([DEFEND_KEYS, ATTACK_KEYS], [0, 1], brutoImg, brutoFarImg, [brutoWeakImg])
	}
	enemyTiles = tileToEnemy.keys()
	currentEnemy = None
	
	# --- SFX Loading ---
	
	sfxFolderName = "sfx\\"
	
	sfxFolderNameThreeangle = sfxFolderName + r"Threeangle SFX.ftm" + "\\"
	sfxStepPath = sfxFolderNameThreeangle + "Threeangle SFX - Track 04 (Button Hover).wav"
	sfxOuchPath = sfxFolderNameThreeangle + "Threeangle SFX - Track 05 (QM).wav"
	sfxLootPath = sfxFolderNameThreeangle + "Threeangle SFX - Track 10 (Bonus HP).wav"
	sfxAttackPath = sfxFolderNameThreeangle + "Threeangle SFX - Track 11 (Target Shatter).wav"
	
	sfxFolderNameEchoes = sfxFolderName + r"Echoes of the Void.ftm (Threeangle version)" + "\\"
	sfxUISelectPath = sfxFolderNameEchoes + "Button Hover.wav"
	sfxFadeOutPath = sfxFolderNameEchoes + "Mixed SFX T15 - Screen Fade Out.wav"
	sfxFadeInPath = sfxFolderNameEchoes + "Mixed SFX T16 - Screen Fade In.wav"
	sfxWinPath = sfxFolderNameEchoes + "Mixed SFX T17 - Note Pick Up.wav"
	
	sfxGrrrPath = sfxFolderName + "Grrr.wav"
	sfxChainPath = sfxFolderName + "GG SFX - Track 01 (Chain).wav"
	
	sfxStep = pygame.mixer.Sound(sfxStepPath)
	sfxOuch = pygame.mixer.Sound(sfxOuchPath)
	sfxWin = pygame.mixer.Sound(sfxWinPath)
	sfxAttack = pygame.mixer.Sound(sfxAttackPath)
	
	sfxUISelect = pygame.mixer.Sound(sfxUISelectPath)
	sfxFadeOut = pygame.mixer.Sound(sfxFadeOutPath)
	sfxFadeIn = pygame.mixer.Sound(sfxFadeInPath)
	sfxLoot = pygame.mixer.Sound(sfxLootPath)
	
	sfxGrrr = pygame.mixer.Sound(sfxGrrrPath)
	sfxChain = pygame.mixer.Sound(sfxChainPath)
	
	PLAY_SOUND_FOREVER = -1
	
	#pygame.mixer.music.load('jazz.wav')
	#pygame.mixer.music.play(PLAY_SOUND_FOREVER)
	#pygame.mixer.music.stop()
	#pygame.mixer.music.pause()
	#pygame.mixer.music.unpause()
	
	def Hit(enemy):
		BOOL_IS_DEAD = True
		
		#print("Hit!")
		PlaySFX(sfxAttack)
		enemy.PopMove()
		
		if len(enemy.moves) == 0:
			#print("Arrrrg, I'm ded")
			enemyPos = enemy.pos
			levelDataMatrix[enemyPos[0]][enemyPos[1]] = ' '  # TODO OPTIONAL: Or potentially, loot!
			enemy = None
			return enemy
		return enemy
	
	
	def AttemptToTurn(directionVector, direction):
		if direction not in ["RIGHT", "LEFT"]:
			raise Exception("Incorrect call to AttemptToTurn() - <direction> must be either \"RIGHT\" or \"LEFT\".")
		
		newDirectionVector = rotateDirection(directionVector, direction)
		turnPos = sumTuples(startPos, newDirectionVector)
		turnTile = levelDataMatrix[turnPos[0]][turnPos[1]]
		if turnTile != 'x':
			# Turn.
			directionVector = newDirectionVector
			return directionVector, True
		else:
			# SprintRPG incorrectness damage.
			print("Can't turn there!")
			return directionVector, False
	
	
	# --- Main logic ---
	
	PlaySFX(sfxChain)  # Like in SprintRPG! :D
	startTime = time()
	
	doUpdate = True
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				#pygame.quit()
				#sys.exit()
				return
			# Whenever a key is pressed down
			elif event.type == pygame.KEYDOWN:
				# Esc -> Create event to quit the game
				if event.key == pygame.K_ESCAPE:
					pygame.event.post(pygame.event.Event(pygame.QUIT))
				
				if currentEnemy != None:  # Fight!!!
					currentMove = currentEnemy.moves[0]
					
					if event.key in FORWARD_KEYS:
						print("FORWARD")
						
						if event.key in currentMove:
							currentEnemy = Hit(currentEnemy)
						else:
							#print("Ouch!")
							PlaySFX(sfxOuch)
						doUpdate = True
					elif event.key in TURN_LEFT_KEYS:
						print("LEFT")
						
						if event.key in currentMove:
							currentEnemy = Hit(currentEnemy)
						else:
							#print("Ouch!")
							PlaySFX(sfxOuch)
						doUpdate = True
					elif event.key in TURN_RIGHT_KEYS:
						print("RIGHT")
						
						if event.key in currentMove:
							currentEnemy = Hit(currentEnemy)
						else:
							#print("Ouch!")
							PlaySFX(sfxOuch)
						doUpdate = True
					elif event.key in ATTACK_KEYS:
						print("ATTACK")
						
						if event.key in currentMove:
							currentEnemy = Hit(currentEnemy)
						else:
							#print("Ouch!")
							PlaySFX(sfxOuch)
						doUpdate = True
					elif event.key in DEFEND_KEYS:
						print("DEFEND")
						
						if event.key in currentMove:
							currentEnemy = Hit(currentEnemy)
						else:
							#print("Ouch!")
							PlaySFX(sfxOuch)
						doUpdate = True
				else:  # Sprint!!!
					if event.key in FORWARD_KEYS:
						# Attempt to go forward.
						frontPos = sumTuples(startPos, directionVector)
						frontTile = levelDataMatrix[frontPos[0]][frontPos[1]]
						if frontTile != 'x':
							levelDataMatrix[startPos[0]][startPos[1]] = 'x' # Ensures that the player cannot return back, by turning twice. Like how you can't go back in SprintRPG.
							startPos = frontPos
							PlaySFX(sfxStep)
							doUpdate = True
					elif event.key in TURN_LEFT_KEYS:
						directionVector, doUpdate = AttemptToTurn(directionVector, "LEFT")
					elif event.key in TURN_RIGHT_KEYS:
						directionVector, doUpdate = AttemptToTurn(directionVector, 	"RIGHT")
					elif event.key in ATTACK_KEYS:
						print("Can't attack. Maybe play a nice animation?")
						doUpdate = True
					elif event.key in DEFEND_KEYS:
						print("Can't defend. Maybe play a nice animation?")
						doUpdate = True
		
		newTile = levelDataMatrix[startPos[0]][startPos[1]]
		frontPos = sumTuples(startPos, directionVector)
		frontTile = levelDataMatrix[frontPos[0]][frontPos[1]]
		
		reachedExit = newTile == 'E'
		if reachedExit:
			print("KUDOS!!!")
			PlaySFX(sfxWin)
			GameOver(victory=True, gameTimeElapsed=gameTimeElapsed)
			return
		
		if doUpdate:
			#print("Update!")
			
			# --- Enemy spotting ---
			if frontTile in enemyTiles:
				spottedEnemy = tileToEnemy[frontTile]
				
				if currentEnemy is None:
					#print("Enemy found!!: " + frontTile)
					currentEnemy = Enemy.fromenemy(spottedEnemy)
					currentEnemy.SetPos(frontPos)
					PlaySFX(sfxGrrr)
			
			# --- GFX ---
			game_window.fill(db32LightGray)
			
			leftDirection = rotateDirection(directionVector, "LEFT")
			rightDirection = rotateDirection(directionVector, "RIGHT")
			
			# --- Maze rooms GFX ---
			if newTile == 'E':
				#print("KUDOS!!!")
				#PlaySFX(sfxWin)
				#return
				pass
			elif frontTile != 'x':
				# Space!
				
				frontLeftPos = sumTuples(frontPos, leftDirection)
				frontLeftTile = levelDataMatrix[frontLeftPos[0]][frontLeftPos[1]]
				frontRightPos = sumTuples(frontPos, rightDirection)
				frontRightTile = levelDataMatrix[frontRightPos[0]][frontRightPos[1]]
				if (frontLeftTile == 'x') == (frontRightTile == 'x'):
					if frontLeftTile == 'x':
						game_window.blit(tileSpaceImg, imgPos)
					else:
						raise Exception("There can't be two spaces in both the front-adjacent tiles!")
				elif frontLeftTile == 'x':
					# There's something to the front-right!
					game_window.blit(tileFrontRightImg, imgPos)
				else:
					# There's something to the front-left!
					game_window.blit(tileFrontLeftImg, imgPos)
			else:
				# Wall. Does a tile to my left or right have a space? It has to!
				leftPos = sumTuples(startPos, leftDirection)
				leftTile = levelDataMatrix[leftPos[0]][leftPos[1]]
				rightPos = sumTuples(startPos, rightDirection)
				rightTile = levelDataMatrix[rightPos[0]][rightPos[1]]
				if (leftTile == 'x') == (rightTile == 'x'):
					raise Exception("EXACTLY ONE of the front-adjacent or adjacent tiles must be a wall."
					+ "\nProbably, the player made an illegal turn?")
				elif leftTile == 'x':
					# There's something to the right!
					game_window.blit(tileRightImg, imgPos)
				else:
					# There's something to the left!
					game_window.blit(tileLeftImg, imgPos)
			
			# --- Enemy GFX ---
			if frontTile in enemyTiles:
				#print("Enemy found!!: " + frontTile)
				enemySprite = currentEnemy.GetCurrentSprite()
				#enemySprite = currentEnemy.spriteDefault
				game_window.blit(enemySprite, imgPos)
			else:
				# There's no enemy in front of us. What about a far one?
				if frontTile != 'x':
					frontFrontPos = sumTuples(frontPos, directionVector)
					frontFrontTile = levelDataMatrix[frontFrontPos[0]][frontFrontPos[1]]
					if frontFrontTile in enemyTiles:
						#print("Far enemy found!: " + frontFrontTile)
						enemySprite = tileToEnemy[frontFrontTile].spriteFar
						game_window.blit(enemySprite, imgPos)

#		SnakeShowScore(white, 'consolas', 20, (frame_size_x/2, frame_size_y/1.25))
			ShowTextCustom(game_window, "SprintRPG", color=white, scale=3, pos=(frame_size_x*0.5, frame_size_y * 0.1))
			doUpdate = False
		pygame.draw.rect(game_window, db32LightGray, pygame.Rect(frame_size_x*0.2, frame_size_y*0.85, frame_size_x*0.6, frame_size_y * 0.1))
		gameTimeElapsed = format(time() - startTime, '.3f')
		ShowTextCustom(game_window, gameTimeElapsed, color=white, scale=2, pos=(frame_size_x*0.5, frame_size_y*0.9))
		
		pygame.display.update()  # Refresh game screen
		fps_controller.tick(FPS)  # Refresh rate
