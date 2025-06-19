import httpx
import json

from logger_init import logger
from errors import APIError


class DikidiApi:
    """ Additional tools for DIKIDI API. """
    
    URL = "https://dikidi.net/ru/mobile/ajax/newrecord" 

    def __init__(self):
        timeout = httpx.Timeout(5)
        self.__client = httpx.AsyncClient(timeout=timeout)

    async def get_page(self, url: str):
        response = await self.__client.get(url)
        try:
            json_data = response.json()
        except json.decoder.JSONDecodeError:
            raise APIError(f"Expected JSON, got: {response.text}")

        if response.status_code == 200:
            return json_data.get("data", {})
        else:
            error_args = json_data.get("error", {})
            raise APIError(f"({error_args.get("code")}): {error_args.get("message")}")
    
    async def close(self):
        await self.__client.aclose()
        