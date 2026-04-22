import os

class MazeVisualizer:
    def __init__(self, maze_data: list[list]) -> None:
        self.maze = maze_data
        self.show_path = False
        self.wall_color = "\033[0;32m"  # Verde por defecto para las paredes normales
        self.reset_color = "\033[0m"
        self.colors = {
            "red": "\033[0;31m",
            "green": "\033[0;32m",
            "blue": "\033[0;34m",
            "yellow": "\033[0;33m",
            "white": "\033[1;37m",
            "cyan": "\033[1;36m"
        }

    def update_data(self, new_maze_data: list[list]) -> None:
        """Actualiza la matriz del laberinto"""
        self.maze = new_maze_data

    def _get_wall_char(self, r, c) -> str:
        """Determina el carácter GRUESO (Heavy) según los vecinos"""
        rows = len(self.maze)
        cols = len(self.maze[0])
        
        # Función auxiliar: Consideramos pared tanto al '1' normal como a la 'P' del logo
        def is_wall(val):
            return val == 1 or val == 'P'

        # Detectar vecinos que son pared o logo
        up = r > 0 and is_wall(self.maze[r-1][c])
        down = r < rows - 1 and is_wall(self.maze[r+1][c])
        left = c > 0 and is_wall(self.maze[r][c-1])
        right = c < cols - 1 and is_wall(self.maze[r][c+1])

        # Lógica de conexión con caracteres GRUESOS
        if up and down and left and right: return "╋━"
        if up and down and right: return "┣━"
        if up and down and left:  return "┫ "
        if left and right and down: return "┳━"
        if left and right and up:   return "┻━"
        if up and right:   return "┗━"
        if up and left:    return "┛ "
        if down and right: return "┏━"
        if down and left:  return "┓ "
        if up or down:     return "┃ "
        if left or right:  return "━━"
        return "━━"

    def draw(self, path_coords=None) -> None:
        if path_coords is None:
            path_coords = set()

        os.system('cls' if os.name == 'nt' else 'clear')

        for r, row in enumerate(self.maze):
            line = ""
            for c, cell in enumerate(row):
                
                # 1. PRIORIDAD MÁXIMA: Especiales (Entrada y Salida)
                # Así nos aseguramos de que sus cuadrados de color nunca se borren
                if cell == 'E':
                    line += "\033[45m  \033[0m"
                elif cell == 'S':
                    line += "\033[41m  \033[0m"

                # 2. Camino de solución
                elif self.show_path and (r, c) in path_coords:
                    line += "\033[1;33m ●\033[0m"
                
                # 3. Paredes NORMALES
                elif cell == 1:
                    char = self._get_wall_char(r, c)
                    line += f"{self.wall_color}{char}{self.reset_color}"

                # 4. Logo 42 (Paredes integradas pero con color distinto)
                elif cell == 'P':
                    char = self._get_wall_char(r, c)
                    line += f"\033[1;36m{char}{self.reset_color}"

                # 5. Pasillos
                else:
                    line += "  "
            print(line)

    def change_color(self, color_name: str) -> None:
        if color_name in self.colors:
            self.wall_color = self.colors[color_name]