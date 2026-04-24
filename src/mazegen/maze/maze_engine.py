import random
from mazegen.maze.cell import Cell


class MazeGenerator:
    def __init__(self,
                 width: int,
                 height: int,
                 entry: tuple[int, int],
                 exit_pos: tuple[int, int],
                 perfect: bool = False,
                 seed: int | None = None
                 ) -> None:
        self.width: int = width
        self.height: int = height
        self.seed = seed
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit_pos
        self.perfect: bool = perfect

        self.grid: list[list[Cell]] = [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def _get_unvisited(self, current: Cell) -> list[tuple[str, Cell]]:
        neighbors: list[tuple[str, Cell]] = []
        x, y = current.x, current.y

        if y > 0 and not self.grid[y - 1][x].visited:
            neighbors.append(('N', self.grid[y - 1][x]))
        if y < self.height - 1 and not self.grid[y + 1][x].visited:
            neighbors.append(('S', self.grid[y + 1][x]))
        if x < self.width - 1 and not self.grid[y][x + 1].visited:
            neighbors.append(('E', self.grid[y][x + 1]))
        if x > 0 and not self.grid[y][x - 1].visited:
            neighbors.append(('W', self.grid[y][x - 1]))

        return neighbors

    def _gen_perfect_backtracker(self) -> None:
        start_x, start_y = self.entry
        current_cell: Cell = self.grid[start_y][start_x]
        current_cell.visited = True

        stack: list[Cell] = [current_cell]

        while stack:
            current_cell = stack[-1]
            neighbors = self._get_unvisited(current_cell)

            if neighbors:
                direction, next_cell = random.choice(neighbors)
                current_cell.remove_wall(next_cell, direction)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

    def generate_maze(self) -> None:
        """
        Calls the maze generation method, if a seed is provided
        it uses the provided seed
        """
        if self.seed is not None:
            random.seed(self.seed)

        # 1. Put the logo first
        self._inject_42_pattern()

        # 2. Generate the maze around it
        self._gen_perfect_backtracker()

        # 3. If necessary, we make it imperfect
        if not self.perfect:
            self.make_imperfect(0.1)

    def get_display_matrix(self) -> list[list]:
        """
        @Pablo
        """
        disp_width = self.width * 2 + 1
        disp_height = self.height * 2 + 1
        matrix: list[list[int | str]] = [
            [1 for _ in range(disp_width)] for _ in range(disp_height)
        ]

        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                my_y = y * 2 + 1
                my_x = x * 2 + 1

                # Lógica del Logo P
                if getattr(cell, 'is_in_pattern', False):
                    matrix[my_y][my_x] = 'P'
                    # Conectar logo hacia el sur
                    if y < self.height - 1 and getattr(
                        self.grid[y+1][x], 'is_in_pattern', False
                    ):
                        matrix[my_y + 1][my_x] = 'P'
                    # Conectar logo hacia el este
                    if x < self.width - 1 and getattr(
                        self.grid[y][x+1], 'is_in_pattern', False
                    ):
                        matrix[my_y][my_x + 1] = 'P'
                else:
                    if matrix[my_y][my_x] != 'P':
                        matrix[my_y][my_x] = 0

                # Lógica de paredes normales (solo si no somos logo)
                if not getattr(cell, 'is_in_pattern', False):
                    if not cell.walls['S'] and y < self.height - 1:
                        if not getattr(
                            self.grid[y+1][x], 'is_in_pattern', False
                        ):
                            matrix[my_y + 1][my_x] = 0

                    if not cell.walls['E'] and x < self.width - 1:
                        if not getattr(
                            self.grid[y][x+1], 'is_in_pattern', False
                        ):
                            matrix[my_y][my_x + 1] = 0

        # Put the entry and exit
        try:
            entry_cell = self.grid[self.entry[1]][self.entry[0]]
            exit_cell = self.grid[self.exit[1]][self.exit[0]]
            
            if getattr(entry_cell, 'is_in_pattern', False):
                raise ValueError("Entry can't be in logo space")
            
            if getattr(exit_cell, 'is_in_pattern', False):
                raise ValueError("Exit can't be in logo space")
            
            e_y, e_x = self.entry[1] * 2 + 1, self.entry[0] * 2 + 1
            matrix[e_y][e_x] = 'E'
            
            s_y, s_x = self.exit[1] * 2 + 1, self.exit[0] * 2 + 1
            matrix[s_y][s_x] = 'S'
        except IndexError:
            raise ValueError("Entry/Exit coordinates out of bounds")

        return matrix

    def _inject_42_pattern(self) -> None:
        """
        Inyecta un '42' en el centro. Al marcar las celdas como 'visited',
        el algoritmo de generación no las pisará ni romperá sus paredes,
        creando un bloque macizo alrededor.
        """
        # Minimum width and height needed for the '42' logo
        if self.width < 11 or self.height < 9:
            print("Not enough area for the '42' pattern!")
            return

        # '42' pattern (5 heigth x 7 width)
        # relative coordinates (y, x)
        pattern = [
            (0, 0), (0, 4), (0, 5), (0, 6),
            (1, 0), (1, 6),
            (2, 0), (2, 1), (2, 2), (2, 4), (2, 5), (2, 6),
            (3, 2), (3, 4),
            (4, 2), (4, 4), (4, 5), (4, 6)
        ]

        # Calculate center
        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2

        # Apply pattern
        for dy, dx in pattern:
            cell = self.grid[start_y + dy][start_x + dx]
            cell.visited = True
            cell.is_in_pattern = True

    def _would_create_2x2(self, x: int, y: int, direction: str) -> bool:
        """
        Checks if by destroying the wall in the current position,
        creates an area wider than 2x2 by asking their neighbours
        """
        c = self.grid[y][x]

        if direction == 'S':
            s = self.grid[y + 1][x]
            if x < self.width - 1:
                e = self.grid[y][x + 1]
                if not c.walls['E'] and not e.walls['S'] and not s.walls['E']:
                    return True
            if x > 0:
                w = self.grid[y][x - 1]
                if not c.walls['W'] and not w.walls['S'] and not s.walls['W']:
                    return True
        elif direction == 'E':
            e = self.grid[y][x + 1]
            if y < self.width - 1:
                s = self.grid[y + 1][x]
                if not c.walls['S'] and not s.walls['E'] and not e.walls['S']:
                    return True
            if y > 0:
                n = self.grid[y - 1][x]
                if not c.walls['N'] and not n.walls['E'] and not e.walls['N']:
                    return True
        return False

    def make_imperfect(self, chance: float = 0.1) -> None:
        """
        Takes the original grid and takes down random walls.
        It prevents the creation of 2x2 open areas, also
        respecting the '42' logo
        """
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                current_cell = self.grid[y][x]

                # Prevents not throwing walls next to the 42 logo
                if getattr(current_cell, 'is_in_pattern', False):
                    continue

                if y < self.height - 1 and current_cell.walls['S']:
                    next_cell = self.grid[y + 1][x]
                    if not getattr(
                        next_cell, 'is_in_pattern', False
                    ) and random.random() < chance:
                        if not self._would_create_2x2(x, y, 'S'):
                            current_cell.remove_wall(next_cell, 'S')

                if x < self.width - 1 and current_cell.walls['E']:
                    next_cell = self.grid[y][x + 1]
                    if not getattr(
                        next_cell, 'is_in_pattern', False
                    ) and random.random() < chance:
                        if not self._would_create_2x2(x, y, 'E'):
                            current_cell.remove_wall(next_cell, 'E')

    def get_grid(self) -> list[list[Cell]]:
        """
        Returns the full maze grid
        """
        return self.grid
