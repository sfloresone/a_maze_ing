
import sys
from utils.parser.config_parser import MazeConfig
from utils.maze.maze_engine import MazeGenerator
from utils.maze.maze_visualizer import MazeVisualizer
from test_file import print_pretty_maze


def print_console(grid) -> None:
    print("\n----Test View----")
    for row in grid:
        line = "".join(cell.to_hex() for cell in row)
        print(line)
    print("-------------------")


def main() -> None:
    if len(sys.argv) != 2:
        print("Use: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        # 1. Cargar configuración
        config = MazeConfig(config_file)

        # 2. Generar el laberinto (Lógica)
        generator = MazeGenerator(config)
        generator.generate_maze()

        # 3. Traducir y Visualizar (Estética)
        # Obtenemos la matriz de bloques (1s y 0s)
        matrix = generator.get_display_matrix()
        
        # Creamos el visualizador y dibujamos
        visualizer = MazeVisualizer(matrix)
        visualizer.draw()

        print(f"\nLaberinto de {config.width}x{config.height} generado.")
        print(f"Perfecto: {config.perfect} | Entrada: {config.entry} | Salida: {config.exit}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
