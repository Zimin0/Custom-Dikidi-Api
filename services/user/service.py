import re
import os
import requests
from dotenv import load_dotenv

from entities.users import DikidiUser

load_dotenv()

class UserManager:
    """Service to manage users"""
    
    @staticmethod
    def read_from_env() -> DikidiUser:
        """ Load Dikidi user from .env file. """
        
        first_name = os.environ.get("DIKIDI_USER_NAME")
        phone = os.environ.get("DIKIDI_USER_PHONE")
        password = os.environ.get("DIKIDI_USER_PASSWORD")

        if first_name is None:
            raise KeyError("DIKIDI_USER_NAME was no found in .env file.")
        if phone is None:
            raise KeyError("DIKIDI_USER_PHONE was no found in .env file.")
        if password is None:
            raise KeyError("DIKIDI_USER_PASSWORD was no found in .env file.")
        
        return DikidiUser(
            first_name=first_name,
            phone=phone,
            password=password
        )
     