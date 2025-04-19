import math

WIDTH = 1000
HEIGHT = 750
FPS = 4
INITIAL_BEINGS = 1000
SQUARE_SIZE = math.ceil(math.sqrt(INITIAL_BEINGS))
SQUARE_WIDTH = 720/SQUARE_SIZE
SCORES = {
    'fightWinScore': 50,
    'fightLoseScore': -100,
    'scareWinScore': 50,
    'threatWinScore': 40,
    'threatLoseScore': -5
}