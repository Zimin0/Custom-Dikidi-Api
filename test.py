import requests
import sys
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def parse_response(response_json): # for URL2
    lessons = response_json["data"]["list"]
    for lesson in lessons:
        # print(f"Урок: {lesson['name']}, дата: {lesson['date']}, время: {lesson['time']}")
        print("========================")
        print(lesson['name'])
        for service in lesson['services']:
            print(service['id'], service['name'])
        # print(lesson['services'])


GORNY_ID = 550001

URL = "https://dikidi.net/owner/ajax/journal/appointment_list/?company_id=550001&master_id=1357241&services_id%5B%5D=5159581&time=2025-02-14+14%3A15%3A00&action_source=direct_link&session=73df0c7cdcdc4b583910e92806b80a1beab80860"
OLD_URL = "https://dikidi.net/ru/ajax/newrecord/time_reservation/?company_id=550001&master_id=1357241&services_id%5B%5D=5159581&time=2025-02-14+14%3A15%3A00&action_source=direct_link&session=73df0c7cdcdc4b583910e92806b80a1beab80860"
# страница с местами https://dikidi.net/550001?p=3.pi-po-ssm-si&o=7&s=5159581
URL_1 = "https://dikidi.net/ru/mobile/ajax/newrecord/service_info/?session=ca1c61ffa429230fc9991738f92a526a307faade&social_key=&company_id=550001&service_id=5159581&lang=ru"
URL2 = "https://dikidi.net/mobile/ajax/newrecord/company_services/?lang=ru&array=1&company=550001&master=&share="
## Данные о компании
URL_3 = "https://dikidi.net/ru/mobile/ajax/newrecord/project_options/?company=550001&session=ca1c61ffa429230fc9991738f92a526a307faade&social_key="
URL_5 = "https://dikidi.net/ru/mobile/newrecord/get_company/?company=550001&session=ca1c61ffa429230fc9991738f92a526a307faade&social_key="
URL_6 = "https://dikidi.net/ru/mobile/ajax/newrecord/get_datetimes/?company_id=550001&service_id%5B%5D=5159581&master_id=1357211&with_first=1&day_month="
# Все записи со страницы https://dikidi.net/550001?p=2.pi-po-sm-mi&o=1&m=1516171
URL_7 = "https://dikidi.net/ru/ajax/newrecord/to_master_get_masters/?company_id=550001"
# response = requests.get(URL_1)

# print(f"{response.status_code=}")
# if response.status_code == 200:
#     # print(response.text.replace(r"\t", "").replace(r"\n", ""))
#     soup = BeautifulSoup(response.json()["data"]["view"], "html.parser")
#     name = soup.select("div.details > div.name")
#     print(name)
#     # parse_response(response.json())

def print_categories():
    for category in get_categories(GORNY_ID):
        print("========================")
        print(category['name'])
        for service in category['services']:
            print(service['id'], service['name'])

def get_categories(company_id: int) -> list:
    """ 
    Возвращает все доступные лабы (category and its services)
    Ссылка: https://dikidi.net/550001?p=2.pi-po-ssm-si&o=7&s=5159581
    """
    URL = f"https://dikidi.net/mobile/ajax/newrecord/company_services/?lang=ru&array=1&company={company_id}"

    response = requests.get(URL)
    res_json = response.json()
    logger.info(res_json)
    
    error_status = res_json.get("error")
    logger.info(f"{error_status=}")
    if error_status.get("code") == 0:
        return res_json.get("data").get("list")
    return []

def get_service_info():
    """ 
    Возвращает все свободные места на лабу. 
    Ссылка: https://dikidi.net/550001?p=3.pi-po-ssm-si&o=7&s=5159581
    """
    URL = "https://dikidi.net/ru/mobile/ajax/newrecord/service_info/?company_id=550001&service_id=5159581&lang=ru"
    
    response = requests.get(URL) # TODO: add status http check
    res_json = response.json()
    logger.info(res_json)

    error_status = res_json.get("error")
    logger.info(f"{error_status=}")
    if error_status.get("code") == 0:
        dirty_html = res_json.get("data").get("view")
        html = dirty_html.replace(r"\t", "").replace(r"\n", "")
        soup = BeautifulSoup(html, "html.parser")
        list_all_free_places = soup.select("div.list") # места для записи
        return list_all_free_places

    return None


def get_datetimes(company_id: int, service_id: int):
    """ 
    Возвращает все свободные места на лабу в определенный день и время (datetimes).
    Ссылка: https://dikidi.net/ru/mobile/ajax/newrecord/get_datetimes/?company_id=550001&service_id%5B%5D=5159581&master_id=1357211&with_first=1&day_month=
    """
    URL = f"https://dikidi.net/ru/mobile/ajax/newrecord/get_datetimes/?company_id=550001&service_id%5B%5D=5159517&master_id=3798406&with_first=1&day_month="
    response = requests.get(URL)


# print_categories()

# print(get_service_info())



# TODO: получить все лабораторные работы для кабинета + места для них.


class Service:
    """ 
    Category +  
    Examples: 
        * Выполнение лаб. 428 (Оптика)
        * Выполнение лаб. 231 (Тв. тело) 
    Page: Выбор занятия
    Page link: https://dikidi.net/550001?p=2.pi-po-ssm&o=7"""
    ...



# Service (Выбор занятия, Выполнение лаб. 428 (Оптика) id=5159581)


# find - Только один элемент, как только встречает, то сразу прекращает дальнейший поиск
# find_all - просматривает всех потомков тега и возвращает всех потомков, которые подходят под условие
# soup.find_all("p", class_="title")
# soup.find_all(id="link2")
# soup.find_all(id=True) # все у кого есть id атрибут тега
# soup.find_all(attrs={"data-foo": "value"}) # для атрибутов, имена которых нельзя использовать в python
# Similarly, you can't use a keyword argument to search for HTML's 'name' attribute, because Beautiful Soup uses the name argument to contain the name of the tag itself. Instead, you can give a value to 'name' in the attrs argument:
# name_soup = BeautifulSoup('<input name="email"/>', 'html.parser')
# name_soup.find_all(name="email")
# []
# name_soup.find_all(attrs={"name": "email"})
# [<input name="email"/>]

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors-through-the-css-property