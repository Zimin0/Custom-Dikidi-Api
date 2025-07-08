from datetime import datetime
from dataclasses import dataclass, field

from entities.datetime_slot import DateTimeSlot

@dataclass
class Date:
    """
    Class representing a free-reservation day (date + [time1, time2, time3...]).
    
    Object will be parsed from ""times":{"1223441":["2025-07-03 12:00:00","2025-07-03 14:00:00"]}" API response.
    
    Attributes:
        * date_string (str): Calendar date in ISO format ``YYYY-MM-DD`` (for example, ``"2025-07-03"``).
        * slots (list[DateTimeSlot]): Free time slots that can be booked on date_string.
    """

    # these attributes will be parsed with parent API entity (Master).
    date_string: str 
    
    # these attributes must be collected separately.
    slots: list[DateTimeSlot] = field(default_factory=list)

    def __post_init__(self):
        date_str_format = "%Y-%m-%d"   
        try:
            datetime.strptime(self.date_string, date_str_format)
        except ValueError:
            raise ValueError(f"'date_string' must sytisfy 'YYYY-MM-DD' format.")

    def __str__(self):
        return f"Date '{self.date_string}' and {len(self.slots)} slots"

    # def get_its_times(self, company_id: int, service_id: int, master_id: int):
    #     """
    #     Запрашивает доступные временные интервалы на указанную дату для мастера и услуги.

    #     Args:
    #         company_id (int): Идентификатор компании.
    #         service_id (int): Идентификатор услуги.
    #         master_id (int): Идентификатор мастера.

    #     Returns:
    #         list[str]: Список доступных временных интервалов.
    #     """
    #     date = self.date_string
    #     URL = ("{base_url}/get_datetimes/"
    #            f"?company_id={company_id}&date={date}&service_id%5B%5D={service_id}"
    #            f"&master_id={master_id}&with_first=false&day_month=")

    #     result_url = URL.format(base_url=DikidiApi.URL, company_id=company_id, date=date, service_id=service_id, master_id=master_id)

    #     logger.debug(f"Запрос доступных временных слотов: {result_url}")
    #     json_data = DikidiApi.get_data_from_api(result_url)

    #     if not json_data:
    #         logger.warning(f"Нет данных о доступных местах для записи к этому мастеру ({master_id}).")
    #         return []
            
    #     if "times" in json_data:
    #         self.times = json_data["times"].get(str(master_id), [])
    #     else:
    #         logger.warning(f"Нет данных о доступных временах на дату {self.date_string}")


    #     return self.times
