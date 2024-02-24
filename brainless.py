import pygame
from brain import Bot, Grid, Action, Direction


class DumbBot(Bot):
    def next_action(self, grid: Grid, bot_dirs: dict[str, Direction]) -> Action:
        return Action.FORWARD


class Brainless:
    BG_COLOR = pygame.Color("#131313")

    def __init__(self, grid: Grid, bot1: Bot, bot2: Bot):

        self.grid = grid
        self.bot_dirs = self.grid.place_bots(bot1, bot2)

        self.viewport = pygame.Surface(
            (self.grid.x_count * self.grid.cell_size, self.grid.y_count * self.grid.cell_size))

    def update(self, dt):
        pass

    def render(self):
        self.viewport.fill(self.BG_COLOR)

        self.grid.draw(self.viewport, self.bot_dirs.copy())


window = pygame.display.set_mode(flags=pygame.RESIZABLE)

clock = pygame.time.Clock()
FPS = 60

grid = Grid(13, 13, 40)
bot1 = Bot("Bot1", (111, 0, 0), (214, 15, 36))
bot2 = DumbBot("Bot2", (0, 0, 111), (52, 38, 248))

brainless = Brainless(grid, bot1, bot2)

run = True
while run:
    dt = clock.tick(FPS)
    window_width, window_height = window.get_size()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    brainless.update(dt)
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
