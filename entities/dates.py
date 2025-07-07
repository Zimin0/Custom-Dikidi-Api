from datetime import datetime
from dataclasses import dataclass, field

from datetime_slot import DateTimeSlot

@dataclass
class Date:
    """
    Class representing a free-reservation day (date + [time1, time2, time3...]).
    
    Object will be parsed from ""times":{"1223441":["2025-07-03 12:00:00","2025-07-03 14:00:00"]}" API response.
    
     Attributes:
        * date_string (str): Calendar date in ISO format ``YYYY-MM-DD`` (for example, ``"2025-07-03"``).
        * slots (list[DateTimeSlot]): Free time slots that can be booked on date_string.
    """

    date_string: str 
    slots: list[DateTimeSlot] = field(default_factory=list)

    def __post_init__(self):
        date_str_format = "%Y-%m-%d"   
        try:
            datetime.strptime(self.date_string, date_str_format)
        except ValueError:
            raise ValueError(f"'date_string' must sytisfy 'YYYY-MM-DD' format.")

    def __str__(self):
        return f"Date '{self.date_string}' and {len(self.slots)} slots"
