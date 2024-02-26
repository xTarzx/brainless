from brain import Bot, Action, Direction, Grid, Projectile, Cell

from random import choice


class DumbBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__("dumbbot", (0, 0, 111), (52, 38, 248))

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
    def __init__(self, *args, **kwargs):
        super().__init__("blindbot", (0, 0, 111), (52, 38, 248))

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
