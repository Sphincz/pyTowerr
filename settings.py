# Authors: Antonio Raimundo
# Partial credits to: Brandon Fong and Michael Ou

# Import pygame
import pygame as pg

# Game settings
ROWS = 15
COLS = 15
TILE_SIZE = 48
SCREEN_WIDTH = TILE_SIZE * COLS
SCREEN_HEIGHT = TILE_SIZE * ROWS
SIDE_PANEL = 300
FPS = 60
HEALTH = 5
TOTAL_WAVES = 3
GAME_MODE = "GENETIC_ALGORITHM"  # MANUAL, GENETIC_ALGORITHM, QLEARNING

# Enemies
SPAWN_COOLDOWN = 400
ENEMY_TYPES = {
    "zombie": {
        "health": 15,
        "speed": 2,
        "image": pg.image.load('assets/images/enemies/zombie.png'),
    },
    "warrior": {
        "health": 25,
        "speed": 3,
        "image": pg.image.load('assets/images/enemies/warrior.png'),
    },
}
ENEMY_SPAWN_DATA = [
    {
        # Wave 1
        "zombie": 10,
        "warrior": 0,
    },
    {
        # Wave 2
        "zombie": 15,
        "warrior": 5,
    },
    {
        # Wave 3
        "zombie": 25,
        "warrior": 15,
    }
]

# Towers
TOWER_LEVELS = 2
TOWER_TYPES = {
    "cannon1": {
        "range": [50, 100],
        "cooldown": [200, 2000],
        "damage": [1, 3],
        "image": pg.image.load('assets/images/towers/cannon1.png'),
    },
    "cannon2": {
        "range": [90, 120],
        "cooldown": [200, 2000],
        "damage": [3, 5],
        "image": pg.image.load('assets/images/towers/cannon2.png'),
    },
}
TOWER_POSITIONS = [
    {
        "id": 0,
        "type": "cannon1",
        "x": 11,
        "y": 2,
        "angle": -90
    },
    {
        "id": 1,
        "type": "cannon1",
        "x": 5,
        "y": 3,
        "angle": 90
    },
    {
        "id": 2,
        "type": "cannon1",
        "x": 3,
        "y": 8,
        "angle": -90
    },
    {
        "id": 3,
        "type": "cannon1",
        "x": 6,
        "y": 7,
        "angle": 90
    },
    {
        "id": 4,
        "type": "cannon1",
        "x": 12,
        "y": 11,
        "angle": -90
    },
    {
        "id": 5,
        "type": "cannon1",
        "x": 6,
        "y": 11,
        "angle": -90
    },
]

# Animation
ANIMATION_STEPS = 8
ANIMATION_DELAY = 15
