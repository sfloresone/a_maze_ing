
from collections import deque
from typing import Optional
from src.mazegen.maze.cell import Cell


class MazeSolver:
    def __init__(
            self,
            grid: list[list[Cell]],
            entry: tuple[int, int],
            exit: tuple[int, int]
            ) -> None:
        self.grid = grid
        self.entry = entry
        self.exit = exit

    def solve(self) -> str:

        if self.entry == self.exit:
            return ""

        queue: deque[tuple[int, int]] = deque([self.entry])

        came_from: dict[
            tuple[int, int],
            Optional[tuple[tuple[int, int], str]]
            ] = {self.entry: None}

        while queue:
            current_x, current_y = queue.popleft()
            if (current_x, current_y) == self.exit:
                break
            current_cell = self.grid[current_y][current_x]

            self._check_neighbor(
                current_cell,
                current_x,
                current_y, queue,
                came_from
                )

        return self._original_path(came_from)

    def _check_neighbor(
            self,
            cell: Cell,
            cell_x: int,
            cell_y: int,
            queue: deque[tuple[int, int]],
            came_from: dict[
            tuple[int, int],
            Optional[tuple[tuple[int, int], str]]
            ]
    ) -> None:
        """
        Checks the free neighbours walls and adds them to the queue
        """
        if not cell.walls['N']:
            next_pos = (cell_x, cell_y - 1)
            if next_pos not in came_from:
                queue.append(next_pos)
                came_from[next_pos] = ((cell_x, cell_y), 'N')

        if not cell.walls['E']:
            next_pos = (cell_x + 1, cell_y)
            if next_pos not in came_from:
                queue.append(next_pos)
                came_from[next_pos] = ((cell_x, cell_y), 'E')

        if not cell.walls['S']:
            next_pos = (cell_x, cell_y + 1)
            if next_pos not in came_from:
                queue.append(next_pos)
                came_from[next_pos] = ((cell_x, cell_y), 'S')

        if not cell.walls['W']:
            next_pos = (cell_x - 1, cell_y)
            if next_pos not in came_from:
                queue.append(next_pos)
                came_from[next_pos] = ((cell_x, cell_y), 'W')

    def _original_path(
            self,
            came_from: dict[
            tuple[int, int],
            Optional[tuple[tuple[int, int], str]]
            ]) -> str:
        """
        Travels through the 'came_from' dictionary, from entry
        to exit reconstructing the original string path
        """
        if self.exit not in came_from:
            return ""

        path = ""
        current = self.exit

        while came_from[current] is not None:
            previous = came_from[current]

            if previous is not None:
                prev_cell, direction = previous
                path += direction
                current = prev_cell

        return path[::-1]

    def get_path_coords(self, solution_str: str) -> set[tuple[int, int]]:
        """
        Convierte el string 'SSENE' en coordenadas (r, c) para el Visualizer
        """
        coords = set()
        curr_x, curr_y = self.entry

        # Añadir posición inicial (mapeada a 2n+1)
        coords.add((curr_y * 2 + 1, curr_x * 2 + 1))

        for move in solution_str:
            # 1. Calculamos hacia dónde vamos en el grid de Cells
            if move == 'N':
                curr_y -= 1
            elif move == 'S':
                curr_y += 1
            elif move == 'E':
                curr_x += 1
            elif move == 'W':
                curr_x -= 1

            # 2. Mapeamos la Cell y el "pasillo"
            #  intermedio a la matriz de dibujo
            draw_y, draw_x = curr_y * 2 + 1, curr_x * 2 + 1

            if move == 'N':
                coords.add((draw_y + 1, draw_x))
            elif move == 'S':
                coords.add((draw_y - 1, draw_x))
            elif move == 'E':
                coords.add((draw_y, draw_x - 1))
            elif move == 'W':
                coords.add((draw_y, draw_x + 1))

            coords.add((draw_y, draw_x))

        return coords
