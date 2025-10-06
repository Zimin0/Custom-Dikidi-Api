import re
import requests

from entities.users import DikidiUser

class AuthenticationService:
    def auth(self, user: DikidiUser) -> str:
        """
        Authenticate user in the DIKIDI website. 
        Return session hash.
        """

        url_post = "https://auth.dikidi.ru/ajax/user/auth/"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0"
        }
        payload = {
            "number": user.phone,
            "password": user.password,
        }

        response = requests.post(url_post, data=payload, headers=headers)

        if response.status_code == 400:
            error_raw = response.json()['error']
            error_text = f"{error_raw['code']}: {error_raw['message']}"
            raise ValueError(error_text)

        regex = r"sw\.auth\.complete\('(\w{40})'\)"
        session_hash = None

        match = re.search(regex, response.json()['callback'])
        if match:
            session_hash = match.group(1)
            return session_hash
        else:
            raise KeyError(f"Unreadable response: {response.json()}")
