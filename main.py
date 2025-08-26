from services.company.service import CompanyService
from services.service.parsing_services_service import ParsingServicesService
from services.booking.service import BookingService
from entities.datetime_slot import DateTimeSlot
from entities.users import DikidiUser
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
    
def user_scenario_4():
    """
    ## UserScenario №4 
    1) Choose required company by its link.
    2) Choose Service, Master, TimeSlot.
    3) Book it and get information about committed booking.
    """
    dkd_client = DikidiApiClient()
    booking_service = BookingService(client=dkd_client)
    booking_service.book(
        company_id=517955, 
        service_id=8384102, 
        master_id=1983880,
        time_slot=DateTimeSlot("2025-09-14 18:00:00"),
        user=DikidiUser(
            first_name="Елена",
            last_name="",
            phone="79172544894"
            )
        )


if __name__ == "__main__":
    # user_scenario_1()
    # user_scenario_2()
    # user_scenario_3()
    user_scenario_4()
    