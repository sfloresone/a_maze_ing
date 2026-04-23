# A-Maze-Ing

*Proyecto desarrollado como parte del currículo de 42 por **seflores** y **pmarcos-**.*

## Descripción

**A-Maze-Ing** es una librería Python que genera y resuelve laberintos perfectos e imperfectos utilizando algoritmos eficientes de backtracking y búsqueda. Un laberinto perfecto es aquel que contiene un único camino entre la entrada y la salida.

El proyecto demuestra la implementación modular de:
- 🎲 Generación de laberintos (con inyección de un patrón "42")
- 🔍 Resolución mediante BFS (Breadth-First Search)
- 🎨 Visualización en consola con colores ANSI y caracteres Unicode
- ⚙️ Exportación a ficheros y parseo de configuración

## Características

- **Generador modular**: Crea laberintos de cualquier tamaño con entrada/salida configurables
- **Logo 42 integrado**: Inyecta un patrón visual "42" preservado durante la generación
- **Laberintos perfectos e imperfectos**: Control total sobre la topología
- **BFS**: Encuentra la ruta óptima desde entrada a salida
- **Visualización interactiva**: Muestra/oculta la solución, cambia colores, regenera el laberinto
- **Exportación**: Guarda laberintos en ficheros de texto con coordenadas de solución

## Instalación

### Requisitos previos
- Python 3.10+
- pip

### Paso a paso

```bash
# 1. Clonar o descargar el proyecto
cd a-maze-ing

# 2. Instalar dependencias (incluye flake8 y mypy)
make install

# O manualmente:
python3 -m pip install -r requirements.txt
python3 -m pip install -e . --no-build-isolation
```

## Uso

### Modo interactivo

```bash
make run
```

O ejecutar directamente:

```bash
PYTHONPATH=src python3 a_maze_ing.py config.txt
```

**Menú interactivo:**
- `1` - Regenerar un nuevo laberinto
- `2` - Mostrar/ocultar la solución
- `3` - Cambiar color de paredes
- `4` - Salir (exporta automáticamente)

### Como librería

```python
from mazegen import MazeGenerator, MazeSolver, MazeVisualizer

# 1. Generar laberinto
generator = MazeGenerator(
    width=20, 
    height=15, 
    entry=(0, 0), 
    exit_pos=(19, 14),
    perfect=True,
    seed=42
)
generator.generate_maze()

# 2. Resolver
solver = MazeSolver(generator.get_grid(), (0, 0), (19, 14))
path = solver.solve()
coords = solver.get_path_coords(path)

# 3. Visualizar
matrix = generator.get_display_matrix()
viz = MazeVisualizer(matrix)
viz.show_path = True
viz.draw(coords)
```

Ver también [`test_package.py`](test_package.py) para un ejemplo completo.

## Configuración

Archivo `config.txt`:

```plaintext
WIDTH=50
HEIGHT=50
ENTRY=1,3
EXIT=24,14
OUTPUT_FILE=output_maze.txt
PERFECT=True
```

**Parámetros:**
- `WIDTH`, `HEIGHT`: Dimensiones del laberinto
- `ENTRY`: Entrada como `x,y`
- `EXIT`: Salida como `x,y`
- `PERFECT`: `True` para laberintos perfectos, `False` para imperfectos
- `OUTPUT_FILE`: Ruta del fichero de exportación

## Algoritmos utilizados

### Generación: Recursive Backtracking
- **Complejidad**: O(width × height)
- **Ventaja**: Genera laberintos perfectos (árbol de expansión)
- **Procedimiento**:
  1. Comenzar desde la entrada
  2. Visitar celdas vecinas no visitadas al azar
  3. Marcar como visitadas y remover paredes
  4. Backtrackear cuando no hay vecinos disponibles

### Resolución: BFS (Breadth-First Search)
- **Complejidad**: O(width × height)
- **Ventaja**: Garantiza encontrar el camino más corto
- **Procedimiento**:
  1. Inicializar cola con la entrada
  2. Explorar todos los vecinos de cada celda
  3. Marcar visitados para evitar ciclos
  4. Reconstruir camino desde salida hacia entrada

### Imperfección controlada
- Añade bucles a un laberinto perfecto con probabilidad configurable
- Preserva el logo "42" intacto

## Estructura del proyecto

