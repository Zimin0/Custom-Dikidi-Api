from logger_init import logger
from utils import DikidiApiClient 
from services.interfaces import IParsingService
from entities.categories import Category

class ParsingCategoryService(IParsingService):

    def get_all_objects(self, company_id: int, amount: int = -1) -> list[Category]:
        """
        Retrieves a list of categories for the specified company.

        Args:
            company_id (int): The ID of the company for which categories will be retrieved.
            amount (int, optional): Maximum number of categories to load (-1 to load all). Defaults to -1.

        Returns:
            list[Category] | None: A list of Category objects, or None if no data is available.
        """
        result_categories = []

        URL = "{base_url}/company_services/?array=1&company={company_id}"
        result_url = URL.format(base_url=self.client.URL, company_id=company_id)
        logger.debug(f"URL for category parsing (company_id={company_id}): {result_url}")

        json_data = self.client.get_data_from_api(result_url)
        
        if not json_data:
            logger.warning(f"No available category data for company {company_id}")
            return None
        
        categories_data = json_data.get("list", [])

        for index, category in enumerate(categories_data):
            if amount != -1 and index >= amount:
                break
            category = Category(
                id=category.get("id", -1),
                name=category.get("name", ""),
                category_value=category.get("category_value", ""),
            )

            result_categories.append(category)

        return result_categories

if __name__ == "__main__":
    dkd = DikidiApiClient()
    parser = ParsingCategoryService(client=dkd)
    categories = parser.get_all_objects(
        company_id=1129503,
        amount=-1
    )
    print(f"{len(categories)} services.")
    print(categories)