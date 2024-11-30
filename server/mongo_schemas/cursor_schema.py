from dataclasses import dataclass, asdict
from typing import Literal

@dataclass
class Cursor:
    access_token: str
    cursor: str
    cursor_type: Literal["transactions"]

    def to_dict(self):
        return asdict(self)