from dataclasses import dataclass
from typing import Optional

@dataclass
class UserDTO:
    username: str
    password: str
    id: Optional[str] = None

@dataclass
class BirthdayDTO:
    name: str
    date: str
    user_id: str
    id: Optional[str] = None