```
a-maze-ing/
├── a_maze_ing.py              # Punto de entrada (modo interactivo)
├── config.txt                 # Configuración de ejemplo
├── test_package.py            # Ejemplo de uso como librería
├── output_maze.txt            # Salida de ejemplo
├── Makefile                   # Automatización
├── requirements.txt           # Dependencias
├── pyproject.toml             # Metadatos del paquete
└── src/mazegen/
    ├── __init__.py            # Exporta clases públicas
    ├── parser/
    │   └── config_parser.py   # Parseo de config.txt
    ├── maze/
    │   ├── cell.py            # Clase Cell (celda del laberinto)
    │   ├── maze_engine.py     # MazeGenerator
    │   ├── maze_visualizer.py # MazeVisualizer
    │   └── gen_output_file.py # Exportación a fichero
    └── algo/
        └── bfs.py             # MazeSolver (BFS)
```

## API Principal

### `MazeGenerator`
```python
MazeGenerator(width, height, entry, exit_pos, perfect=False, seed=None)
- generate_maze()          → Genera el laberinto
- get_grid()               → Devuelve lista de Cell
- get_display_matrix()     → Devuelve matriz de visualización (1s, 0s, 'E', 'S', 'P')
```

### `MazeSolver`
```python
MazeSolver(grid, entry, exit)
- solve()                  → Devuelve string de movimientos (N/S/E/W)
- get_path_coords(path)    → Devuelve set de (x, y) del camino
```

### `MazeVisualizer`
```python
MazeVisualizer(maze_data)
- draw(path_coords)        → Dibuja en consola
- show_path                → Propiedad booleana
- change_color(name)       → Cambia color de paredes
- update_data(new_maze)    → Actualiza matriz
```

## Partes reutilizables

- **`MazeGenerator`**: Independiente, sin dependencias internas (solo Cell)
  - Reutilizar: `gen = MazeGenerator(...); gen.generate_maze()`
  
- **`MazeSolver`**: Requiere un `grid` de `Cell`, retorna rutas
  - Reutilizar: `solver = MazeSolver(grid, entry, exit); path = solver.solve()`
  
- **`MazeVisualizer`**: Recibe matriz numérica/simbólica
  - Reutilizar: `viz = MazeVisualizer(matrix); viz.draw(path_coords)`
  
- **`MazeConfig`**: Parsea ficheros `.txt` con formato clave=valor
  - Reutilizar: `config = MazeConfig("config.txt")`

Todas las clases están en el namespace `mazegen` importable tras instalar.

## Gestión del proyecto

### Equipo
- **seflores**: Desarrollo inicial y arquitectura
- **pmarcos-**: Optimización, visualización y documentación

### Control de calidad

```bash
# Linting y type checking
make lint       # Ejecuta flake8 + mypy

# Limpiar generados
make clean      # Elimina __pycache__, dist/, .mypy_cache

# Construcción
make build      # Genera distribución con setuptools
```

**Estándares aplicados:**
- PEP 8 (flake8)
- Type hints con mypy
- Modularidad según estándares de 42

## Notas técnicas

- **Visualización**: Usa códigos ANSI (colores) y caracteres Unicode Heavy (paredes gruesas)
  - Puede no renderizar correctamente en terminales limitadas o Windows CMD nativo
  - Recomendado: WSL, Linux, macOS, o Windows Terminal

- **Logo "42"**: Se inyecta como bloque sólido preservado; requiere min. 11×9 celdas

- **Formato de salida**: Coordenadas + movimientos (N/S/E/W) en texto plano

## Ejemplos rápidos

### Generar laberinto 10×10 perfecto
```bash
echo "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\nPERFECT=True" > mini.txt
PYTHONPATH=src python3 a_maze_ing.py mini.txt
```

### Generar con seed reproducible
```python
gen = MazeGenerator(20, 20, (0, 0), (19, 19), seed=12345)
gen.generate_maze()
# Mismo seed → mismo laberinto siempre
```

## Recursos

- **Algoritmos**:
  - [Recursive Backtracking](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker)
  - [BFS Pathfinding](https://en.wikipedia.org/wiki/Breadth-first_search)

- **Documentación interna**: Docstrings en cada módulo

- **Validación**: Script `output_validator.py` disponible para validar exportaciones

## Uso de IA

Este proyecto ha sido desarrollado con ayuda de herramientas de IA para:
- Optimización de algoritmos
- Refactorización y mejora de legibilidad

---

**Última actualización**: Abril 2026