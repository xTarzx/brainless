import pygame


class Brainless:
    BG_COLOR = pygame.Color("#434343")
    GRID_COLOR = pygame.Color("#131313")
    GRID_THICK = 3

    def __init__(self, grid_x, grid_y, cell_size):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.cell_size = cell_size
        self.viewport = pygame.Surface(
            (self.grid_x * cell_size, self.grid_y * cell_size))

    def update(self, dt):
        pass

    def render(self):
        self.viewport.fill(self.BG_COLOR)

        for x in range(self.grid_x):
            pygame.draw.line(self.viewport, self.GRID_COLOR, (x * self.cell_size,
                             0), (x*self.cell_size, self.viewport.get_height()), self.GRID_THICK)
        for y in range(self.grid_y):
            pygame.draw.line(self.viewport, self.GRID_COLOR, (0,
                             y*self.cell_size), (self.viewport.get_width(), y*self.cell_size), self.GRID_THICK)


window = pygame.display.set_mode(flags=pygame.RESIZABLE)

clock = pygame.time.Clock()
FPS = 60

brainless = Brainless(13, 13, 40)

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
