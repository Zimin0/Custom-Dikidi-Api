import sys
import requests
import logging
from bs4 import BeautifulSoup
from dataclasses import dataclass, field

class APIError(Exception): # TODO: move to errors.py file
    ...

# TODO: move logger to its file
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 

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
        result_url = URL.format(base_url=DikidiAPI.URL, company_id=company_id, service_id=self.id)
        logger.debug(f"URL for parsing categories(company_id={self.id}: {result_url}")

        json_data = DikidiAPI.get_data_from_api(result_url)

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

    def __str__(self):
        return f"Category № {self.id} | '{self.name}'"

    def get_its_services(self, company_id: int, max_amount: int = -1):
        """
        Получает список услуг, относящихся к данной категории.

        Args:
            company_id (int): Идентификатор компании.
            max_amount (int): Максимальное количество услуг, которое нужно загрузить (-1 для загрузки всех).

        Returns:
            list[Service]: Список услуг, относящихся к категории.
        """
        URL = "{base_url}/company_services/?array=1&company={company_id}"
        result_url = URL.format(base_url=DikidiAPI.URL, company_id=company_id)
        logger.debug(f"URL для парсинга услуг категории (company_id={company_id}): {result_url}")

        json_data = DikidiAPI.get_data_from_api(result_url)

        if not json_data:
            logger.warning(f"Нет данных о доступных услугах для данной категории {self.id}")
            return None

        category_data = json_data.get("list", [])
        
        for category in category_data:
            if category.get("id") == self.id:  # Найти соответствующую категорию
                counter = 0
                for service in category.get("services", []):
                    if max_amount != -1 and counter >= max_amount:
                        break
                    counter += 1
                    serv = Service(
                        id=service.get("id", -1),
                        company_service_id=service.get("company_service_id", -1),
                        name=service.get("name", ""),
                        time=service.get("time", 0),
                        service_value=service.get("service_value", ""),
                        service_points=service.get("service_points", 0.0),
                    )
                    self.services.append(serv)
                break  # Выход из цикла, если нашли нужную категорию

        return self.services

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

    def __str__(self):
        return f"Company № {self.id} | '{self.name}'"
    
    def recursive_print(self):
        sep = "   "
        print(self)
        for category in self.categories:
            print(1 * sep, category)
            for service in category.services:
                print(2 * sep, service)
                for master in service.masters:
                    print(3 * sep, master)
                    for date in master.dates:
                        print(4 * sep, date)

    def parse_all_company_recursive(self, max_amount_of_any: int = -1):
        """
        Последовательно загружает всю информацию о компании, включая категории, услуги, мастеров и их доступные даты.

        Args:
            max_amount_of_any (int): Максимальное количество элементов (категорий, услуг, мастеров, дат) для загрузки (-1 для загрузки всех).
        """
        logger.info(f"Начинаем парсинг компании (ID: {self.id})")
        
        self.parse_company_info()

        self.categories = self.get_its_categories(max_amount=max_amount_of_any)
        total_categories = len(self.categories)
        logger.info(f"Загружено категорий: {total_categories}")

        category_counter = 1
        for category in self.categories:
            logger.info(f"({category_counter}/{total_categories}) Обрабатываем категорию: {category.name}")
            category.get_its_services(self.id, max_amount=max_amount_of_any)
            category_counter += 1

            total_services = len(category.services)
            logger.info(f"  → Загружено услуг: {total_services}")

            service_counter = 1
            for service in category.services:
                logger.info(f"  ({service_counter}/{total_services}) Обрабатываем услугу: {service.name}")
                service.get_its_masters(self.id, max_amount=max_amount_of_any)
                service_counter += 1

                total_masters = len(service.masters)
                logger.info(f"    → Загружено мастеров: {total_masters}")

                master_counter = 1
                for master in service.masters:
                    logger.info(f"    ({master_counter}/{total_masters}) Обрабатываем мастера: {master.username}")
                    master.get_its_dates(self.id, service.id, max_amount=max_amount_of_any)
                    master_counter += 1

                    total_dates = len(master.dates)
                    logger.info(f"      → Загружено дат: {total_dates}")


    def parse_company_info(self) -> None: 
        """ Collects company attributes from the API, except "categories". """
        URL =  "{base_url}/get_datetimes/?company_id={company_id}"
        result_url = URL.format(base_url=DikidiAPI.URL, company_id=self.id)
        logger.debug(f"URL for parsing company({self.id}): {result_url}")

        json_data = DikidiAPI.get_data_from_api(result_url)

        if not json_data:
            logger.warning(f"Нет данных о доступных категориях для данной компании {self.id}")
            return None

        company_data = json_data.get("company", {})

        self.name = company_data.get("name", "")
        self.description = company_data.get("name", "")

        return  None

    def get_its_categories(self, max_amount: int = -1, parse_services: bool = False):
        """ 
        Получает список категорий для данной компании и сохраняет в поле `categories`.

        Args:
            max_amount (int): Максимальное количество категорий (-1 для загрузки всех).
            parse_services (bool): Нужно ли загружать услуги внутри категорий.
        
        Returns:
            list[Category]: Список категорий.
        """
        URL = "{base_url}/company_services/?array=1&company={company_id}"
        result_url = URL.format(base_url=DikidiAPI.URL, company_id=self.id)
        logger.debug(f"URL для парсинга категорий (company_id={self.id}): {result_url}")

        json_data = DikidiAPI.get_data_from_api(result_url)
        
        if not json_data:
            logger.warning(f"Нет данных о доступных категориях для данной компании {self.id}")
            return None
        
        categories_data = json_data.get("list", [])
        counter = 0

        for category in categories_data:
            if max_amount != -1 and counter >= max_amount:
                break
            counter += 1
            cat = Category(
                id=category.get("id", -1),
                name=category.get("name", ""),
                category_value=category.get("category_value", ""),
            )

            self.categories.append(cat)

        if parse_services:
            for category in self.categories:
                category.get_its_services(self.id)

        return self.categories


class DikidiAPI:
    """ Additional tools for DIKIDI API. """
    
    URL = "https://dikidi.net/ru/mobile/ajax/newrecord" 

    @staticmethod
    def get_data_from_api(url: str) -> str:
        """ 
        Parse data from DIKIDI API by provided URL. 
            Args:
                url (str): url to parse
        """
        failed = True
        while failed:
            try:
                response = requests.get(url)
            except requests.exceptions.SSLError:
                failed = True
                logger.info("SSLError occured.")
            else:
                failed = False
        json_data = response.json()
        if response.ok:
            return json_data.get("data", {})
        else:
            error_args = json_data.get("error")
            raise APIError(f"({error_args.get("code")}): {error_args.get("message")}")


cp1 = Company(id=550001)
cp1.parse_all_company_recursive(max_amount_of_any=-1)
# cp1.recursive_print()

print(1)