from utils import DikidiApiClient 
from entities.dates import Date 
from entities.datetime_slot import DateTimeSlot
from logger_init import logger
from services.interfaces import IParsingService

class ParsingDatetimeService(IParsingService):
    """ Requests the available time intervals for the specified date for the certain "master" and "service". """
    
    def get_all_objects(self, date: Date, company_id: int, service_id: int,  master_id: int):
        """
        Args:
            date (Date): date object
            company_id (int): Company ID.
            service_id (int): Service ID.
            master_id (int): Master ID.

        Returns:
            list[str]: List of available "DateTimeSlots". 
        """
        result_datetimes: list[DateTimeSlot] = [] 
        
        URL = ("{base_url}/get_datetimes/"
               f"?company_id={company_id}&date={date.date_string}&service_id%5B%5D={service_id}"
               f"&master_id={master_id}&with_first=false&day_month=")

        result_url = URL.format(base_url=self.client.URL, company_id=company_id, date=date, service_id=service_id, master_id=master_id)

        logger.debug(f"Request for available time slots: {result_url}")
        json_data = self.client.get_data_from_api(result_url)

        if not json_data:
            logger.warning(f"There is no data about available places to write to this Master ({master_id}).")
            return []
            
        if "times" in json_data:
            for dtime in json_data["times"].get(str(master_id), []):
                result_datetimes.append(DateTimeSlot(dtime))
        else:
            logger.warning(f"No available seats (DateTimeSlot) on the date '{date.date_string}'")

        return result_datetimes


if __name__ == "__main__":
    dkd = DikidiApiClient()
    pdtslot = ParsingDatetimeService(client=dkd)
    slots = pdtslot.get_all_objects(
        date=Date("2025-08-10"),
        company_id=1129503,
        master_id=2483897,
        service_id=13765992
    )

    print(slots)