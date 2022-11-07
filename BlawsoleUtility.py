import pygame, os


FPS = 30

# Game size
game_size_x = 64
game_size_y = 64

# Window size
frame_size_x = 640
frame_size_y = 640


# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
db32LightGray = pygame.Color(155, 173, 183)

# Fonts
fontPixel = pygame.font.Font('slkscrb.ttf', 16)

DIRECTION_LEFT = (-1,0)
DIRECTION_RIGHT = (1,0)
DIRECTION_UP = (0,1)
DIRECTION_DOWN = (0,-1)
directionVectors = [DIRECTION_LEFT, DIRECTION_UP, DIRECTION_RIGHT, DIRECTION_DOWN]


# https://stackoverflow.com/questions/497885/python-element-wise-tuple-operations-like-sum
# TODO OPTIONAL: Type testing.
def sumTuples(tuple1, tuple2):
	return tuple(item1 + item2 for item1, item2 in zip(tuple1, tuple2))


# 3^
# 2|
# 1|
# 0+-->x
#  0123
def printXYMatrix(matrix):
	try:
		for y in range(len(matrix[0])):
			for x in range(len(matrix)):
				print(matrix[x][len(matrix[0])-y-1], end='')
			print()
	except Exception as e:
		raise e


def loadImageScaled(path, size):
	image = pygame.image.load(path)
	image = pygame.transform.scale(image, size)
	return image


# TODO OPTIONAL: Typecheck
def PlaySFX(sfx):
	pygame.mixer.Sound.play(sfx)


Clear = lambda: os.system('cls')


def ShowText(game_window=None, text="ShowText()", color=black, font='times', size=24, pos=(0,0), antialiasing=True):
	"""Identical to show_text_system()."""
	ShowTextSystem(game_window, text, color, font, size, pos, antialiasing)


def ShowTextSystem(game_window=None, text="ShowTextSystem()", color=black, font='times', size=24, pos=(0,0), antialiasing=True):
	if not isinstance(font, str):
		raise Exception("ShowTextSystem() was called incorrectly - <font> must be a string.")
	ShowTextComplex(game_window, text, color, font, size, pos, antialiasing)


# The main difference between this and show_text_system is
#	the (incomplete) type checking default arguments.
def ShowTextCustom(game_window=None, text="ShowTextCustom()", color=black, font=fontPixel, scale=2, pos=(0,0), antialiasing=False):
	# TODO - Check that this is a FONT
	if isinstance(font, str):
		raise Exception("ShowTextCustom() was called incorrectly - <font> must be a pygame font.")
	ShowTextComplex(game_window, text, color, font, scale, pos, antialiasing)


def ShowTextComplex(game_window=None, text="ERROR #001 - THIS SHOULDN'T BE VISIBLE", color=black, font='times', size=24, pos=(0,0), antialiasing=True):
	if game_window is None:
		raise Exception("game_window mustn't be None.")

	if isinstance(font, str):
		score_font = pygame.font.SysFont(font, size)
		score_surface = score_font.render(text, antialiasing, color)
		score_rect = score_surface.get_rect()
		score_rect.midtop = pos
		game_window.blit(score_surface, score_rect)
		# pygame.display.flip()
	else:
		# Assumed: font is a FontObject, initialized with a custom font using pygame.font.Font().
		# In this case, the size turns into a *scale* instead.
		scaleX = size
		scaleY = size
		textSurfaceObj = font.render(text, antialiasing, color)
		textRectObj = textSurfaceObj.get_rect()
		textSurfaceObj = pygame.transform.scale(textSurfaceObj,
			(int(textRectObj[2] * scaleX), int(textRectObj[3] * scaleY)))
		textRectObj = textSurfaceObj.get_rect()
		textRectObj.center  = (pos[0], pos[1])
		game_window.blit(textSurfaceObj, textRectObj)


# TODO OPTIONAL: Typecheck <string>
def MultilineStringToMatrix(string):
	stringSplit = string.splitlines()
	size1 = len(stringSplit)
	size2 = len(stringSplit[0])
	return [[stringSplit[size1-j-1][i] for j in range(size1)] for i in range(size2)]