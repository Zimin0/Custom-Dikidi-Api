from dataclasses import dataclass
from typing import Optional

@dataclass
class DikidiUser:
    phone: str
    password: str
    first_name: str
    last_name: Optional[str] = None 

