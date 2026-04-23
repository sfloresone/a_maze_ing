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

        # 1. Inyectamos el logo PRIMERO
        self._inject_42_pattern()

        # 2. Generamos el laberinto alrededor
        self._gen_perfect_backtracker()

        # 3. Hacemos imperfecto si es necesario
        if not self.perfect:
            self.make_imperfect(0.1)

    def get_display_matrix(self) -> list[list]:
        disp_width = self.width * 2 + 1
        disp_height = self.height * 2 + 1
        matrix = [[1 for _ in range(disp_width)] for _ in range(disp_height)]

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

        # Colocar Entrada y Salida
        try:
            e_y, e_x = self.entry[1] * 2 + 1, self.entry[0] * 2 + 1
            s_y, s_x = self.exit[1] * 2 + 1, self.exit[0] * 2 + 1
            matrix[e_y][e_x] = 'E'
            matrix[s_y][s_x] = 'S'
        except IndexError:
            pass

        return matrix

    def _inject_42_pattern(self) -> None:
        """
        Inyecta un '42' en el centro. Al marcar las celdas como 'visited',
        el algoritmo de generación no las pisará ni romperá sus paredes,
        creando un bloque macizo alrededor.

        !FALTA MOSTRAR UN MENSAJE DE ERROR EN CASO DE QUE NO CUMPLA DIMENSIONES
        """
        # Dimensión mínima para que el 42 quepa con algo de margen
        if self.width < 11 or self.height < 9:
            return

        # Patrón del '42' (5 celdas de alto x 7 de ancho)
        # Coordenadas relativas (y, x)
        pattern = [
            (0, 0), (0, 4), (0, 5), (0, 6),
            (1, 0), (1, 6),
            (2, 0), (2, 1), (2, 2), (2, 4), (2, 5), (2, 6),
            (3, 2), (3, 4),
            (4, 2), (4, 4), (4, 5), (4, 6)
        ]

        # Calcular el centro
        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2

        # Aplicar el patrón
        for dy, dx in pattern:
            cell = self.grid[start_y + dy][start_x + dx]
            cell.visited = True
            cell.is_in_pattern = True

    def make_imperfect(self, chance: float = 0.1) -> None:
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                current_cell = self.grid[y][x]

                # Evitar romper paredes que conecten con el logo 42
                if getattr(current_cell, 'is_in_pattern', False):
                    continue

                if y < self.height - 1 and current_cell.walls['S']:
                    next_cell = self.grid[y + 1][x]
                    if not getattr(
                        next_cell, 'is_in_pattern', False
                    ) and random.random() < chance:
                        current_cell.remove_wall(next_cell, 'S')

                if x < self.width - 1 and current_cell.walls['E']:
                    next_cell = self.grid[y][x + 1]
                    if not getattr(
                        next_cell, 'is_in_pattern', False
                    ) and random.random() < chance:
                        current_cell.remove_wall(next_cell, 'E')

    def get_grid(self) -> list[list[Cell]]:
        return self.grid
