from logger_init import logger
from utils import DikidiApiClient 
from services.interfaces import IParsingService
from entities.masters import Master
from bs4 import BeautifulSoup

class ParsingMastersService(IParsingService):
    """Requests the available masters for the specified service in the given company. """

    def get_all_objects(self, company_id: int, service_id: int, amount: int = -1) -> list[Master]:
        """
        Args:
            company_id (int): Company ID.
            service_id (int): Service ID.
            max_amount (int, optional): Maximum number of masters to return. Defaults to -1 (no limit).

        Returns:
            list[Master]: List of available Master objects.
        """
        result_masters = []

        URL = "{base_url}/service_info/?company_id={company_id}&service_id={service_id}&lang=ru"
        result_url = URL.format(base_url=self.client.URL, company_id=company_id, service_id=service_id)
        logger.debug(f"URL for parsing categories(company_id={company_id}: {result_url}")

        json_data = self.client.get_data_from_api(result_url)

        if not json_data:
            logger.warning(f"No master data returned for service_id={service_id} in company_id={company_id}")
            return []
            
        raw_html = json_data.get("view", "")
        pairs = self.__parse_by_soup(raw_html, amount)

        for master_id, master_name in pairs:
            master = Master(id=master_id, name=master_name)
            result_masters.append(master)

        logger.debug(f"Parsed {len(result_masters)} masters for service_id={service_id}")
        return result_masters

    def __parse_by_soup(self, raw_html: str, amount: int) -> list[tuple[int, str]]:
        """Parse raw HTML by BeautifulSoup()."""

        result_pairs = []
        html = raw_html.replace(r"\t", "").replace(r"\n", "")
        soup = BeautifulSoup(html, "html.parser")

        for index, master_tag in enumerate(soup.select("a.master")):
            if amount != -1 and index >= amount:
                break
            master_id = master_tag.get("data-id", -1)
            master_name = master_tag.select_one("div.name").text
            result_pairs.append(
                (master_id, master_name)
                )
        return result_pairs

if __name__ == "__main__":
    dkd = DikidiApiClient()
    parser = ParsingMastersService(client=dkd)
    dates = parser.get_all_objects(
        company_id=1129503,
        service_id=13765992,
        amount=-1
    )
    print(f"{len(dates)} masters.")
    print(dates)