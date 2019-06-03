import database
import utils
from datetime import datetime, timedelta


class User:
    def __init__(self, username, userid, name, second_name, axcess):
        self.username = username
        self.userID = userid
        self.name = name
        self.second_name = second_name
        self.axcess = axcess


def check_user(username, password):
    try:
        user_from_db = database.return_user(username)[0]
    except IndexError:
        return False
    user = User(user_from_db[1], user_from_db[0], user_from_db[3],
                user_from_db[4], user_from_db[5])
    salt = user_from_db[2].split(',')[1]
    hashed_password = utils.hash_password(password, salt)
    if hashed_password == user_from_db[2].split(',')[0]:
        return user
    else:
        return False


def create_user(username, first_name, second_name, password, axcess=5):
    salt = utils.gennerate_salt()
    hashed_password = utils.hash_password(password, salt) + ',' + salt
    values = [first_name, second_name, username, hashed_password, axcess]
    database.add_user(values)


def update_user(id, permissions, badge):
    database.update_user(id, permissions, badge)


def check_parking(badge):
    dates = badge[0][1].split(',')
    datetime_dates = []
    for day in dates:
        day = day.split('/')
        datetime_dates.append(
            datetime.strptime(day[0] + ' ' + day[1] + ' 2019', '%d %b ''%Y'))
    current_date = datetime.today()
    parking = 'True'
    for day in datetime_dates:
        for i in range(0, 6):
            if current_date.date() == (day + timedelta(days=i)).date():
                parking = 'False'
    return parking


if __name__ == '__main__':
    create_user('toor', 'josh', 'mugglestone', 'root', '1')
