import sqlite3

connection = sqlite3.connect('Database.db', check_same_thread=False)


def add_user(values):
    cursor = connection.cursor()
    sql = '''insert into Login(FirstName,Surname,Username,Password,Roles)
        VALUES('{0}','{1}','{2}','{3}','{4}');'''.format(values[0], values[1],
                                                         values[2], values[3],
                                                         values[4])
    cursor.execute(sql)
    connection.commit()


def remove_user(id):
    sql = '''UPDATE Login
            SET Roles = 'Removed' 
            WHERE EmployeeNo = '{0}' '''.format(id)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()


def return_user(username):
    sql = ('''SELECT * from Login WHERE Username='{0}' 
    AND Roles IS NOT 'Removed';''').format(username)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    return cursor.fetchall()


def return_user_id(id):
    sql = '''SELECT * from Login WHERE EmployeeNo='{0}';'''.format(id)
    cursor = connection.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def manage_users():
    sql = '''SELECT Login.EmployeeNo, Login.Username, Login.FirstName, Login.Surname,
    Login.Roles, BadgeLink.BadgeColour
    FROM Login
    LEFT JOIN BadgeLink ON Login.EmployeeNo=BadgeLink.EmployeeNo
    WHERE Roles IS NOT 'Removed' '''
    cursor = connection.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def manage_users_adimin(dept):
    sql = '''SELECT Login.EmployeeNo, Login.Username, Login.FirstName, Login.Surname,
    Login.Roles, BadgeLink.BadgeColour, Employee.EmployerDept
    FROM Login
    LEFT JOIN BadgeLink ON Login.EmployeeNo=BadgeLink.EmployeeNo
    LEFT JOIN Employee ON Login.EmployeeNo=Employee.EmployeeNo
    WHERE Employee.EmployerDept = '{0}' '''.format(dept)
    cursor = connection.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def manage_users_search(key, search):
    sql = '''SELECT Login.EmployeeNo, Login.Username, Login.FirstName, Login.Surname,
    Login.Roles, BadgeLink.BadgeColour
    FROM Login
    LEFT JOIN BadgeLink ON Login.EmployeeNo=BadgeLink.EmployeeNo
    WHERE {0} = '{1}' '''.format(key, search)
    cursor = connection.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def manage_users_search_adimin(key, search, dept):
    sql = '''SELECT Login.EmployeeNo, Login.Username, Login.FirstName, Login.Surname,
    Login.Roles, BadgeLink.BadgeColour, Employee.EmployerDept
    FROM Login
    LEFT JOIN BadgeLink ON Login.EmployeeNo=BadgeLink.EmployeeNo
    LEFT JOIN Employee ON Login.EmployeeNo=Employee.EmployeeNo
    WHERE {0} = '{1}' 
    AND Employee.EmployerDept = '{2}' '''.format(key, search, dept)
    cursor = connection.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def update_user(id, permissions, badge):
    sql = '''UPDATE Login
             SET Roles = '{0}' 
             WHERE EmployeeNo = {1}'''.format(permissions, id)
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.execute('''SELECT * FROM BadgeLink WHERE EmployeeNo = '{0}' '''.format(id))
    test = cursor.fetchall()
    if test:
        print('update')
        sql = '''UPDATE BadgeLink 
        SET BadgeColour = '{0}' 
        WHERE EmployeeNo = '{1}' '''.format(badge, id)
    else:
        sql = '''INSERT INTO BadgeLink (EmployeeNo, BadgeColour) 
        VALUES ('{1}', '{0}') '''.format(badge, id)
    cursor.execute(sql)
    connection.commit()


