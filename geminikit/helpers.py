import secrets
import string
import re

def generate_random_string():
    length = 1230
    characters = string.ascii_letters + string.digits + '-_'
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return "!"+random_string



base_cookies = {
    'SID': None,
    '__Secure-1PSID': None,
    '__Secure-3PSID': None,
    'HSID': None,
    'SSID': None,
    'APISID': None,
    'SAPISID': None,
    '__Secure-1PAPISID': None,
    '__Secure-3PAPISID': None,
    '1P_JAR': None,
    'SEARCH_SAMESITE': None,
    'AEC': None,
    '_ga': None,
    'NID': None,
    '__Secure-1PSIDTS': None,
    '__Secure-3PSIDTS': None,
    '_ga_WC57KJ50ZZ': None,
    'SIDCC': None,
    '__Secure-1PSIDCC': None,
    '__Secure-3PSIDCC': None,
}


def get_cookies_from_file(text):
    cookies = {}
    for cookie_name in base_cookies:
      pattern = rf' {cookie_name}=([^\s;]+)'
      match = re.search(pattern, text)
      if match:
        cootext = match.group(1)
        
        cookies[cookie_name] = cootext
      else:
        if cookie_name == "__Secure-1PSID":
            raise Exception("Failed to get cookie from your file, is this valid log file?")
        pass
    
    return cookies



