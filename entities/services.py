from dataclasses import dataclass, field
from bs4 import BeautifulSoup

from entities.masters import Master
from utils import DikidiApi
from logger_init import logger

@dataclass
class Service:
    """
    Класс, представляющий услугу.

    Attributes:
        id (int): Уникальный идентификатор услуги.
        company_service_id (int): Идентификатор услуги внутри компании.
        name (str): Название услуги.
        time (int): Длительность услуги в минутах.
        service_value (str): Полное значение услуги.
        service_points (float): Очки услуги (рейтинг или популярность).
    """
    id: int
    company_service_id: int
    name: str
    time: int = 0
    service_value: str = ""
    service_points: float = 0.0
    masters: list[Master] = field(default_factory=list)

    # commpany_id = ...- ? 

    def __str__(self):
        return f"Service № {self.id} | '{self.name}'"
    
    def get_its_masters(self, company_id: int, max_amount: int = -1):
        URL = "{base_url}/service_info/?company_id={company_id}&service_id={service_id}&lang=ru"
        result_url = URL.format(base_url=DikidiApi.URL, company_id=company_id, service_id=self.id)
        logger.debug(f"URL for parsing categories(company_id={self.id}: {result_url}")

        json_data = DikidiApi.get_data_from_api(result_url)

        if not json_data:
            logger.warning(f"Нет данных о доступных мастерах для данной услуги {self.id}")
            return None
            
        dirty_html = json_data.get("view", "")
        html = dirty_html.replace(r"\t", "").replace(r"\n", "")
        soup = BeautifulSoup(html, "html.parser") # TODO: move
        counter = 0
        for master in soup.select("a.master"):
            if max_amount != -1 and counter >= max_amount:
                break
            counter += 1
            mst = Master(
                id=master.get("data-id", -1),
                username=master.select_one("div.name").text
            )
            self.masters.append(mst)

        return self.masters
