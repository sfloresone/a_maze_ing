import os
from utils.maze.maze_engine import MazeGenerator
from utils.parser.config_parser import MazeConfig


class MazeVisualizer:
    def __init__(self, maze_data: list[list]) -> None:
        self.maze = maze_data
        self.show_path = False
        self.wall_color = "\033[1;37m"
        self.reset_color = "\033[0m"
        self.colors = {
            "red": "\033[0;31m",
            "green": "\033[0;32m",
            "blue": "\033[0;34m",
            "yellow": "\033[0;33m",
            "white": "\033[1;37m"
        }

    def update_data(self, new_maze_data: list[list]) -> None:
        """Nos permite actualizar el laberinto sin crear un nuevo objeto"""
        self.maze = new_maze_data

    def draw(self, path_coords=None) -> None:
        if path_coords is None:
            path_coords = set()

        os.system('cls' if os.name == 'nt' else 'clear')

        for r, row in enumerate(self.maze):
            line = ""
            for c, cell in enumerate(row):
                # 1. Prioridad: Mostrar el camino (Solution Path)
                if self.show_path and (r, c) in path_coords:
                    line += "\033[0;33m.\033[0m"
                
                # 2. Paredes
                elif cell == 1:
                    line += f"{self.wall_color}██{self.reset_color}"

                # 3. Entrada
                elif cell == 'E':
                    line += "\033[0;32mE\033[0m"

                # 4. Salida
                elif cell == 'S':
                    line += "\033[0;31mS\033[0m"

                # 5. Pasillos vacíos
                else:
                    line += "  "  # IMPORTANTE: Espacio para que no se deforme
            print(line)

    def change_color(self, color_name: str) -> None:
        if color_name in self.colors:
            self.wall_color = self.colors[color_name]

    def create_42_logo(self):
        pass


def main() -> None:
   # Inicializamos configuración y generador
    config = MazeConfig(width=15, height=10, perfect=False)
    
    # Iniciamos generador
    gen = MazeGenerator(config)
    gen.generate_maze()
    
    # IMPORTANTE: Usamos el "traductor" que mencionamos antes
    # para convertir objetos Cell en una matriz de 1s y 0s
    # Iniciamos visualizador
    maze_viz = MazeVisualizer(gen.get_display_matrix())

    while True:
        maze_viz.draw()
        print("\n=== A-Maze-Ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path")
        print("3. Change colors")
        print("4. Quit")

        choice = input("\nChoice? (1-4): ")

        if choice == "1":
            # Aqui vendra backtracking recursivo
            gen = MazeGenerator(config)
            gen.generate_maze()
            maze_viz.update_data(gen.get_display_matrix())

        elif choice == "2":
            maze_viz.show_path = not maze_viz.show_path

        elif choice == "3":
            new_color = input("Color (red/green/blue/yellow/white): ").lower()
            maze_viz.change_color(new_color)

        elif choice == "4":
            break


if __name__ == "__main__":
    main()
