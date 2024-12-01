from dataclasses import dataclass, asdict
from typing import Literal

@dataclass
class Cursor:
    access_token: str
    cursor: str
    cursor_type: Literal["transactions"]

    def to_dict(self):
        return {
            "access_token": self.access_token,
            "cursor": self.cursor,
            "cursor_type": self.cursor_type
        }
    
    @classmethod
    def from_dict(cls, dict:dict):
        required_fields = ["access_token", "cursor", "cursor_type"]
        if not all(field in dict for field in required_fields):
            raise ValueError(f"Missing required fields. Expected {required_fields}")
        return cls(
            access_token = dict["access_token"],
            cursor = dict["cursor"],
            cursor_type = dict["cursor_type"]
        )
