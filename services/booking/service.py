from logger_init import logger
from utils import DikidiApiClient
from entities.datetime_slot import DateTimeSlot
from entities.users import DikidiUser
from entities.bookings import BookingData

class BookingService:
    def __init__(self, client: DikidiApiClient):
        self.__client = client
    
    def book(self, company_id: int, service_id: int, master_id: int, time_slot: DateTimeSlot, user: DikidiUser):
        bk_data = BookingData(
            session_hash="752cbbcf0a29fdb00aeb7dc6cd7b9e899bc63007",
            company_id=str(company_id),
            service_id=str(service_id),
            master_id=str(master_id),
            time_slot=time_slot,
            user=user
        )
        self.__client.book(bk_data)
    