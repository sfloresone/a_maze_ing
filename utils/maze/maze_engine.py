
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

        # self._make_imperfect
        if not self.perfect:
            self.make_imperfect(0.1)

        # Aqui habría que hacer un algoritmo extra para romper algunas paredes
        # if not self.perfect:
        # self._make_imperfect
        # Finalmente tendriamos que injectar "42" dentro de nuestro laberinto
        # si tiene las dimensiones suficientes, algo asi:
        # self._inject_42_pattern()


    def get_display_matrix(self) -> list[list]:
        """ Convierte el grid de objetos Cell en una matriz de 1s, 0s, E y S """
        # Tamaño ampliado para que las paredes ocupen su propia celda
        disp_width = self.width * 2 + 1
        disp_height = self.height * 2 + 1
        matrix = [[1 for _ in range(disp_width)] for _ in range(disp_height)]

        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                # Coordenada en la matriz de dibujo
                my_y = y * 2 + 1
                my_x = x * 2 + 1
                matrix[my_y][my_x] = 0

                # Si no hay pared al sur, abrimos el bloque de abajo
                if not cell.walls['S'] and y < self.height - 1:
                    matrix[my_y + 1][my_x] = 0
                
                # Si no hay pared este, abrimos el bloque de la derecha
                if not cell.walls['E'] and x < self.width - 1:
                    matrix[my_y][my_x + 1] = 0

                # Colocamos entrada y salida en los bordes de la matriz
                # Ajustamos las coordenadas de la config al sistema 2n+1
            try:
                e_y, e_x = self.entry[1] * 2 + 1, self.entry[0] * 2 + 1
                s_y, s_x = self.exit[1] * 2 + 1, self.exit[0] * 2 + 1
                
                matrix[e_y][e_x] = 'E'
                matrix[s_y][s_x] = 'S'
            except IndexError:
                raise ValueError("Error: The entry or exit is out of bounds.")
        
        return matrix


    def make_imperfect(self, chance: float = 0.1) -> None:
        """
        Function that allows us to add more exits to the original maze (by knocking down walls).
        """
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                current_cell = self.grid[y][x]

                # Intentar romper hacia el sur
                if y < self.height - 1 and current_cell.walls['S']:
                    if random.random() < chance:
                        next_cell = self.grid[y + 1][x]
                        current_cell.remove_wall(next_cell, 'S')
                
                # Intentar romper hacia el este
                if y < self.width - 1 and current_cell.walls['E']:
                    if random.random() < chance:
                        next_cell = self.grid[y][x + 1]
                        current_cell.remove_wall(next_cell, 'E')

    def _inject_42_pattern():
        pass

    def get_grid(self) -> list[list[Cell]]:
        return self.grid
