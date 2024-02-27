import pygame
from brain import Bot, Cell, Grid, Action, Direction, Projectile
from copy import deepcopy


from example_bots import TestBot1, TestBot2


class Brainless:
    BG_COLOR = pygame.Color("#131313")

    def __init__(self, grid: Grid, bot1: Bot, bot2: Bot):

        self.grid = grid
        self.bots = [bot1, bot2]
        self.bot_dirs = self.grid.place_bots(bot1, bot2)
        self.projectiles: list[Projectile] = []

        self.viewport = pygame.Surface(
            (self.grid.x_count * self.grid.cell_size, self.grid.y_count * self.grid.cell_size))

    def execute_action(self, bot: Bot, action: Action) -> tuple[pygame.Vector2, list[Projectile]]:
        """
        return new position and shoot
        """

        bot_cell_idx = self.grid.get_bot_cell_idx(bot)
        bot_cell = self.grid.grid[bot_cell_idx]

        new_pos = pygame.Vector2(bot_cell.x, bot_cell.y)
        direction = self.bot_dirs[bot.name]

        projectiles = []

        match action:
            case Action.FORWARD:
                new_pos += direction.value

            case Action.TURN_CC:
                match direction:
                    case Direction.UP:
                        self.bot_dirs[bot.name] = Direction.LEFT
                    case Direction.LEFT:
                        self.bot_dirs[bot.name] = Direction.DOWN
                    case Direction.DOWN:
                        self.bot_dirs[bot.name] = Direction.RIGHT
                    case Direction.RIGHT:
                        self.bot_dirs[bot.name] = Direction.UP

            case Action.TURN_CW:
                match direction:
                    case Direction.UP:
                        self.bot_dirs[bot.name] = Direction.RIGHT
                    case Direction.RIGHT:
                        self.bot_dirs[bot.name] = Direction.DOWN
                    case Direction.DOWN:
                        self.bot_dirs[bot.name] = Direction.LEFT
                    case Direction.LEFT:
                        self.bot_dirs[bot.name] = Direction.UP

            case Action.SHOOT:
                front = new_pos + direction.value
                projectiles.append(
                    Projectile(front.x, front.y, direction))

            case Action.WAIT:
                pass
            case action:
                assert False, f"Unknown action {action}"

        return new_pos, projectiles

    def update(self, dt) -> bool:
        new_projectiles = []
        for projectile in self.projectiles:
            new_projectile_pos = pygame.Vector2(
                projectile.x, projectile.y) + projectile.direction.value

            if new_projectile_pos.x < 0 or new_projectile_pos.x >= self.grid.x_count or new_projectile_pos.y < 0 or new_projectile_pos.y >= self.grid.y_count:
                continue

            new_projectiles.append(
                Projectile(new_projectile_pos.x, new_projectile_pos.y, projectile.direction))

        bots_actions: dict[str, Action] = {}
        bots_crashed: dict[str, bool] = {}
        bots_new_pos: dict[str, pygame.Vector2] = {}
        bots_projectiles: dict[str, list[Projectile]] = {}

        for bot in self.bots:
            bots_actions[bot.name] = bot.next_action(
                deepcopy(self.grid), self.bot_dirs, deepcopy(new_projectiles))

        for bot in self.bots:
            bot_cell: Cell = self.grid.grid[self.grid.get_bot_cell_idx(bot)]
            bot_pos = pygame.Vector2(bot_cell.x, bot_cell.y)
            bot_new_pos, bot_projectiles = self.execute_action(
                bot, bots_actions[bot.name])

            bots_new_pos[bot.name] = bot_new_pos
            bots_projectiles[bot.name] = bot_projectiles

        for projectiles in bots_projectiles.values():
            new_projectiles.extend(projectiles)

        for bot in self.bots:
            bot_new_pos = bots_new_pos[bot.name]

            if bot_new_pos.x < 0 or bot_new_pos.x >= self.grid.x_count or bot_new_pos.y < 0 or bot_new_pos.y >= self.grid.y_count:
                bots_crashed[bot.name] = True

            if self.grid.cell_at(int(bot_new_pos.x), int(bot_new_pos.y)).pit:
                bots_crashed[bot.name] = True

            for other_bot in self.bots:
                if bot.name != other_bot.name:
                    other_bot_new_pos = bots_new_pos[other_bot.name]
                    if bot_new_pos == other_bot_new_pos:
                        if bots_actions[bot.name] == Action.FORWARD:
                            bots_crashed[other_bot.name] = True

                        if bots_actions[other_bot.name] == Action.FORWARD:
                            bots_crashed[bot.name] = True

        for projectile in new_projectiles:
            pos = pygame.Vector2(projectile.x, projectile.y)

            for bot in self.bots:
                bot_new_pos = bots_new_pos[bot.name]
                if pos == bot_new_pos:
                    bots_crashed[bot.name] = True

        for bot in self.bots:
            bot_cell = self.grid.grid[self.grid.get_bot_cell_idx(bot)]
            bot_cell.bot = None

            bot_new_pos = bots_new_pos[bot.name]

            bot_new_cell = self.grid.cell_at(
                int(bot_new_pos.x), int(bot_new_pos.y))
            bot_new_cell.bot = bot

        self.projectiles.clear()
        self.projectiles.extend(new_projectiles)

        if any(bots_crashed.values()):
            for bot_name, crashed in bots_crashed.items():
                crashed = "crashed" if crashed else ""
                print(f"{bot_name} {crashed}")
            return False

        return True

    def render(self):
        self.viewport.fill(self.BG_COLOR)

        self.grid.draw(self.viewport, self.bot_dirs.copy())
        for projectile in self.projectiles:
            pygame.draw.circle(self.viewport, (255, 0, 0), (projectile.x * self.grid.cell_size + self.grid.cell_size // 2,
                                                            projectile.y * self.grid.cell_size + self.grid.cell_size // 2), self.grid.cell_size // 6)


window = pygame.display.set_mode(flags=pygame.RESIZABLE)

clock = pygame.time.Clock()
FPS = 60

grid = Grid(13, 13, 40)

bot1 = TestBot1()
bot2 = TestBot2()

brainless = Brainless(grid, bot1, bot2)

set_sim_speed = 0.18
sim_speed = set_sim_speed
sim = False

run = True
while run:
    dt = clock.tick(FPS)

    if sim:
        sim_speed -= dt/1000
        if sim_speed <= 0:
            run = brainless.update(dt)
            sim_speed = set_sim_speed

    window_width, window_height = window.get_size()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                run = brainless.update(dt)

            if event.key == pygame.K_p:
                sim = not sim
                sim_speed = set_sim_speed

    brainless.render()

    render_width, render_height = brainless.viewport.get_size()
    ratio = render_width / render_height

    if window_width / window_height > ratio:
        render_width = window_height * ratio
        render_height = window_height

    else:
        render_width = window_width
        render_height = window_width / ratio

    render_x = (window_width - render_width) // 2
    render_y = (window_height - render_height) // 2

    window.fill((0, 0, 0))
    window.blit(pygame.transform.scale(
        brainless.viewport, (render_width, render_height)),  (render_x, render_y))

    pygame.display.update()

pygame.quit()
