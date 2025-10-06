import re
from datetime import datetime
from dataclasses import dataclass

@dataclass
class DateTimeSlot:
    """
    Class representing a reservation time slot (single date-time).

    Object must contain `2025-07-03 12:00:00` string.

    Attributes:
        * slot_str (str): time slot in string format YYYY-MM-DD HH:MM:SS.
    """
    slot_str: str

    def __post_init__(self):
        dt_format = "%Y-%m-%d %H:%M:%S"
        try:
            datetime.strptime(self.slot_str, dt_format)
        except ValueError:
            raise ValueError(f"Time slot must satisfy the '{dt_format}' format")
    
    def __str__(self) -> str:
        return self.slot_str
    
    def get_date(self) -> str:
        """Get date from self.slot_str."""
        date_pattern = r"^([%\w\-]+)"
        date_match = re.search(date_pattern, self.slot_str)
        if date_match:
            return date_match.group(1)

    def get_time(self) -> str:
        """Get time from self.slot_str."""
        time_pattern = r"([%\w:]+)$"
        time_match = re.search(time_pattern, self.slot_str)
        if time_match:
            return time_match.group(1)
