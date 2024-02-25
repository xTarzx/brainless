from __future__ import annotations
import pygame
from enum import Enum, auto


# Ait lemme explain this shit
# The objective of the game is to destroy your opponent's bot first
# Bots will get destroyed if:
#   - a projectile hits them
#   - rammed by another bot (driven into)
# The map is a grid defined by a continuous array of cells
# Your task is to make an 'AI'
# You do this by inheriting the Bot class and overriding the 'next_action' method (i recc you make it a diff file and import this for ease of use)
# You receive as arguments:
#   - the grid state
#   - the bots directions ( dict[ botname, direction ] )
# The method should return the next action your bot will perform
# TIP:
# You are free to override __init__, remember to initialize super class aswell (https://www.w3schools.com/python/python_inheritance.asp#:~:text=Use%20the%20super()%20Function)


class Direction(Enum):
    UP = pygame.Vector2(0, -1)
    DOWN = pygame.Vector2(0, 1)
    LEFT = pygame.Vector2(-1, 0)
    RIGHT = pygame.Vector2(1, 0)


class Action(Enum):
    WAIT = auto()
    FORWARD = auto()
    TURN_CC = auto()
    TURN_CW = auto()
    SHOOT = auto()


class Bot:
    def __init__(self, name, color, face_color):
        self.name = name
        self.color = color
        self.face_color = face_color

    def next_action(self, grid: Grid, bot_dirs: dict[str, Direction], projectiles: list[Projectile]) -> Action:
        return Action.WAIT

    def __eq__(self, other: Bot):
        return self.name == other.name


class Projectile:
    def __init__(self, x, y, direction: Direction):
        self.x = x
        self.y = y
        self.direction = direction

    def draw(self, surface: pygame.Surface, cell_size):
        pygame.draw.circle(surface, (255, 0, 0), (self.x*cell_size + cell_size//2,
                                                  self.y*cell_size + cell_size//2), cell_size//4)


class Cell:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.bot: Bot | None = None
        self.pit = False

    def draw(self, surface: pygame.Surface, bot_dirs: dict[str, Direction]):
        if self.pit:
            return
        if self.bot:
            pygame.draw.rect(surface, self.bot.color, (self.x * self.size,
                                                       self.y*self.size, self.size, self.size))

            direction = bot_dirs[self.bot.name]

            center_x = self.x*self.size + self.size//2
            center_y = self.y*self.size + self.size//2

            dist = self.size//4
            sz = self.size//8

            center_x += direction.value.x * dist
            center_y += direction.value.y * dist

            pygame.draw.circle(surface, self.bot.face_color,
                               (center_x, center_y), sz)
        else:
            pygame.draw.rect(surface, self.color, (self.x * self.size,
                                                   self.y*self.size, self.size, self.size))

        pygame.draw.rect(surface, (110, 110, 110), (self.x * self.size,
                         self.y*self.size, self.size, self.size), 1)


class Grid:
    def __init__(self, x, y, cell_size):
        self.x_count = x
        self.y_count = y
        self.cell_size = cell_size

        self.gen_grid()
        assert x * y == len(self.grid), "Grid size does not match"

    def gen_grid(self) -> list[Cell]:
        self.grid = [Cell(x, y, self.cell_size, (43, 43, 43))
                     for y in range(self.x_count) for x in range(self.y_count)]

    def cell_at(self, x, y) -> Cell:
        if x < 0 or x >= self.x_count or y < 0 or y >= self.y_count:
            None
        return self.grid[x + y * self.x_count]

    def cell_idx(self, x, y) -> int:
        return x + y * self.x_count

    def place_bots(self, bot1: Bot, bot2: Bot) -> dict[str, Direction]:
        self.cell_at(1, self.y_count//2).bot = bot1
        self.cell_at(self.x_count-2, self.y_count//2).bot = bot2

        return {bot1.name: Direction.RIGHT, bot2.name: Direction.LEFT}

    def draw(self, surface: pygame.Surface, bot_dirs: dict[str, Direction]):
        for cell in self.grid:
            cell.draw(surface, bot_dirs)

    def get_bot_cell_idx(self, bot: Bot) -> int | None:
        for idx, cell in enumerate(self.grid):
            if cell.bot is None:
                continue

            if cell.bot == bot:
                return idx
        return None
