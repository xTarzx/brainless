import pygame
from brain import Bot, Grid, Action, Direction, Projectile
from copy import deepcopy


from example_bots import DumbBot, BlindBot, RandomBot


class Brainless:
    BG_COLOR = pygame.Color("#131313")

    def __init__(self, grid: Grid, bot1: Bot, bot2: Bot):

        self.grid = grid
        self.bot_dirs = self.grid.place_bots(bot1, bot2)
        self.projectiles: list[Projectile] = []

        self.viewport = pygame.Surface(
            (self.grid.x_count * self.grid.cell_size, self.grid.y_count * self.grid.cell_size))

    def execute_action(self, bot: Bot, action: Action) -> pygame.Vector2:
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
        bot1_action = bot1.next_action(
            deepcopy(self.grid), self.bot_dirs, deepcopy(new_projectiles))
        bot2_action = bot2.next_action(
            deepcopy(self.grid), self.bot_dirs, deepcopy(new_projectiles))

        bot1_crashed = False
        bot2_crashed = False

        bot1_cell = self.grid.grid[self.grid.get_bot_cell_idx(bot1)]
        bot1_pos = pygame.Vector2(bot1_cell.x, bot1_cell.y)
        bot1_new_pos, bot1_projectiles = self.execute_action(
            bot1, bot1_action)

        bot2_new_pos, bot2_projectiles = self.execute_action(
            bot2, bot2_action)
        bot2_cell = self.grid.grid[self.grid.get_bot_cell_idx(bot2)]
        bot2_pos = pygame.Vector2(bot2_cell.x, bot2_cell.y)

        new_projectiles.extend(bot1_projectiles)
        new_projectiles.extend(bot2_projectiles)

        if bot1_new_pos.x < 0 or bot1_new_pos.x >= self.grid.x_count or bot1_new_pos.y < 0 or bot1_new_pos.y >= self.grid.y_count:
            bot1_crashed = True

        if bot2_new_pos.x < 0 or bot2_new_pos.x >= self.grid.x_count or bot2_new_pos.y < 0 or bot2_new_pos.y >= self.grid.y_count:
            bot2_crashed = True

        for projectile in new_projectiles:
            pos = pygame.Vector2(projectile.x, projectile.y)
            if pos == bot1_new_pos:
                bot1_crashed = True
            if pos == bot2_new_pos:
                bot2_crashed = True

        if bot1_new_pos == bot2_new_pos:
            print("CRASH")
            if bot1_action == Action.FORWARD:
                bot2_crashed = True
            if bot2_action == Action.FORWARD:
                bot1_crashed = True

        self.grid.cell_at(int(bot1_pos.x), int(bot1_pos.y)).bot = None
        self.grid.cell_at(int(bot1_new_pos.x), int(bot1_new_pos.y)).bot = bot1
        self.grid.cell_at(int(bot2_pos.x), int(bot2_pos.y)).bot = None
        self.grid.cell_at(int(bot2_new_pos.x), int(bot2_new_pos.y)).bot = bot2

        self.projectiles.clear()
        self.projectiles.extend(new_projectiles)

        if bot1_crashed or bot2_crashed:
            print(
                f"bot1_crashed ({bot1.name}): {bot1_crashed} {'loser' if bot1_crashed else ''}")
            print(
                f"bot2_crashed ({bot2.name}): {bot2_crashed} {'loser' if bot2_crashed else ''}")
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
bot1 = RandomBot("randombot1", (0, 111, 12), (248, 52, 38))
bot2 = RandomBot("randombot2", (0, 0, 111), (52, 38, 248))

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
