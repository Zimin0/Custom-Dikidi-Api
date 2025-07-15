from dataclasses import dataclass, field

from entities.services import Service
from utils import DikidiApi
from logger_init import logger

@dataclass
class Category:
    """
    Represents a category that groups multiple services.

    Attributes:
        id (int): Unique identifier of the category (from 'id' in API).
        name (str): Display name of the category (from 'name' in API).
        category_value (str): Alternative or duplicate name of the category (from 'category_value' in API).
        services (list[Service]): List of services that belong to this category (fetched separately).
    """

    # these attributes will be parsed with parent API entity (Category).
    id: int             # 'id' in API
    name: str           # 'name' in API
    category_value: str # duplicates 'name' field, 'category_value' in API

    # these attributes must be collected separately.
    services: list[Service] = field(default_factory=list)

    def __str__(self):
        return f"Category № {self.id} | '{self.name}'"

    # def get_its_services(self, company_id: int, max_amount: int = -1):
    #     """
    #     Получает список услуг, относящихся к данной категории.

    #     Args:
    #         company_id (int): Идентификатор компании.
    #         max_amount (int): Максимальное количество услуг, которое нужно загрузить (-1 для загрузки всех).

    #     Returns:
    #         list[Service]: Список услуг, относящихся к категории.
    #     """
    #     URL = "{base_url}/company_services/?array=1&company={company_id}"
    #     result_url = URL.format(base_url=DikidiApi.URL, company_id=company_id)
    #     logger.debug(f"URL для парсинга услуг категории (company_id={company_id}): {result_url}")

    #     json_data = DikidiApi.get_data_from_api(result_url)

    #     if not json_data:
    #         logger.warning(f"Нет данных о доступных услугах для данной категории {self.id}")
    #         return None

    #     category_data = json_data.get("list", [])
        
    #     for category in category_data:
    #         if category.get("id") == self.id:  # Найти соответствующую категорию
    #             counter = 0
    #             for service in category.get("services", []):
    #                 if max_amount != -1 and counter >= max_amount:
    #                     break
    #                 counter += 1
    #                 serv = Service(
    #                     id=service.get("id", -1),
    #                     company_service_id=service.get("company_service_id", -1),
    #                     name=service.get("name", ""),
    #                     time=service.get("time", 0),
    #                     service_value=service.get("service_value", ""),
    #                     service_points=service.get("service_points", 0.0),
    #                 )
    #                 self.services.append(serv)
    #             break  # Выход из цикла, если нашли нужную категорию

    #     return self.services
