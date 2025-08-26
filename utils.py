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
            "Referer": f"https://dikidi.ru/record/{data.company_id}", # TODO: really is needed
            "Origin": "https://dikidi.ru",
        }

        # Step 1. Booking required timeslot.
        reservation_url = (
            "https://dikidi.ru/ru/ajax/newrecord/time_reservation/"
            f"?company_id={data.company_id}"
            f"&master_id={data.master_id}"
            f"&services_id%5B%5D={data.service_id}" # TODO: fix url 
            f"&time={data.time_slot.slot_str.replace(' ', '+').replace(":", "%3A")}"
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
            "agreement": "1"
        }
        r3 = requests.post(record_url, data=record_data, headers=headers)
        print("📌 record:", r3.status_code, r3.json())

