import sys
import requests
import logging
from bs4 import BeautifulSoup
from dataclasses import dataclass, field



# TODO: move logger to its file
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)



@dataclass
class Dates:
    """
    Класс для хранения информации о доступных датах и времени записи для мастера.

    Attributes:
        dates_true (list[str]): Список доступных дат.
        date_near (str): Ближайшая доступная дата.
        times (list[str]): Доступные временные интервалы для записи.
        first_date_true (str): Первая доступная дата.
    """
    dates_true: list[str] = field(default_factory=list)
    date_near: str = ""
    times: list[str] = field(default_factory=list)
    first_date_true: str = ""


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


@dataclass
class Category:
    """
    Класс, представляющий категорию услуг.

    Attributes:
        id (int): Уникальный идентификатор категории.
        name (str): Название категории.
        category_value (str): Полное значение категории.
        services (list[Service]): Список услуг в данной категории.
    """
    id: int
    name: str
    category_value: str
    services: list[Service] = field(default_factory=list)

    def __post_init__(self):
        self.__annotations__["id"] = "Уникальный идентификатор категории"


class APIError(Exception): # TODO: move to errors.py file
    ...

@dataclass
class Company:
    """
    Класс, представляющий компанию, предоставляющую услуги.

    Attributes:
        id (int): Уникальный идентификатор компании.
        name (str): Название компании.
        description (str | None): Описание компании (может быть пустым).
        categories (list[Category]): Список категорий услуг, предоставляемых компанией.
    """
    id: int
    name: str = ""
    description: str | None = ""
    categories: list[Category] = field(default_factory=list)

    def collect_from_api(self) -> None: 
        """ Collects company attributes from the API, except "categories". """
        URL =  "{base_url}/get_datetimes/?company_id={company_id}"
        result_url = URL.format(base_url=Dikidi_API.URL, company_id=self.id)
        logger.debug(f"URL for parsing company({self.id}): {result_url}")
        response = requests.get(result_url)
        json_data = response.json()
        if response.ok:
            company_data = json_data.get("data", {}).get("company", {})

            self.name = company_data.get("name", "")
            self.description = company_data.get("name", "")
            # self.categories = ... # can be parsed by get_categories()

        else:
            error_args = json_data.get("error")
            raise APIError(f"({error_args.get("code")}): {error_args.get("message")}")

        return  None

    def get_categories(self):
        """ Collects categories for this company and saves in "categories" field. """
        URL = "{base_url}/company_services/?array=1&company={company_id}"
        result_url = URL.format(base_url=Dikidi_API.URL, company_id=self.id)
        logger.debug(f"URL for parsing categories(company_id={self.id}: {result_url}")

        json_data = Dikidi_API.get_data_from_api(result_url)
        categories = json_data.get("data").get("list")
        for category in categories:
            print('===========================')
            print(category.get("name"))
            print('===========================')

        return categories
            

class Dikidi_API:
    
    URL = "https://dikidi.net/ru/mobile/ajax/newrecord" 

    @staticmethod
    def get_data_from_api(url: str) -> str:
        """ 
        Parse data from DIKIDI API by provided URL. 
            Args:
                url (str): url to parse
        """
        response = requests.get(url)
        json_data = response.json()
        if response.ok:
            return json_data
        else:
            error_args = json_data.get("error")
            raise APIError(f"({error_args.get("code")}): {error_args.get("message")}")





cp1 = Company(id=550001)
cp1.collect_from_api()
print(cp1)

categories = cp1.get_categories()

print(categories)


# class APISettings():
#     ...