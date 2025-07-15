from dataclasses import dataclass, field
from bs4 import BeautifulSoup

from entities.masters import Master
from utils import DikidiApi
from logger_init import logger

@dataclass
class Service:
    """
    Represents a service offered by a company, including details and available specialists.

    Attributes:
        id (int): Unique identifier of the service.
        company_service_id (int): Identifier used by the company for internal referencing (from 'company_service_id' in API).
        image (str): URL or path to the image associated with the service (from 'image' in API).
        cost (int): Cost or price of the service (from 'cost' or 'price' in API).
        name (str): Display name of the service (from 'name' in API).
        duration (int): Duration of the service in minutes (mapped from 'time' in API).
        service_value (str): Alternative or duplicate name of the service (from 'service_value' in API).
        service_points (float): Points or rating associated with the service (from 'service_points' in API).
        masters (list[Master]): List of specialists (masters) who can perform this service (fetched separately).
    """
    
    # these attributes will be parsed with parent API entity (Service).
    id: int
    company_service_id: int     # 'company_service_id' in API
    image: str                  # 'image' in API
    cost: int                   # 'cost' or 'price' in API
    name: str                   # 'name' in API
    duration: int = 0           # 'time' in API
    service_value: str = ""     # duplicates 'name' field, 'service_value' in value
    service_points: float = 0.0 # 'service_points' in API

    # these attributes must be collected separately.
    masters: list[Master] = field(default_factory=list)

    def __str__(self):
        return f"Service № {self.id} | '{self.name}'"
    
    # def get_its_masters(self, company_id: int, max_amount: int = -1):
    #     URL = "{base_url}/service_info/?company_id={company_id}&service_id={service_id}&lang=ru"
    #     result_url = URL.format(base_url=DikidiApi.URL, company_id=company_id, service_id=self.id)
    #     logger.debug(f"URL for parsing categories(company_id={self.id}: {result_url}")

    #     json_data = DikidiApi.get_data_from_api(result_url)

    #     if not json_data:
    #         logger.warning(f"Нет данных о доступных мастерах для данной услуги {self.id}")
    #         return None
            
    #     dirty_html = json_data.get("view", "")
    #     html = dirty_html.replace(r"\t", "").replace(r"\n", "")
    #     soup = BeautifulSoup(html, "html.parser") # TODO: move
    #     counter = 0
    #     for master in soup.select("a.master"):
    #         if max_amount != -1 and counter >= max_amount:
    #             break
    #         counter += 1
    #         mst = Master(
    #             id=master.get("data-id", -1),
    #             username=master.select_one("div.name").text
    #         )
    #         self.masters.append(mst)

    #     return self.masters
