from dataclasses import dataclass

from entities.datetime_slot import DateTimeSlot
from entities.users import DikidiUser

@dataclass
class BookingData:
    session_hash: str
    company_id: str
    service_id: str
    master_id: str
    time_slot: str
    user: DikidiUser

