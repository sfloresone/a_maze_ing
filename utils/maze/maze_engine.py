
import random
from utils.parser.config_parser import MazeConfig
from utils.maze.cell import Cell


class MazeGenerator:
    def __init__(self, config: MazeConfig) -> None:
        self.width: int = config.width
        self.height: int = config.height
        self.entry: tuple[int, int] = config.entry
        self.exit: tuple[int, int] = config.exit
        self.perfect: bool = config.perfect

        self.grid: list[list[Cell]] = [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

    def _get_unvisited(self, current: Cell) -> list[tuple[str, Cell]]:
        neighbors: list[tuple[str, Cell]] = []
        x, y = current.x, current.y

        # North (y - 1)
        if y > 0 and not self.grid[y - 1][x].visited:
            neighbors.append(('N', self.grid[y - 1][x]))
        # South (y + 1)
        if y < self.height - 1 and not self.grid[y + 1][x].visited:
            neighbors.append(('S', self.grid[y + 1][x]))
        # East (x + 1)
        if x < self.width - 1 and not self.grid[y][x + 1].visited:
            neighbors.append(('E', self.grid[y][x + 1]))
        # Weast (x - 1)
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

            # Si hay vecinos por visitar
            if neighbors:
                # Si hay vecinos elegimos uno al azar
                direction, next_cell = random.choice(neighbors)
                # Tiramos la pared
                current_cell.remove_wall(next_cell, direction)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                # Si no hay vecinos, estamos en callejon sin salida
                # Hacemos backtrack, es decir retrocedemos
                stack.pop()

    def generate_maze(self) -> None:
        self._gen_perfect_backtracker()

        # Aqui habría que hacer un algoritmo extra para romper algunas paredes
        # if not self.perfect:
        # self._make_imperfect
        # Finalmente tendriamos que injectar "42" dentro de nuestro laberinto
        # si tiene las dimensiones suficientes, algo asi:
        # self._inject_42_pattern()


    def make_imperfect(self, chance: float = 0.1) -> None:
        """
        Function that allows us to add more exits to the original maze (by knocking down walls).
        """
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                if 

    def _inject_42_pattern():
        pass

    def get_grid(self) -> list[list[Cell]]:
        return self.grid
