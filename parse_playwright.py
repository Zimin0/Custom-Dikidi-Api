from playwright.sync_api import sync_playwright
import json

from logger_init import logger
from errors import APIError


class DikidiAPI:
    """ Additional tools for DIKIDI API. """
    
    URL = "https://dikidi.net/ru/mobile/ajax/newrecord" 

    @staticmethod
    def get_data_from_api(url: str) -> dict:
        """ 
        Parse JSON data from DIKIDI API using Playwright request.
            Args:
                url (str): API endpoint to request
        """
        logger.debug(f"Starting Playwright request for URL: {url}")
        with sync_playwright() as p: # open connection 
            browser = p.chromium.launch(headless=True) # 
            context = browser.new_context()
            try:
                response = context.request.get(url, timeout=15000)
                if response.status != 200:
                    raise APIError(f"Bad response: {response.status}")
                
                json_data = response.json()
                if "error" in json_data and json_data["error"]["code"] != 0:
                    raise APIError(f'({json_data["error"]["code"]}): {json_data["error"]["message"]}')
                
                return json_data.get("data", {})
            except Exception as e:
                logger.exception(f"Failed to retrieve data from {url}")
                raise
            finally:
                browser.close()
