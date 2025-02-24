from dataclasses import dataclass, field

from entities.categories import Category
from utils import DikidiAPI
from logger_init import logger


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
