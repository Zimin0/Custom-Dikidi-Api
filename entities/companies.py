from dataclasses import dataclass, field

from entities.categories import Category
from logger_init import logger

@dataclass
class InnerSchedule:
    """ Schedule structure for inner usage inside 'Company' class."""
    day:        str | None
    work_from:  str | None
    work_to:    str | None

    @staticmethod
    def parse(value: list[dict]) -> "InnerSchedule":
        """Create InnerSchedule's object from API response, f.e. - [{'day': 'Пн—Вс', 'work_from': '10:00', 'work_to': '22:00'}]. """

        if len(value) != 0:
            value = value.pop(0)
        else:
            value = {}
            logger.debug(f"List for InnerSchedule creation should not be empty, got: '{value}'.")

        day = value.get("day")
        work_from = value.get("work_from")
        work_to = value.get("work_to")
        
        object = InnerSchedule(
            day,
            work_from,
            work_to
        )

        return object
    
@dataclass
class ShortCompany:
    """
    Shortened version of Company class.
    Can be used for faster uploading.
    """
    id: int
    name: str

@dataclass
class Company:
    """
    Represents a company that provides various categorized services.

    Attributes:
        id (int): Unique identifier of the company (from 'id' in API).
        name (str): Display name of the company (from 'name' in API).
        description (str): Description of the company and its services (from 'description' in API).
        address (str): Physical address of the company (from 'address' in API).
        phones (list[str]): List of contact phone numbers (from 'phones' in API).
        currency_abbr (str): Abbreviation of the currency used by the company (from 'currency_abbr' in API).
        schedule (InnerSchedule): Weekly schedule or working hours of the company (from 'schedule' in API).
        categories (list[Category]): List of service categories offered by the company (fetched separately).
    """

    # these attributes will be parsed with parent API entity (Company).
    id: int                                         # 'id' in API
    name: str                                       # 'name' in API
    description: str                                # 'description' in API
    image: str                                      # 'image' in API
    address: str                                    # 'address' in API
    currency_abbr: str                              # 'currency_abbr' in API
    schedule: InnerSchedule                         # 'schedule' in API
    currency_abbr: str                              # 'currency_abbr' in API
    phones: list[str] = field(default_factory=list) # 'phones' in API

    # these attributes must be collected separately.
    categories: list[Category] = field(default_factory=list)

    def print_short(self):
        return f"Company № {self.id} | '{self.name}'"
    
    # def recursive_print(self):
    #     sep = "   "
    #     print(self)
    #     for category in self.categories:
    #         print(1 * sep, category)
    #         for service in category.services:
    #             print(2 * sep, service)
    #             for master in service.masters:
    #                 print(3 * sep, master)
    #                 for date in master.dates:
    #                     print(4 * sep, date)

    # def parse_all_company_recursive(self, max_amount_of_any: int = -1):
    #     """
    #     Последовательно загружает всю информацию о компании, включая категории, услуги, мастеров и их доступные даты.

    #     Args:
    #         max_amount_of_any (int): Максимальное количество элементов (категорий, услуг, мастеров, дат) для загрузки (-1 для загрузки всех).
    #     """
    #     logger.info(f"Начинаем парсинг компании (ID: {self.id})")
        
    #     self.parse_company_info()

    #     self.categories = self.get_its_categories(max_amount=max_amount_of_any)
    #     total_categories = len(self.categories)
    #     logger.info(f"Загружено категорий: {total_categories}")

    #     category_counter = 1
    #     for category in self.categories:
    #         logger.info(f"({category_counter}/{total_categories}) Обрабатываем категорию: {category.name}")
    #         category.get_its_services(self.id, max_amount=max_amount_of_any)
    #         category_counter += 1

    #         total_services = len(category.services)
    #         logger.info(f"  --> Загружено услуг: {total_services}")

    #         service_counter = 1
    #         for service in category.services:
    #             logger.info(f"  ({service_counter}/{total_services}) Обрабатываем услугу: {service.name}")
    #             service.get_its_masters(self.id, max_amount=max_amount_of_any)
    #             service_counter += 1

    #             total_masters = len(service.masters)
    #             logger.info(f"    --> Загружено мастеров: {total_masters}")

    #             master_counter = 1
    #             for master in service.masters:
    #                 logger.info(f"    ({master_counter}/{total_masters}) Обрабатываем мастера: {master.username}")
    #                 master.get_its_dates(self.id, service.id, max_amount=max_amount_of_any)
    #                 master_counter += 1

    #                 total_dates = len(master.dates)
    #                 logger.info(f"      --> Загружено дат: {total_dates}")


    # def parse_company_info(self) -> None: 
    #     """ Collects company attributes from the API, except "categories". """
    #     URL =  "{base_url}/get_datetimes/?company_id={company_id}"
    #     result_url = URL.format(base_url=DikidiApi.URL, company_id=self.id)
    #     logger.debug(f"URL for parsing company({self.id}): {result_url}")

    #     json_data = DikidiApi.get_data_from_api(result_url)

    #     if not json_data:
    #         logger.warning(f"Нет данных о доступных категориях для данной компании {self.id}")
    #         return None

    #     company_data = json_data.get("company", {})

    #     self.name = company_data.get("name", "")
    #     self.description = company_data.get("name", "")

    #     return None

    # def get_its_categories(self, max_amount: int = -1, parse_services: bool = False):
    #     """ 
    #     Получает список категорий для данной компании и сохраняет в поле `categories`.

    #     Args:
    #         max_amount (int): Максимальное количество категорий (-1 для загрузки всех).
    #         parse_services (bool): Нужно ли загружать услуги внутри категорий.
        
    #     Returns:
    #         list[Category]: Список категорий.
    #     """
    #     URL = "{base_url}/company_services/?array=1&company={company_id}"
    #     result_url = URL.format(base_url=DikidiApi.URL, company_id=self.id)
    #     logger.debug(f"URL для парсинга категорий (company_id={self.id}): {result_url}")

    #     json_data = DikidiApi.get_data_from_api(result_url)
        
    #     if not json_data:
    #         logger.warning(f"Нет данных о доступных категориях для данной компании {self.id}")
    #         return None
        
    #     categories_data = json_data.get("list", [])
    #     counter = 0

    #     for category in categories_data:
    #         if max_amount != -1 and counter >= max_amount:
    #             break
    #         counter += 1
    #         cat = Category(
    #             id=category.get("id", -1),
    #             name=category.get("name", ""),
    #             category_value=category.get("category_value", ""),
    #         )

    #         self.categories.append(cat)

    #     if parse_services:
    #         for category in self.categories:
    #             category.get_its_services(self.id)

    #     return self.categories
