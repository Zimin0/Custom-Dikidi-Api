import requests
import datetime
from requests import Response
from bs4 import BeautifulSoup

UNI_ID = "550001"
STEP = "0"

LOGIN = "79313661220"
PASSWORD = "Sx3ux,tg4XiFXHf"

url = f"https://dikidi.net/{UNI_ID}?p={STEP}.pi"





auth_headers={
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

### AUTH ###
session = requests.Session() # Создаем сессию для хранения cookies


auth_data = {
    'number': LOGIN, # phone number
    'password': PASSWORD
}

response = session.post(
    url='https://auth.dikidi.ru/ajax/user/auth/',
    data=auth_data,
    headers=auth_headers
)

print(response.json())
session.cookies.set("token", "084a7a8de598494eda2a43df0216cf740f6e306d~73df0c7cdcdc4b583910e92806b80a1beab80860", domain=".dikidi.net")
session.cookies.set("cookie_name", "4d2c284c688472ede377309414e720b0e8777b2e~565981eef2e79071223f86fe8abf20c9189030e1", domain=".dikidi.net")

session.cookies.set("domain_sid", "NDa1JvLVA_xoPrrnujl26%3A1739343394693", domain=".dikidi.net")
session.cookies.set("cookie_name", "4d2c284c688472ede377309414e720b0e8777b2e~565981eef2e79071223f86fe8abf20c9189030e1", domain=".dikidi.net")

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

params={
    'company': "550001",
    'client': '',
    'start': "2025-02-13",
    'end': "2025-02-13",
    'date_field': '',
    'date_order': '',
    'sort_field': '',
    'sort_order': '',
    'limit': 60,
    'offset': 0,
    'first': 1
}

response = session.get(url="https://dikidi.net/owner/ajax/journal/appointment_list/", headers=headers, params=params)


print(f"{response.status_code=}")
if response.status_code == 200:
    print(response.json())
# else:
#     print(f"{response.status_code=}")
#     # print(response.text)

# date_object = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), datetime.time.min).strftime('%Y-%m-%d')
# print(date_object)

session.close()

# print("URL:", url)

# with open("downloaded_page.html", "w", encoding="utf-8") as f:
#     f.write(response.text)

# if response.status_code == 200:
#     soup = BeautifulSoup(response.text, 'html.parser') # TODO: попробовать несколько прасеров
#     header = soup.select_one("h1.title")
#     print(f"Университет: {header}")
#     all_appointments = soup.find_all("div", class_="details")
#     print(all_appointments)

