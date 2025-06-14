from dataclasses import dataclass, field
from utils import DikidiApi
from logger_init import logger

@dataclass
class Date:
    """
    Класс, представляющий конкретную дату с возможностью получения доступных временных слотов.
    
    Attributes:
        date (str): Дата в формате YYYY-MM-DD.
        times (list[str]): Список доступных временных интервалов в этот день.
    """
    date_string: str
    times: list[str] = field(default_factory=list)

    def __str__(self):
        return f"Date '{self.date_string}'"

    def get_its_times(self, company_id: int, service_id: int, master_id: int):
        """
        Запрашивает доступные временные интервалы на указанную дату для мастера и услуги.

        Args:
            company_id (int): Идентификатор компании.
            service_id (int): Идентификатор услуги.
            master_id (int): Идентификатор мастера.

        Returns:
            list[str]: Список доступных временных интервалов.
        """
        date = self.date_string
        URL = ("{base_url}/get_datetimes/"
               f"?company_id={company_id}&date={date}&service_id%5B%5D={service_id}"
               f"&master_id={master_id}&with_first=false&day_month=")

        result_url = URL.format(base_url=DikidiApi.URL, company_id=company_id, date=date, service_id=service_id, master_id=master_id)

        logger.debug(f"Запрос доступных временных слотов: {result_url}")
        json_data = DikidiApi.get_data_from_api(result_url)

        if not json_data:
            logger.warning(f"Нет данных о доступных местах для записи к этому мастеру ({master_id}).")
            return []
            
        if "times" in json_data:
            self.times = json_data["times"].get(str(master_id), [])
        else:
            logger.warning(f"Нет данных о доступных временах на дату {self.date_string}")


        return self.times
