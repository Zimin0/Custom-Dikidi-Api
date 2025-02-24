import requests

from logger_init import logger


class DikidiAPI:
    """ Additional tools for DIKIDI API. """
    
    URL = "https://dikidi.net/ru/mobile/ajax/newrecord" 

    @staticmethod
    def get_data_from_api(url: str) -> str:
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

