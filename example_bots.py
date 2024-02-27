import pygame
from brain import Bot, Action, Direction, Grid, Projectile, Cell

from random import choice


class DumbBot(Bot):
    def __init__(self, name="dumbbot", color=(0, 0, 111), face_color=(52, 38, 248)):
        super().__init__(name, color, face_color)

        self.rot = False

    def next_action(self,
                    grid: Grid,
                    bot_dirs: dict[str, Direction],
                    projectiles: list[Projectile]) -> Action:
        if self.rot:
            self.rot = False
            return Action.TURN_CW

        self.rot = True
        return Action.FORWARD


class BlindBot(Bot):
    def __init__(self, name="blindbot", color=(0, 0, 111), face_color=(52, 38, 248)):
        super().__init__(name, color, face_color)

        self.actions = [Action.TURN_CC, Action.SHOOT, Action.TURN_CC]
        self.curr = -1

    def next_action(self,
                    grid: Grid,
                    bot_dirs: dict[str, Direction],
                    projectiles: list[Projectile]) -> Action:
        self.curr += 1
        self.curr %= len(self.actions)
        return self.actions[self.curr]


class RandomBot(Bot):
    def __init__(self, name="randombot", color=(0, 0, 111), face_color=(52, 38, 248)):
        super().__init__(name, color, face_color)

    def next_action(self,
                    grid: Grid,
                    bot_dirs: dict[str, Direction],
                    projectiles: list[Projectile]) -> Action:
        return choice([Action.FORWARD, Action.TURN_CW, Action.TURN_CC, Action.SHOOT])


class ForwardBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def next_action(self,
                    grid: Grid,
                    bot_dirs: dict[str, Direction],
                    projectiles: list[Projectile]) -> Action:
        return Action.FORWARD


class IDKBot(Bot):
    def __init__(self, name="idkman", color=(12, 245, 133), face_color=(13, 85, 110)):
        super().__init__(name, color, face_color)

        self.fleeing = False

    def next_action(self,
                    grid: Grid,
                    bot_dirs: dict[str, Direction],
                    projectiles: list[Projectile]) -> Action:

        bot_cell: Cell = grid.grid[grid.get_bot_cell_idx(self.name)]
        bot_dir = bot_dirs[self.name]

        other_bot_name = None
        other_bot_dir = None

        for name, direction in bot_dirs.items():
            if name != self.name:
                other_bot_name = name
                other_bot_dir = direction
                break

        other_bot_cell: Cell = grid.grid[grid.get_bot_cell_idx(other_bot_name)]

        if self.fleeing:
            self.fleeing = False
            return Action.FORWARD

        for projectile in projectiles:
            if self.is_projectile_toward(bot_cell, projectile):
                if projectile.direction == bot_dir or projectile.direction == bot_dir.opposite():
                    self.fleeing = True
                    return choice([Action.TURN_CW, Action.TURN_CC])

                return Action.FORWARD

        if self.is_in_sight(bot_cell, bot_dir, other_bot_cell):
            return Action.SHOOT

        if bot_cell.y == other_bot_cell.y:
            match bot_dir:
                case Direction.UP:
                    if bot_cell.x < other_bot_cell.x:
                        return Action.TURN_CW
                    else:
                        return Action.TURN_CC
                case Direction.DOWN:
                    if bot_cell.x < other_bot_cell.x:
                        return Action.TURN_CC
                    else:
                        return Action.TURN_CW
                case _:
                    return choice([Action.TURN_CW, Action.TURN_CC])

        if bot_cell.x == other_bot_cell.x:
            match bot_dir:
                case Direction.LEFT:
                    if bot_cell.y < other_bot_cell.y:
                        return Action.TURN_CC
                    else:
                        return Action.TURN_CW
                case Direction.RIGHT:
                    if bot_cell.y < other_bot_cell.y:
                        return Action.TURN_CW
                    else:
                        return Action.TURN_CC
                case _:
                    return choice([Action.TURN_CW, Action.TURN_CC])

        next_pos = pygame.Vector2(bot_cell.x, bot_cell.y) + bot_dir.value

        if next_pos.x < 0 or next_pos.x >= grid.x_count or next_pos.y < 0 or next_pos.y >= grid.y_count:
            return choice([Action.TURN_CW, Action.TURN_CC])

        bot_next_cell: Cell = grid.cell_at(next_pos.x, next_pos.y)

        if bot_next_cell.pit:
            return choice([Action.TURN_CW, Action.TURN_CC])

        return Action.FORWARD

    def is_in_sight(self, bot_cell: Cell, bot_dir: Direction, other_bot_cell: Cell) -> bool:
        match bot_dir:
            case Direction.UP:
                if bot_cell.y > other_bot_cell.y and bot_cell.x == other_bot_cell.x:
                    return True
            case Direction.DOWN:
                if bot_cell.y < other_bot_cell.y and bot_cell.x == other_bot_cell.x:
                    return True
            case Direction.LEFT:
                if bot_cell.x > other_bot_cell.x and bot_cell.y == other_bot_cell.y:
                    return True
            case Direction.RIGHT:
                if bot_cell.x < other_bot_cell.x and bot_cell.y == other_bot_cell.y:
                    return True

        return False

    def is_projectile_toward(self, bot_cell: Cell, projectile: Projectile):
        match projectile.direction:
            case Direction.UP:
                if bot_cell.y < projectile.y and bot_cell.x == projectile.x:
                    return True
            case Direction.DOWN:
                if bot_cell.y > projectile.y and bot_cell.x == projectile.x:
                    return True
            case Direction.LEFT:
                if bot_cell.x < projectile.x and bot_cell.y == projectile.y:
                    return True
            case Direction.RIGHT:
                if bot_cell.x > projectile.x and bot_cell.y == projectile.y:
                    return True

        return False


class TestBot1(Bot):
    def __init__(self, name="testbot1", color=(0, 0, 111), face_color=(52, 38, 248)):
        super().__init__(name, color, face_color)

        self.shoot = True

    def next_action(self, grid: Grid, bot_dirs: dict[str, Direction], projectiles: list[Projectile]) -> Action:
        if self.shoot:
            self.shoot = False
            return Action.SHOOT
        return Action.WAIT


class TestBot2(Bot):
    def __init__(self, name="testbot2", color=(0, 0, 111), face_color=(248, 38, 31)):
        super().__init__(name, color, face_color)

        self.wait = True

    def next_action(self, grid: Grid, bot_dirs: dict[str, Direction], projectiles: list[Projectile]) -> Action:
        if self.wait:
            self.wait = False
            return Action.WAIT

        return Action.FORWARD
