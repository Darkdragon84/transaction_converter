from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Transactions:
    COLUMNS: ClassVar[list[str]]
