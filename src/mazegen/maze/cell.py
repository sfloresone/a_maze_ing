

class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

        self.walls: dict[str, bool] = {
            "N": True,  # North
            "S": True,  # South
            "E": True,  # East
            "W": True  # West
        }
        #  'Remember state' variable for BFS and Backtracking
        self.visited: bool = False
        self.is_in_pattern: bool

    def to_hex(self) -> str:
        value: int = 0

        if self.walls['N']:
            value += 1
        if self.walls['E']:
            value += 2
        if self.walls['S']:
            value += 4
        if self.walls['W']:
            value += 8

        return hex(value)[2:].upper()

    def remove_wall(self, other: 'Cell', direction: str) -> None:
        """
        Throws the shared wall in this cell and the neighbour cell
        """
        if direction == 'N':
            self.walls['N'] = False
            other.walls['S'] = False
        elif direction == 'S':
            self.walls['S'] = False
            other.walls['N'] = False
        elif direction == 'E':
            self.walls['E'] = False
            other.walls['W'] = False
        elif direction == 'W':
            self.walls['W'] = False
            other.walls['E'] = False
