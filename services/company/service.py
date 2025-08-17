import requests
from bs4 import BeautifulSoup

from entities.companies import Company, InnerSchedule, ShortCompany
from logger_init import logger
from utils import DikidiApiClient

class CompanyService:
    """
    Service for working with Dikidi companies.
    
    * Typical usage example:

        service = CompanyService(client)
        company = service.get_by_id(123)
        companies = service.search_by_name("barbershop")
        companies_detailed = service.search_by_name_detailed("barbershop")
    """

    def __init__(self, client: DikidiApiClient):
        self.__client = client

    def get_by_id(self, company_id: int) -> Company | None:
        """
        Get a single company by its unique ID.
        Args:
            company_id (int): Unique identifier of the company.

        Returns:
            Company | None: 
                A `Company` object with all available fields populated,
                or ``None`` if the company was not found.
        """
        result_company = None
        url = "https://dikidi.ru/ru/mobile/ajax/newrecord/get_datetimes/?company_id={company_id}"

        formatted_url = url.format(company_id=company_id)
        response = self.__client.get_data_from_api(formatted_url)
        company_data = response['company']

        result_company = Company(
            id=company_data['id'],
            name=company_data['name'],
            description=company_data['description'],
            image=company_data['image'],
            schedule=InnerSchedule.parse(company_data['schedule']),
            phones=company_data['phones'],
            address=company_data['address'],
            currency_abbr=company_data['currency_abbr']
            )

        return result_company

    def search_by_name(self, name: str) -> list[ShortCompany]:
        """
        Search for companies by name.
        Args:
            name (str): Query string for company name search.

        Returns:
            list[ShortCompany]: 
                A list of `ShortCompany` objects containing the `id` and `name` 
                of each matched company. Returns an empty list if no companies 
                are found.
        """

        result_short_companies = []
        url = f"https://dikidi.ru/ru/catalog/?limit=200&query={name}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        bs = BeautifulSoup(response.text, "html.parser")
        block_with_companies = bs.find("div", id="filter-result")
        company_cards = block_with_companies.find_all("a", class_="company item")
        
        if not company_cards:
            not_found_h1 = block_with_companies.find("h1", attrs={"data-perform": "frontend.catalog.init_not_found(this)"})
            if not_found_h1:
                logger.info("Message:", not_found_h1.get_text(strip=True))
            else:
                logger.info("No companies or empty result messages were found.")

        for card in company_cards:
            company_name = card.find("div", class_="name").get_text(strip=True)
            html_attribute_value = card.find("div", class_="favorite-status")['data-href']
            cleared_elemets = [el for el in html_attribute_value.split('/') if el.strip()] # skip empty strings'.
            company_id = int(cleared_elemets[-1])

            logger.debug(f"Found company's data : '{company_name}' ({company_id})")
            short_company = ShortCompany(
                id=company_id, 
                name=company_name
            )

            result_short_companies.append(short_company)

        return result_short_companies

    def search_by_name_detailed(self, name) -> list[Company]:
        """
        Fetch full company objects for all matches to a name query.
        Extended version of method 'search_by_name()' to upload full information about each company. 
        
        Args:
            name (str): Query string to search companies by name.

        Returns:
            list[Company]: A list of fully populated `Company` objects.
            Returns an empty list if no companies match the query.
        """
        result_companies = []
        short_companies = self.search_by_name(name)
        for sh_company in short_companies:
            detailed_company = self.get_by_id(sh_company.id)
            result_companies.append(detailed_company)
        
        return result_companies


if __name__ == "__main__":
    dikidi_client = DikidiApiClient()
    company_service = CompanyService(dikidi_client)
    found_company = company_service.get_by_id(140627)
    print(f"{found_company=}")

    list_of_companies = company_service.search_by_name("груминг")
    print("List of companies:", len(list_of_companies))
