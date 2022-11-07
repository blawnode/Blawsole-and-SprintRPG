import pygame, sys


# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
	print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
	sys.exit(-1)
else:
	print('[+] Game successfully initialised')


from BlawsoleUtility import *
from BlawsoleSnake import start_snake_game
from BlawsoleSprintRPG import start_sprint_game


class GameCartridge:
	def __init__(self, startFunction, name):
		self.startFunction = startFunction
		self.name = name


choiceToGameCartridge = {
		"1": GameCartridge(start_snake_game, "Snake"),
		"2": GameCartridge(start_sprint_game, "SprintRPG"),
	}


def ShowCartridgeSelectionMenu(instaClear, gameId, gameParameters):
	# Initialise game window
	pygame.display.set_caption('Blawsole')
	game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
	
	
	# FPS (frames per second) controller
	fps_controller = pygame.time.Clock()
	
	
	blawnodeImg = loadImageScaled("Blawnode.png", (64, 64))
	game_window.blit(blawnodeImg, (0, 640-64))
	pygame.display.update()  # Refresh game screen
	
	
	if instaClear or input("Clear screen?\n> ") == "yes":
		Clear()
	
	chooseGameMessage = "Choose 0 or 'exit' to... exit.\n"
	for choice, cartridge in choiceToGameCartridge.items():
		chooseGameMessage += "Choose " + choice + " for " + cartridge.name + "\n"
	
	choice = gameId
	exitChosen = False
	
	while True:  # Broken by <exitChosen>.
		while choice not in choiceToGameCartridge.keys():
			choice = input(chooseGameMessage).lower()
			if choice in ["0", "exit"]:
				exitChosen = True
				break
		
		if exitChosen:
			break
		
		cartridge = choiceToGameCartridge[choice]
		
		print("Loading " + cartridge.name + "...")
		pygame.display.set_caption(cartridge.name)
		cartridge.startFunction(game_window, fps_controller, gameParameters)
		print("Exited " + cartridge.name + ".")
		game_window.fill(black)
		pygame.display.flip()
		game_window.blit(blawnodeImg, (0, 640-64))
		pygame.display.update()  # Refresh game screen
		choice = None
	print("Hope that playing the Blawsole was fun!")


def main():
	print(f"Arguments count: {len(sys.argv)}")
	for i, arg in enumerate(sys.argv):
		print(f"Argument {i:>6}: {arg}")
	args = sys.argv[1:]  # Without the file name.
	
	validFlags = ["-clear", "-game=", "-level="]
	
	if len(args) > len(validFlags):
		raise Exception("Nah nah, there's too much arguments!"
		+ "\nFlags: -clear -game=GAMEID")
	
	instaClear = False
	gameId = None
	gameParameters = {}
	
	for arg in args:
		if arg == "-clear":
			instaClear = True
		elif arg.startswith("-game="):
			gameArg = arg[len("-game="):]
			if gameArg in choiceToGameCartridge.keys():
				gameId = gameArg
		elif arg.startswith("-level="):
			gameArg = arg[len("-level="):]
			gameParameters["level"] = gameArg
				
	
	ShowCartridgeSelectionMenu(instaClear, gameId, gameParameters)

if __name__ == "__main__":
    main()