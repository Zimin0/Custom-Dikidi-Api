from dataclasses import dataclass
from datetime_slot import DateTimeSlot
from users import DikidiUser

@dataclass
class Booking:
    session_hash: str
    company_id: int
    service_id: int
    master_id: int
    time_slot: DateTimeSlot
    user: DikidiUser
