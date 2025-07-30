from logger_init import logger
from utils import DikidiApiClient 
from services.interfaces import IParsingService
from entities.dates import Date 

class ParsingDatesService(IParsingService):  
    """ 
    Fetches every calendar **date** on which the specified *master* 
    can still be booked for the selected *service*. 
    """

    def get_all_objects(self, company_id: int, service_id: int, master_id: int, amount: int = -1) -> list[Date]:
        """
        Return all available booking dates for master's `master_id`.

        Args:
            company_id (int): Unique identifier of the company inside Dikidi.
            service_id (int): ID of the service the customer wants to book.
            master_id (int): ID of the staff member ("master").
            amount (int, optional): Maximum number of dates to return.
                Use ``-1`` (default) to return all available dates.

        Returns:
            list[Date]: A list of :class:`~entities.dates.Date` objects.
        """ 
        result_dates = []

        URL = "{base_url}/get_datetimes/?company_id={company_id}&service_id[]={service_id}&master_id={master_id}&with_first=1"
        result_url = URL.format(base_url=self.client.URL, company_id=company_id, service_id=service_id, master_id=master_id)
        logger.debug(f"URL для получения дат записи мастера (master_id={master_id}): {result_url}")

        json_data = self.client.get_data_from_api(result_url)
        if not json_data:
            logger.warning(f"Нет данных о доступных датах для мастера {master_id}")
            return []

        all_dates = json_data.get("dates_true", [])

        if amount != -1:
            all_dates = all_dates[:amount]

        for date in all_dates:
            result_dates.append(
                Date(date_string=date, slots=[])
            )

        return result_dates

if __name__ == "__main__":
    dkd = DikidiApiClient()
    parser = ParsingDatesService(client=dkd)
    dates = parser.get_all_objects(
        company_id=1129503,
        service_id=13765992,
        master_id=2483899,
        amount=-1
    )
    print(f"{len(dates)} свободных дат.")
    print(dates)