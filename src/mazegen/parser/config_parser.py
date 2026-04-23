
import os
from typing import Tuple


class MazeConfig:
    def __init__(self, filepath: str):
        self.filepath: str = filepath
        self.width: int = 0
        self.height: int = 0
        self.entry: Tuple[int, int] = (-1, -1)
        self.exit: Tuple[int, int] = (-1, -1)
        self.outputfile: str = ""
        self.perfect: bool = False
        self.seed: int | None = None

        self._parse()
        self._validate()

    """
    @Sergio verificar todo el parseo (revisar chat de @Pablo)
    """
    def _assign_value(self, key: str, value: str, line_num: int) -> None:
        value = value.strip('"\'')

        try:
            if key == 'WIDTH':
                self.width = int(value)
            elif key == 'HEIGHT':
                self.height = int(value)
            elif key == 'ENTRY':
                parts = value.split(',')
                if len(parts) != 2:
                    raise ValueError(f"ENTRY requires 2 values, got {value}")
                self.entry = (int(parts[0].strip()), int(parts[1].strip()))
            elif key == 'EXIT':
                parts = value.split(',')
                if len(parts) != 2:
                    raise ValueError(f"EXIT requires 2 values, got {value}")
                self.exit = (int(parts[0].strip()), int(parts[1].strip()))
            elif key == 'OUTPUT_FILE':
                self.outputfile = value
            elif key == 'PERFECT':
                self.perfect = value.lower() in ('true', '1', 'yes')
            elif key == 'SEED':
                self.seed = int(value)
            else:
                pass
        except ValueError:
            raise ValueError(
                f"Error: Invalid value for {key} in line {line_num}")

    def _parse(self) -> None:
        if not os.path.isfile(self.filepath):
            raise FileNotFoundError(
                f"Error: Missing config file '{self.filepath}'")

        with open(self.filepath, 'r', encoding='utf-8') as file:
            for num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if '=' not in line:
                    raise ValueError(
                        f"Syntax error in line {num}. Missing '='")

                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                self._assign_value(key, value, num)

    def _validate(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Error: WIDTH and HEIGHT must be (> 0)")
        if self.entry == (-1, -1) or self.exit == (-1, -1):
            raise ValueError("Error: ENTRY and EXIT coordinates are missing")
        if not self.outputfile:
            raise ValueError("Error: Missing OUTPUT_FILE specificator")
        if self.entry == self.exit:
            raise ValueError("Error: Both entry and exit can't be equal")
        valid_x = 0 <= self.entry[0] < self.width
        valid_y = 0 <= self.entry[1] < self.height

        valid_x_exit = 0 <= self.exit[0] < self.width
        valid_y_exit = 0 <= self.exit[1] < self.height

        if not valid_x or not valid_y:
            raise ValueError(
                f"Error: ENTRY {self.entry} is out of bounds. "
                f"Valid range: X(0 to {self.width - 1}),"
                f" Y(0 to {self.height - 1})"
            )

        if not valid_x_exit or not valid_y_exit:
            raise ValueError(
                f"Error: EXIT {self.exit} is out of bounds. "
                f"Valid range: X(0 to {self.width - 1}),"
                f" Y(0 to {self.height - 1})"
            )
