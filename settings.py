import pygame
import persistence
import sys
from objective import ObjectiveManager
from pathlib import Path

def init():
    pygame.init()

    # Window
    global WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_DIMENSIONS, SCREEN, CLOCK
    WINDOW_WIDTH, WINDOW_HEIGHT = 1275, 690
    WINDOW_DIMENSIONS = (WINDOW_WIDTH, WINDOW_HEIGHT)
    SCREEN = pygame.display.set_mode(WINDOW_DIMENSIONS)
    CLOCK = pygame.time.Clock()

    # Assets
    global ICONS, SKINS, BACKGROUND_IMG
    ICONS = {
        'exit':                 get_resource_path('src/exit.png'),
        'coin':                 get_resource_path('src/coin.png'),
        'bomb':                 get_resource_path('src/bomb.png'),
        'health_potion':        get_resource_path('src/health_potion.png'),
        'max_health_potion':    get_resource_path('src/max_health_potion.png'),
        'reduce_speed_potion':  get_resource_path('src/reduce_speed_potion.png'),
        'buttonRight':          get_resource_path('src/buttonRight.png'),
        'buttonLeft':           get_resource_path('src/buttonLeft.png'),
        'start':                get_resource_path('src/start.png'),
        'lobby':                get_resource_path('src/lobby.png'),
        'chest':                get_resource_path('src/chest.png'),
    }
    SKINS = {
        'cookie': get_resource_path('src/cookie.png'),
        'tower':  get_resource_path('src/tower.png'),
    }
    BACKGROUND_IMG = pygame.image.load(get_resource_path('src/background.png')).convert()

    # Game state
    global points, session_high, health, max_health
    global selected_skin, high_score, _persisted
    points = session_high = 0
    max_health = 3
    health = max_health
    selected_skin = 'cookie'

    _persisted = persistence.load()
    high_score = _persisted.get('high_score', 0)

    # Sprite groups
    global LOBBY_SPRITES, GAME_SPRITES, BUTTONS
    global COINS, BOMBS, CHESTS, OBSTACLES
    global HEALTH_POTIONS, MAX_HEALTH_POTIONS, REDUCE_SPEED_POTIONS
    LOBBY_SPRITES     = pygame.sprite.Group()
    GAME_SPRITES      = pygame.sprite.Group()
    BUTTONS           = pygame.sprite.Group()
    COINS             = pygame.sprite.Group()
    BOMBS             = pygame.sprite.Group()
    HEALTH_POTIONS    = pygame.sprite.Group()
    MAX_HEALTH_POTIONS = pygame.sprite.Group()
    REDUCE_SPEED_POTIONS = pygame.sprite.Group()
    CHESTS            = pygame.sprite.Group()
    OBSTACLES         = pygame.sprite.Group()

    # FSM states
    global STATE_LOBBY, STATE_PLAY, STATE_QUIT, GAME_STATE
    STATE_LOBBY = 'LOBBY'
    STATE_PLAY  = 'PLAY'
    STATE_QUIT  = 'QUIT'
    GAME_STATE  = STATE_LOBBY

    # Objectives
    from objective import ObjectiveManager, make_collect_objective

    # Example: collect 50 coins → spawn a chest + +1 max health
    def reward_collect_50():
        from game_elements import Chest, MaxHealthPotion, ReduceSpeedPotion
        sw, sh = WINDOW_DIMENSIONS
        Chest.spawn(GAME_SPRITES, CHESTS, position=(sw//2, sh//2), reward_specs=[
        (MaxHealthPotion, 1),    # spawn 1 max health potions
        (ReduceSpeedPotion, 1),  # spawn 1 speed potion
    ])

    ObjectiveManager.register(
        make_collect_objective(10, reward_fn=reward_collect_50)
    )

def change_points(delta):
    global points, session_high
    points += delta
    session_high = max(session_high, points)

def change_health(delta):
    global health
    health = max(0, min(max_health, health + delta))
    
def change_max_health(delta):
    global max_health
    max_health = max(0, max_health + delta)

def save_high_score():
    global high_score, _persisted
    if session_high > high_score:
        high_score = session_high
        _persisted['high_score'] = high_score
        persistence.save(_persisted)

def change_state(state):
    global GAME_STATE
    GAME_STATE = state

def reset():
    global points, session_high, health, max_health
    points = session_high = 0
    health = max_health = 3
    GAME_SPRITES.empty()
    LOBBY_SPRITES.empty()
    COINS.empty()
    BOMBS.empty()
    MAX_HEALTH_POTIONS.empty()
    HEALTH_POTIONS.empty()
    REDUCE_SPEED_POTIONS.empty()
    CHESTS.empty()
    OBSTACLES.empty()
    
def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False) and hasattr(sys, "_MEIPASS"):
        return (Path(sys._MEIPASS) / relative_path).resolve()
    return (Path(__file__).parent / relative_path).resolve()
