from dataclasses import dataclass
import requests

from logger_init import logger
from errors import APIError

# @dataclass
# class RecordData:
#     """ Class to store data for creating new record in DIKIDI. """
#     company_id: int
#     master_id: int
#     service_id: int
#     time_slot: str
#     phone: str
#     first_name: str
#     last_name: str

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
    
    # def get_all_objects(url: str):
    #     URL = "{base_url}/get_datetimes/?company_id={company_id}&service_id[]={service_id}&master_id={master_id}&with_first=1"
    #     result_url = URL.format(base_url=DikidiApi.URL, company_id=company_id, service_id=service_id, master_id=self.id)
    #     logger.debug(f"URL для получения дат записи мастера (master_id={self.id}): {result_url}")

    #     json_data = DikidiApi.get_data_from_api(result_url)
    #     if not json_data:
    #         logger.warning(f"Нет данных о доступных датах для мастера {self.id}")
    #         return []

    
    # @staticmethod
    # def create_record(data: RecordData) -> bool:

