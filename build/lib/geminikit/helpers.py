import secrets
import string

def generate_random_string():
    length = 1230
    characters = string.ascii_letters + string.digits + '-_'
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return "!"+random_string
