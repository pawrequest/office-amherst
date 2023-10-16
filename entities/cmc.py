from dataclasses import dataclass
from typing import Optional, Iterable


@dataclass
class Connection:
    name: str
    table: str
    fields: Optional[Iterable[str]] = None
