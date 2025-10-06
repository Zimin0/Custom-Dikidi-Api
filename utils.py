from dataclasses import dataclass
import requests

from logger_init import logger
from errors import APIError
from entities.bookings import BookingData

class DikidiApiClient:
    """ Additional tools for DIKIDI API. """
    
    URL = "https://dikidi.net/ru/mobile/ajax/newrecord" 

    def get_data_from_api(self, url: str) -> str:
        """ 
        Parse data from DIKIDI API by provided URL. 
            Args:
                url (str): url to parse
        """
        failed = True
        while failed:
            try:
                response = requests.get(url)
                print('----------------------------------')
                print(response.headers)
                print('----------------------------------')
            except requests.exceptions.SSLError:
                failed = True
                logger.info("SSLError occured.")
            else:
                failed = False
        json_data = response.json()
        if response.ok:
            return json_data.get("data", {})
        else:
            error_args = json_data.get("error")
            raise APIError(f"({error_args.get("code")}): {error_args.get("message")}")

    def book(self, data: BookingData):
        headers = {
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"https://dikidi.ru/record/{data.company_id}", # TODO: really is needed?
            "Origin": "https://dikidi.ru",
        }

        # Step 0. Create session.
        g = f"https://dikidi.ru/mobile/ajax/newrecord/company_services/?company={data.company_id}"
        r0 = requests.get(g, headers)
        print(r0.headers)
        
        ## COOKIES в целом  не нужны, т.к. даже без их добавления сессия 9709cf6530eb4abfd712c2f261e6c6a2d5bd7f9e не требует подтверждения.
        import re
        saved_arg = ''
        parsed_cookie_args = list(map(str.strip, re.split(r";|,", r0.headers["Set-Cookie"]))) # TODO: обработать случай, когда в заголовке несколько set-cookies
        for arg in parsed_cookie_args:
            match = re.search(r"cookie_name=[^~]+~(.+)", arg)
            if match and not data.session_hash:
                saved_arg = arg
                data.session_hash = match.group(1).replace("%3A", ":")
                break 

        if not data.session_hash:
            # cookie_str = f"cookie_name=171439abb7face671ce6c97768cfc757b6292360~{};"
            test_cookie_str = f"_ym_uid=1739291734480476872; cid=726596f1247d5592ef625c9af6f900cf293af551~498817; lang=43bb664ecc8b6f42007ce39baebf98030f44b688~ru; _ym_d=1755089382; {saved_arg}; _ym_isad=1; _ym_visorc=b; uac=60317105764238e768b374d2e22aabeefad6ad63~922f3d296b6f27fc0d03457c830a27e4%3A1756596488.1641"
            headers['Cookie'] = test_cookie_str
        
        if data.session_hash:
            test_cookie_str = f"_ym_uid=1739291734480476872; cid=726596f1247d5592ef625c9af6f900cf293af551~498817; lang=43bb664ecc8b6f42007ce39baebf98030f44b688~ru; _ym_d=1755089382; cookie_name=d312b206e507843e46b66c5d13e9c18358990b4a~692f4bb3775d076eec768eee90344cc176e7258f; _ym_isad=1; _ym_visorc=b; uac=52fd0240bd98272035cf72df7e424ba03e914390~a41b290ad94a8e932979b154c586d6f6%3A1756663445.2709"
            headers['Cookie'] = test_cookie_str
     

        print(data.session_hash)
        print(headers)

        # Step 1. Booking required timeslot.
        # breakpoint()
        reservation_url = (
            "https://dikidi.ru/ru/ajax/newrecord/time_reservation/"
            f"?company_id={data.company_id}"
            f"&master_id={data.master_id}"
            f"&services_id%5B%5D={data.service_id}" # TODO: fix url 
            f"&time={str(data.time_slot).replace(' ', '+').replace(":", "%3A")}"
            f"&action_source=dikidi"
            f"&session={data.session_hash}"
        )
        r1 = requests.get(reservation_url, headers=headers)
        print("🕒 time_reservation:", r1.status_code, r1.json())

        # Step 2. Check newRecord
        check_url = (
            f"https://dikidi.ru/ru/mobile/newrecord/check/?company={data.company_id}&session={data.session_hash}&social_key="
        )
        check_data = {
            "company": data.company_id,
            "type": "normal",
            "session": data.session_hash,
            "social_key": "",
            "share_id": "0",
            "phone": data.user.phone,
            "first_name": data.user.first_name,
            "last_name": data.user.last_name,
            "comments": "",
            "promocode_appointment_id": ""
        }
        r2 = requests.post(check_url, data=check_data, headers=headers)
        print("✅ check:", r2.status_code, r2.json())

        # Step 3. Creating and commiting record.
        record_url = (
            f"https://dikidi.ru/ru/ajax/newrecord/record/?company_id={data.company_id}&session={data.session_hash}&social_key="
        )
        record_data = {
            "type": "normal",
            "name": f"{data.user.first_name} {data.user.last_name}",
            "first_name": data.user.first_name,
            "last_name": data.user.last_name,
            "phone": data.user.phone,
            "is_show_all_times": "3",
            "captcha_token": "",
            "action_source": "direct_link",
            "session": data.session_hash,
            "social_key": "",
            "active_cart_id": "0",
            "active_method": "0",
            "agreement": "1",
            "code": "1234"
        }

        r3 = requests.post(record_url, data=record_data, headers=headers)
        print("📌 record:", r3.status_code, r3.json())
