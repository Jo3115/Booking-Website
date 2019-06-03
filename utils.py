import hashlib
import uuid
from datetime import datetime, timedelta
import database


def hash_password(password, salt):
    password += salt
    hash_object = hashlib.md5(password.encode())
    return hash_object.hexdigest()


def gennerate_salt():
    salt_object = uuid.uuid4().hex
    return salt_object


def to_date_time(string):
    return datetime.strptime(string, '%Y-%m-%dT%H:%M')


def check_badge(user):
    try:
        database.get_badge(user)[0][1]
    except IndexError:
        return False
    return True
