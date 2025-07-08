from dataclasses import dataclass, field

from entities.dates import Date
from utils import DikidiApi
from logger_init import logger

@dataclass
class Master:
    """
    Represents a specialist (master) who provides a specific service.

    Attributes:
        id (int): Unique identifier of the master.
        name (str): Display name of the master (mapped from 'username' in API).
        service_name (str): Name of the service provided by the master.
        duration (int): Duration of the service in minutes (mapped from 'time' in API).
        free_dates (list[str]): Available dates for booking the master (mapped from 'dates_true' in API).
        dates (list[Date]): Detailed information for each available date (should be fetched separately).
    """
    
    # these attributes will be parsed with parent API entity (Service).
    id: int
    name: str                                           # 'username' in API
    service_name: str = ""
    duration: int = 0                                   # 'time' in API
    free_dates: list[str] = field(default_factory=list) # 'dates_true' in API
    
    # these attributes must be collected separately.
    dates: list[Date] = field(default_factory=list)

    def __str__(self):
        return f"Master № {self.id} | '{self.username}'"
    
    # def get_its_dates(self, company_id: int, service_id: int, max_amount: int = -1):
    #     """
    #     Получает доступные даты и время записи для данного мастера.

    #     Args:
    #         company_id (int): Идентификатор компании.
    #         service_id (int): Идентификатор услуги.
    #         max_amount (int): Максимальное количество дат, которое нужно загрузить (-1 для загрузки всех).

    #     Returns:
    #         list[Dates]: Список объектов Dates с датами и временем доступности мастера.
    #     """
    #     URL = "{base_url}/get_datetimes/?company_id={company_id}&service_id[]={service_id}&master_id={master_id}&with_first=1"
    #     result_url = URL.format(base_url=DikidiApi.URL, company_id=company_id, service_id=service_id, master_id=self.id)
    #     logger.debug(f"URL для получения дат записи мастера (master_id={self.id}): {result_url}")

    #     json_data = DikidiApi.get_data_from_api(result_url)
    #     if not json_data:
    #         logger.warning(f"Нет данных о доступных датах для мастера {self.id}")
    #         return []

    #     all_dates = json_data.get("dates_true", [])

    #     if max_amount != -1:
    #         all_dates = all_dates[:max_amount]

    #     for date in all_dates:
    #         self.dates.append(
    #             Date(
    #                 date_string=date, 
    #                 times=[]
    #             )
    #         )

    #     return self.dates
