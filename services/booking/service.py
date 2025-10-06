from logger_init import logger
from utils import DikidiApiClient
from entities.datetime_slot import DateTimeSlot
from entities.users import DikidiUser
from entities.bookings import BookingData

class BookingService:
    def __init__(self, client: DikidiApiClient):
        self.__client = client
    
    def book(self, company_id: int, service_id: int, master_id: int, time_slot: DateTimeSlot, session_hash: str, user: DikidiUser):
        bk_data = BookingData(
            session_hash=session_hash,
            company_id=str(company_id),
            service_id=str(service_id),
            master_id=str(master_id),
            time_slot=time_slot,
            user=user
        )
        
        self.__client.book(bk_data)
    