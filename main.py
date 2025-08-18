from services.company.service import CompanyService
from services.parsing_services_service import ParsingServicesService
from utils import DikidiApiClient

def user_scenario_1():
    """ 
    UserScenario №1
    1) I'm searching a company by its ID.
    2) I want to see information about the company.
    3) I want to see all the services of the company.
    """
    company_id = 511357
    dkd_client = DikidiApiClient()
    company_services = CompanyService(client=dkd_client)

    service_parser = ParsingServicesService(client=dkd_client)

    company = company_services.get_by_id(company_id)
    print(company.print_short())
    
    all_services = service_parser.get_all_objects(company.id)
    print(f"Found {len(all_services)} services:")
    for serv in all_services:
        print(serv.print_short())

def user_scenario_2():
    """
    UserScenario №2
    1) I'm searching a company by its name.
    2) I choose from the provided filtered options.
    """
    company_query = "кот"
    dkd_client = DikidiApiClient()
    company_services = CompanyService(client=dkd_client)

    list_of_companies = company_services.search_by_name(company_query)
    print(f"Filtered {list_of_companies} companies.")

def user_scenario_3():
    """ 
    ## UserScenario №3
    1) Parse Company by link to its page (f.e.: https://dikidi.net/ru/1642062?p=0.pi)
    2) I want to see information about the company.
    """
    links = [
        'https://dikidi.ru/ru/profile/zoosalon_foks_kommuny_59_511357',
        'https://dikidi.ru/ru/profile/511357',
        'https://dikidi.ru/ru/511357?p=0.pi',
        'https://dikidi.ru/ru/511357',
        'https://dikidi.net/en/511357',
    ]

    dkd_client = DikidiApiClient()
    company_services = CompanyService(client=dkd_client)

    for link in links:
        print("Processing link:", link)
        company = company_services.get_by_link(link)
        print("Parsed Company with ID =", company.id)       

if __name__ == "__main__":
    user_scenario_1()
    user_scenario_2()
    user_scenario_3()
