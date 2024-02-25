from brain import Grid


class RoundMap(Grid):
    def __init__(self, x, y, cell_size):
        super().__init__(x, y, cell_size)

        for x in range(13):
            for y in range(13):
                if (x-6)**2 + (y-6)**2 < 16:
                    self.cell_at(x, y).pit = True
