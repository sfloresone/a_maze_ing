from src.mazegen import MazeGenerator, MazeSolver, MazeVisualizer

laberinto = MazeGenerator(
    width=15, height=10, entry=(0, 0), exit_pos=(14, 9), perfect=True
)
laberinto.generate_maze()

solucion = MazeSolver(laberinto.get_grid(), (0, 0), (14, 9))
path = solucion.solve()
coordenadas = solucion.get_path_coords(path)

matriz = laberinto.get_display_matrix()
visualizar = MazeVisualizer(matriz)
visualizar.show_path = True

visualizar.draw(coordenadas)
