from logger_init import logger
from utils import DikidiApiClient 
from services.interfaces import IParsingService
from entities.services import Service

class ParsingServicesService(IParsingService):
    """Requests the available services for the specified category in the given company. """

    def get_all_objects(self, company_id: int, category_id: int | None, amount: int = -1) -> list[Service]:
        """
        Получает список услуг, относящихся к данной категории.

        Args:
            company_id (int): Идентификатор компании.
            amount (int): Максимальное количество услуг, которое нужно загрузить (-1 для загрузки всех).

        Returns:
            list[Service]: Список услуг, относящихся к категории.
        """
        result_services = []

        URL = "{base_url}/company_services/?array=1&company={company_id}"
        result_url = URL.format(base_url=self.client.URL, company_id=company_id)
        logger.debug(f"URL for parsing services ({company_id=} and {category_id=}): {result_url}")

        json_data = self.client.get_data_from_api(result_url)

        if not json_data:
            logger.warning(f"No data of available services for '{company_id=}' and {category_id=}")
            return None

        category_data = json_data.get("list", [])
        
        for category in category_data:
            if (category_id is None) or (category.get("id") == str(category_id)):
                for index, service in enumerate(category.get("services", [])):
                    if amount != -1 and index >= amount:
                        break
                    serv = Service(
                        id=service.get("id", -1),
                        company_service_id=service.get("company_service_id", -1),
                        image=service.get("image", ""),
                        cost=service.get("cost", -1),
                        name=service.get("name", ""),
                        duration=service.get("time", 0),
                        service_value=service.get("service_value", ""),
                        service_points=service.get("service_points", 0.0),
                    )
                    result_services.append(serv)

        return result_services

if __name__ == "__main__":
    dkd = DikidiApiClient()
    parser = ParsingServicesService(client=dkd)
    services = parser.get_all_objects(
        company_id=1129503,
        category_id=None, # or 3120630
        amount=-1
    )
    print(f"{len(services)} services.")
    print(services)