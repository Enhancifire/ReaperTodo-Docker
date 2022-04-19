import hashlib
from uuid import uuid4

def hash(password: str):
    salt = str(uuid4())

    key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
            )


    return (str(key), salt)

def dehash(key, salt: str, password: str):
    new_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
            )

    new_key = str(new_key)
    if key == new_key:
        return True
    else:
        return False
