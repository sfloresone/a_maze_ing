
import sys
from src.mazegen.parser.config_parser import MazeConfig
from src.mazegen.maze.maze_engine import MazeGenerator
from src.mazegen.maze.maze_visualizer import MazeVisualizer
from src.mazegen.maze.gen_output_file import export_maze
from src.mazegen.algo.bfs import MazeSolver


def main() -> None:
    if len(sys.argv) != 2:
        print("Use: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        # 1. Cargar configuración
        config = MazeConfig(config_file)

        # 2. Generar el laberinto (Lógica)
        generator = MazeGenerator(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit_pos=config.exit,
            perfect=config.perfect,
            seed=config.seed
        )
        generator.generate_maze()

        # 3. Obtener las coordenadas del camino
        solver = MazeSolver(generator.get_grid(), config.entry, config.exit)
        solved_path = solver.solve()
        path_coords = solver.get_path_coords(solved_path)

        # 4. Traducir y Visualizar (Estética)
        # Obtenemos la matriz de bloques (1s y 0s)
        matrix = generator.get_display_matrix()
        visualizer = MazeVisualizer(matrix)
        visualizer.show_path = False

        while True:
            export_maze(
                config.outputfile,
                generator.get_grid(),
                config.entry,
                config.exit,
                solved_path
            )
            # Dibujar laberinto
            # Pasamos path_coords siempre,
            # el visualizador decide si pintarlas con show_path
            visualizer.draw(path_coords)
            print("\n=== A-Maze-Ing ===")
            print("1. Re-generate a new maze")
            print(f"2. {'Hide' if visualizer.show_path else 'Show'} path")
            print("3. Change colors")
            print("4. Quit")

            choice = input("\nChoice? (1-4): ")

            if choice == "1":
                # IMPORTANTE: Al regenerar,
                # hay que repetir todo el proceso lógico
                gen = MazeGenerator(
                    width=config.width,
                    height=config.height,
                    entry=config.entry,
                    exit_pos=config.exit,
                    perfect=config.perfect,
                    seed=config.seed
                )
                gen.generate_maze()

                # Actualizar solución
                solver = MazeSolver(gen.get_grid(), config.entry, config.exit)
                solved_path = solver.solve()
                path_coords = solver.get_path_coords(solved_path)

                # Actualizar dibujo
                visualizer.update_data(gen.get_display_matrix())

            elif choice == "2":
                visualizer.show_path = not visualizer.show_path

            elif choice == "3":
                new_color = input(
                    "Color (red/green/blue/yellow/white): ").lower()
                visualizer.change_color(new_color)
            elif choice == "4":
                break

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
