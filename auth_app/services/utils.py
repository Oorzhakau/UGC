import string
import uuid
from secrets import choice as secrets_choice


def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


def generate_random_string():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets_choice(alphabet) for _ in range(16))
