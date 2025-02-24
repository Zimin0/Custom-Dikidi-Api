from dataclasses import dataclass, field

from entities.dates import Dates
from utils import DikidiAPI
from logger_init import logger

@dataclass
class Master:
    """
    Класс, представляющий мастера, выполняющего услуги.

    Attributes:
        id (int): Уникальный идентификатор мастера.
        username (str): Имя мастера (или название лабораторной работы).
        service_name (str): Название услуги, которую выполняет мастер.
        time (int): Длительность услуги у мастера в минутах.
        dates_true (list[str]): Доступные даты для записи к мастеру.
        times (list[str]): Доступные временные интервалы для записи.
    """
    id: int
    username: str
    service_name: str = ""
    time: int = 0
    dates_true: list[str] = field(default_factory=list)
    times: list[str] = field(default_factory=list)
    dates: list[Dates] = field(default_factory=list)

    def __str__(self):
        return f"Master № {self.id} | '{self.username}'"
    
    def get_its_dates(self, company_id: int, service_id: int, max_amount: int = -1):
        """
        Получает доступные даты и время записи для данного мастера.

        Args:
            company_id (int): Идентификатор компании.
            service_id (int): Идентификатор услуги.
            max_amount (int): Максимальное количество дат, которое нужно загрузить (-1 для загрузки всех).

        Returns:
            list[Dates]: Список объектов Dates с датами и временем доступности мастера.
        """
        URL = "{base_url}/get_datetimes/?company_id={company_id}&service_id[]={service_id}&master_id={master_id}&with_first=1"
        result_url = URL.format(base_url=DikidiAPI.URL, company_id=company_id, service_id=service_id, master_id=self.id)
        logger.debug(f"URL для получения дат записи мастера (master_id={self.id}): {result_url}")

        json_data = DikidiAPI.get_data_from_api(result_url)
        if not json_data:
            logger.warning(f"Нет данных о доступных датах для мастера {self.id}")
            return []

        all_dates = json_data.get("dates_true", [])
        times_dict = json_data.get("times", {})
        if times_dict: # can recieve a blank list
            times_dict = times_dict.get(str(self.id), [])
        first_date = json_data.get("first_date_true", "")
        date_near = json_data.get("date_near", "")

        if max_amount != -1:
            all_dates = all_dates[:max_amount]
            times_dict = times_dict[:max_amount]

        dates_obj = Dates(
            dates_true=all_dates,
            date_near=date_near,
            times=times_dict,
            first_date_true=first_date
        )
        self.dates.append(dates_obj)

        return self.dates
