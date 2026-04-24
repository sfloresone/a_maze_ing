
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

        self.seen_keys: set[str] = set()

        self._parse()
        self._validate()

    """
    Tries to assign the VALID keys
    """
    def _assign_value(self, key: str, value: str, line_num: int) -> None:

        if key in self.seen_keys:
            raise ValueError(
                f"Syntax error in line {line_num}: Duplicate key '{key}'"
                f"Each key must be defined only once"
                )

        valid_keys = {
            'WIDTH', 'HEIGHT',
            'ENTRY', 'EXIT',
            'OUTPUT_FILE', 'PERFECT', 'SEED'
        }
        if key not in valid_keys:
            raise ValueError(
                f"Syntax error in line {line_num}: Unknown key '{key}'."
                )
        self.seen_keys.add(key)
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
                if not value.endswith(".txt"):
                    raise ValueError(
                        f"OUTPUT_FILE must end with '.txt', got '{value}'"
                    )
                self.outputfile = value
            elif key == 'PERFECT':
                val_lower = value.lower()
                if val_lower == 'true':
                    self.perfect = True
                elif val_lower == 'false':
                    self.perfect = False
                else:
                    raise ValueError(
                        f"PERFECT must be 'True' or 'False', got '{value}'"
                        )
            elif key == 'SEED':
                self.seed = int(value)
        except ValueError as e:
            if "end" in str(e) or "requires" in str(e) or "must be" in str(e):
                raise ValueError(f"Syntax error in line {line_num}: {e}")
            raise ValueError(
                f"Invalid value for {key} in line {line_num}")

    def _parse(self) -> None:
        if not os.path.isfile(self.filepath):
            raise FileNotFoundError(
                f"Error: Missing config file '{self.filepath}'")

        with open(self.filepath, 'r', encoding='utf-8') as file:
            for num, line in enumerate(file, 1):
                og_line = line.strip('\n\r')
                line = og_line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.count('=') != 1:
                    raise ValueError(
                        f"Syntax error in line {num}."
                        f" Must follow strict 'KEY=VALUE' format"
                        )

                key, value = line.split('=')
                if key != key.strip() or value != value.strip() or ' ' in key:
                    raise ValueError(
                        f"Syntax error in line {num}: Spaces not allowed"
                        f" around '=' or inside the key."
                    )

                self._assign_value(key, value, num)

    def _validate(self) -> None:
        required_keys = {
            'WIDTH', 'HEIGHT',
            'ENTRY', 'EXIT',
            'OUTPUT_FILE', 'PERFECT'
        }
        missing = required_keys - self.seen_keys
        if missing:
            raise ValueError(
                "Syntax error: Missing mandatory key in config file"
                f"-> {', '.join(missing)}"
            )

        if self.width <= 0 or self.height <= 0:
            raise ValueError("Error: WIDTH and HEIGHT must be (> 0)")
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
