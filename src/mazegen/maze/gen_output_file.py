
from src.mazegen.maze.cell import Cell


def export_maze(
        filepath: str,
        grid: list[list[Cell]],
        entry: tuple[int, int],
        exit: tuple[int, int],
        path: str = ""
) -> None:
    """
    Generates the outputfile within the maze specifications

    Args:
        filepath: File creation path
        grid: The 2D matrix
        entry: A tuple with (x,y) entry coordinates
        exit: A tuple with (x,y) exit coordinates
        path: String with the path solution
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:

            for row in grid:
                line = "".join(cell.to_hex() for cell in row)
                f.write(f"{line}\n")

            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit[0]},{exit[1]}\n")
            f.write(f"{path}\n")
    except IOError as e:
        print(f"Error: Outputfile could not be generated {e}")