def update_user_info(id, mobile, postcode, employer, type_of_employment, blue_badge):
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM Employee WHERE EmployeeNo = '{0}' '''.format(id))
    test = cursor.fetchall()
    if test:
        print('update')
        sql = '''UPDATE Employee 
        SET MobileNo = '{0}', 
            Postcode = '{1}', 
            EmployerDept = '{2}', 
            TypeOfEmployment = '{3}',
            BlueBadge = '{4}'
        WHERE EmployeeNo = '{5}' '''.format(mobile, postcode, employer, type_of_employment,
                                            blue_badge, id)
    else:
        sql = '''INSERT INTO Employee (EmployeeNo, MobileNo, Postcode, EmployerDept, ExtensionNo, 
        TypeOfEmployment, BlueBadge) 
        VALUES ('{0}', '{1}', '{2}', '{3}', 
        '{4}', '{5}', '{6}') '''.format(id, mobile, postcode, employer, 'Not',
                                          type_of_employment, blue_badge)
    cursor.execute(sql)
    connection.commit()


def create_car(reg, id, make, electric):
    sql = '''INSERT INTO Registration (VehicleReg, EmployeeNo, VehicleMake, ElectricCar)
    VALUES ('{0}','{1}','{2}','{3}') '''.format(reg, id, make, electric)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()


def get_car(id):
    sql = '''SELECT * from Registration WHERE EmployeeNo='{0}'
    AND Active IS Null;'''.format(id)
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


def remove_car(id):
    sql = '''UPDATE Registration
    SET Active = 'No' 
    WHERE VehicleReg = '{0}' '''.format(id)
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


def get_badge(id):
    sql = '''SELECT BadgeLink.BadgeColour, Badge.Dates
     FROM BadgeLink
     LEFT JOIN Badge ON BadgeLink.BadgeColour=Badge.BadgeColour
     WHERE EmployeeNo = {0}'''.format(id)
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


def get_bookings():
    sql = '''SELECT DateTimeIN, DateTimeOUT, ParkingNo, BookingID FROM Booking
    WHERE Active = 'Yes' '''
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


def create_booking(reg, date_in, date_out, parking_no, bay_type, active):
    sql = '''INSERT INTO Booking (VehicleReg, DateTimeIN, DateTimeOUT, 
    ParkingNo, BayType, Active)
    VALUES ('{0}','{1}','{2}','{3}','{4}','{5}') '''.format(reg, date_in, date_out,
                                                      parking_no, bay_type, active)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()


def delete_booking(id):
    sql = '''UPDATE Booking
             SET Active = 'No' 
             WHERE BookingID = {0}'''.format(id)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()


def get_bookings_reg(reg):
    cursor = connection.cursor()
    cursor.execute(('''SELECT * FROM Booking WHERE VehicleReg='{0}' 
    AND Active = 'Yes' '''.format(reg)))
    data = cursor.fetchall()
    return data


def get_bookings_reg_previous(reg):
    cursor = connection.cursor()
    cursor.execute(('''SELECT * FROM Booking WHERE VehicleReg='{0}' 
    AND Active = 'No' '''.format(reg)))
    data = cursor.fetchall()
    print(data)
    return data


def get_employee(reg):
    cursor = connection.cursor()
    cursor.execute(('''SELECT * FROM Employee WHERE EmployeeNo='{0}' 
    '''.format(reg)))
    data = cursor.fetchall()
    return data


def report_id():
    sql = '''SELECT Registration.EmployeeNo, Booking.VehicleReg, 
    Booking.ParkingNo, Booking.DateTimeIN, Booking.DateTimeOUT
    FROM Booking
    LEFT JOIN Registration ON Registration.VehicleReg=Booking.VehicleReg'''
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


def report_id_key(id):
    sql = '''SELECT Registration.EmployeeNo, Booking.VehicleReg, 
    Booking.ParkingNo, Booking.DateTimeIN, Booking.DateTimeOUT
    FROM Booking
    LEFT JOIN Registration ON Registration.VehicleReg=Booking.VehicleReg
    WHERE Registration.EmployeeNo = '{0}' '''.format(id)
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    return data


def report_colour():
    sql = '''SELECT BadgeLink.BadgeColour, 
    Login.EmployeeNo, 
    Registration.VehicleReg, 
    Booking.ParkingNo, 
    Booking.DateTimeIN, 
    Booking.DateTimeOUT
    FROM Booking
    LEFT JOIN Registration ON Registration.VehicleReg=Booking.VehicleReg
    LEFT JOIN Login ON Registration.EmployeeNo = Login.EmployeeNo
    LEFT JOIN BadgeLink ON Login.EmployeeNo = BadgeLink.EmployeeNo'''
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


def report_colour_key(colour):
    sql = '''SELECT BadgeLink.BadgeColour, 
    Login.EmployeeNo, 
    Registration.VehicleReg, 
    Booking.ParkingNo, 
    Booking.DateTimeIN, 
    Booking.DateTimeOUT
    FROM Booking
    LEFT JOIN Registration ON Registration.VehicleReg=Booking.VehicleReg
    LEFT JOIN Login ON Registration.EmployeeNo = Login.EmployeeNo
    LEFT JOIN BadgeLink ON Login.EmployeeNo = BadgeLink.EmployeeNo
    WHERE BadgeLink.BadgeColour = '{0}' '''.format(colour)
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


if __name__ == '__main__':
    #values = ['josh', 'mugglestone', 'root', 'toor', '1']
    #print(manage_users_search(1,1))
    sql = ''' ALTER TABLE Registration
    ADD Active TEXT; '''
    print(report_colour_key('White'))

"""
    sql = '''CREATE TABLE user(
            userID int AUTO_INCREMENT,
            firstname varchar(255) NOT NULL,
            surname varchar(255) NOT NULL,
            username varchar(255) NOT NULL,
            password varchar(255) NOT NULL,
            axcess int NOT NULL,
            UNIQUE (username),
            PRIMARY KEY (userID))'''
"""
