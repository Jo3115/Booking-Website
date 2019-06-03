from flask import Flask, render_template, url_for, request, session, \
    redirect, send_from_directory
import os
import datetime
import user
import database
import utils


app = Flask(__name__)


app.secret_key = ''''b"\xe6\xf9+G-\xda\x90\xc6\\8\xd2\xe2'\x10e\xd6\x073c\x7f
\n\xdd\xcd\x91"'''


def check_logged_in():
    try:
        return session['user']
    except KeyError:
        return ' '


@app.route('/home')
def home_page():
    """Displays The Homepage"""
    if check_logged_in() == ' ':
        return redirect(url_for('login_page'))
    elif session['user'][4] == 'Facilities':
        return redirect(url_for('reports'))
    else:
        operation = request.args.get('operation')
        booking_id = request.args.get('booking_id')
        if operation == 'delete':
            database.delete_booking(booking_id)
        badge = ''
        try:
            badge = database.get_badge(session['user'][3])[0][1]
            badge = badge.split(',')
        except IndexError:
            pass
        car = database.get_car(session['user'][3])
        parking = []
        for i in car:
            for x in database.get_bookings_reg(i[0]):
                parking.append(x)
        return render_template('home.html',
                               user=check_logged_in(),
                               badge=badge,
                               parking=parking,
                               badge_true=utils.check_badge(session['user'][3]))


@app.route('/', methods=['GET', 'POST'])
def login_page():
    """"""
    if check_logged_in() == ' ':
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if username == '' or password == '':
                return render_template('login.html',
                                       error='Username Or Password Is Blank',
                                       user=check_logged_in())
            user_temp = user.check_user(username, password)
            if user_temp is False:
                return render_template('login.html',
                                       error='Incorrect Login',
                                       user=check_logged_in())
            else:
                session['user'] = [user_temp.username, user_temp.name,
                                   user_temp.second_name, user_temp.userID,
                                   user_temp.axcess]
                try:
                    badge = database.get_badge(session['user'][3])
                    session['user'].append(user.check_parking(badge))
                except IndexError:
                    pass
                return redirect(url_for('home_page'))
        return render_template('login.html',
                               user=check_logged_in())
    else:
        return redirect(url_for('home_page'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login_page'))


@app.route('/manage_users_page')
def manage_users_page():
    if check_logged_in() != ' ':
        if session['user'][4] == 'Admin':
            operation = request.args.get('operation')
            user_id = request.args.get('user_id')
            key = request.args.get('key')
            search = request.args.get('search')
            if operation == 'delete':
                database.remove_user(user_id)
            if operation == 'search' and search != '':
                try:
                    data = database.manage_users_search(key, search)
                except:
                    data = []
            else:
                data = database.manage_users()
            return render_template('manage_users.html',
                                   user=check_logged_in(),
                                   data=data)
        elif session['user'][4] == 'Manager':
            operation = request.args.get('operation')
            user_id = request.args.get('user_id')
            key = request.args.get('key')
            search = request.args.get('search')
            try:
                dept = database.get_employee(session['user'][3])[0][3]
            except:
                dept = ''
            if operation == 'delete':
                database.remove_user(user_id)
            elif operation == 'search' and search != '':
                try:
                    data = database.manage_users_search_admin(key, search,
                                                              dept)
                except:
                    data=[]
            else:
                data = database.manage_users_adimin(dept)
            return render_template('manage_users.html',
                                   user=check_logged_in(),
                                   data=data)
    return redirect(url_for('login_page'))


@app.route('/manage_users_page/reservations')
def manage_user_reservations():
    if check_logged_in() != ' ':
        if session['user'][4] == 'Admin' or session['user'][4] == 'Manager':
            user_id = request.args.get('user_id')
            operation = request.args.get('operation')
            booking_id = request.args.get('booking_id')
            if operation == 'delete':
                database.delete_booking(booking_id)
            car = database.get_car(user_id)
            parking = []
            for i in car:
                for x in database.get_bookings_reg(i[0]):
                    parking.append(x)
            user_checked = database.return_user_id(user_id)
            print(user_checked)
            return render_template('manage_user_reservations.html',
                                   user=check_logged_in(),
                                   user_checked=user_checked,
                                   parking=parking)
    return redirect(url_for('login_page'))


@app.route('/manage_users_page/reservations/previous')
def manage_user_reservations_previous():
    if check_logged_in() != ' ':
        if session['user'][4] == 'Admin' or session['user'][4] == 'Manager':
            user_id = request.args.get('user_id')
            operation = request.args.get('operation')
            booking_id = request.args.get('booking_id')
            if operation == 'delete':
                database.delete_booking(booking_id)
            car = database.get_car(user_id)
            parking = []
            for i in car:
                for x in database.get_bookings_reg_previous(i[0]):
                    parking.append(x)
            user_checked = database.return_user_id(user_id)
            return render_template('manage_user_reservations.html',
                                   user=check_logged_in(),
                                   user_checked=user_checked,
                                   parking=parking,
                                   previous=True)
    return redirect(url_for('login_page'))


@app.route('/create_users_page',  methods=['GET', 'POST'])
def create_users_page():
    if check_logged_in() != ' ':
        if session['user'][4] == 'Admin':
            if request.method == 'POST':
                if '' in [request.form.get('username'),
                          request.form.get('first_name'),
                          request.form.get('seccond_name'),
                          request.form.get('password'),
                          request.form.get('permissions')]:
                    return render_template('create_user.html',
                                           user=check_logged_in(),
                                           error='Entry Was Left Blank')
                else:
                    try:
                        user.create_user(request.form.get('username'),
                                         request.form.get('first_name'),
                                         request.form.get('seccond_name'),
                                         request.form.get('password'),
                                         request.form.get('permissions'))
                    except:
                        return render_template('create_user.html',
                                               user=check_logged_in(),
                                               error='Username Is Already In Use')
                return redirect(url_for('manage_users_page'))
            else:
                return render_template('create_user.html',
                                       user=check_logged_in())
    return redirect(url_for('login_page'))


@app.route('/edit_users_page',  methods=['GET', 'POST'])
def edit_users_page():
    if check_logged_in() != ' ':
        if session['user'][4] == 'Admin':
            id = request.args.get('user_id')
            if request.method == 'POST':
                user.update_user(id,
                                 request.form.get('permissions'),
                                 request.form.get('badge'))
                return redirect(url_for('manage_users_page'))
            else:
                return render_template('eddit_user.html',
                                       user=check_logged_in(),
                                       edit_user=database.return_user_id(id)[0])
    return redirect(url_for('login_page'))


@app.route('/user_info')
def user_info():
    if check_logged_in() != ' ':
        id = request.args.get('user_id')
        print(id)
        if id is None:
            id = session['user'][3]
        badge = ''
        try:
            badge = database.get_badge(id)[0][0]
        except IndexError:
            pass
        data = database.get_employee(id)
        if data == []:
            data = [[], [], [], [], [], []]
        return render_template('user_info.html',
                               user=check_logged_in(),
                               user_information=database.return_user_id(id)[0],
                               badge=badge,
                               data=data)
    return redirect(url_for('login_page'))


@app.route('/edit_users_info',  methods=['GET', 'POST'])
def edit_users_info():
    if check_logged_in() != ' ':
        id = request.args.get('user_id')
        if id is None:
            id = session['user'][3]
        if request.method == 'POST':
            database.update_user_info(id,
                                      request.form.get('Mobile_No'),
                                      request.form.get('Postcode'),
                                      request.form.get('Department'),
                                      request.form.get('type_of_employment'),
                                      request.form.get('blue_badge'))
            return redirect(url_for('manage_users_page'))
        else:
            return render_template('eddit_user_info.html',
                                   user=check_logged_in(),
                                   edit_user=database.return_user_id(id)[0])
    return redirect(url_for('login_page'))


@app.route('/view_car')
def view_car():
    if check_logged_in() != ' ':
        operation = request.args.get('operation')
        car_id = request.args.get('car_id')
        if operation == 'delete':
            database.remove_car(car_id)
        car = database.get_car(session['user'][3])
        print(check_logged_in())
        return render_template('manage_user_cars.html',
                               user=check_logged_in(),
                               car=car)
    return redirect(url_for('login_page'))


@app.route('/register_car',  methods=['GET', 'POST'])
def register_car():
    if check_logged_in() != ' ':
        if request.method == 'POST':
            if len(request.form.get('VehicleReg')) > 7:
                return render_template('register_car.html',
                                       user=check_logged_in(),
                                       error='Car Reg Is To Long')
            database.create_car(request.form.get('VehicleReg'),
                                session['user'][3],
                                request.form.get('VehicleMake'),
                                request.form.get('Electric'))
            return redirect(url_for('home_page'))
        else:
            return render_template('register_car.html',
                                   user=check_logged_in())
    return redirect(url_for('login_page'))


@app.route('/book_parking',  methods=['GET', 'POST'])
def book_parking():
    if check_logged_in() != ' ':
        if request.method == 'POST':
            bays = [i for i in range(1, 1000)]
            car = request.form.get('car').split(',')
            car_info = []
            for i in car:
                car_info.append(i.split(':')[1])
            start = request.form.get('start_time')
            end = request.form.get('finish_time')
            try:
                start_datetime = utils.to_date_time(start)
                end_datetime = utils.to_date_time(end)
            except ValueError:
                return render_template('book_parking.html',
                                       user=check_logged_in(),
                                       cars=database.get_car(session['user'][3]),
                                       error='Invalid Date Entry')
            if start_datetime >= end_datetime:
                return render_template('book_parking.html',
                                       user=check_logged_in(),
                                       cars=database.get_car(session['user'][3]),
                                       error=
                                       'Invalid Date Entry: Start Date Cant Be After End Date')
            if start_datetime < datetime.datetime.now():
                return render_template('book_parking.html',
                                       user=check_logged_in(),
                                       cars=database.get_car(session['user'][3]),
                                       error=
                                       'Invalid Date Entry: Start Date Cant Be In The Past')
            data = database.get_bookings()
            for i in data:
                i_datetime_start = utils.to_date_time(i[0])
                i_datetime_end = utils.to_date_time(i[1])
                if i_datetime_end < datetime.datetime.now():
                    database.delete_booking(i[3])
                if i_datetime_end > start_datetime and i_datetime_start \
                        < end_datetime:
                    bays.remove(i[2])
            if car_info[2].strip() != 'Electric':
                for i in range(1, 101):
                    try:
                        bays.remove(i)
                    except:
                        pass
            try:
                if database.get_employee(session['user'][3])[0][6] == 'No':
                    for i in range(950, 1000):
                        bays.remove(i)
                else:
                    for i in range(1, 949):
                        bays.remove(i)
            except:
                pass
            database.create_booking(car_info[0].strip(), start, end, bays[0],
                                    car_info[2], 'Yes')
            return redirect(url_for('home_page'))
        else:
            return render_template('book_parking.html',
                                   user=check_logged_in(),
                                   cars=database.get_car(session['user'][3]))
    return redirect(url_for('login_page'))


@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if check_logged_in() != ' ':
        if request.method == 'POST':
            key = request.args.get('key')
            instuction = request.form.getlist('id')
            if instuction is []:
                return render_template('reports_main.html',
                                       user=check_logged_in(),
                                       key=request.args.get('key'),
                                       data=database.manage_users(),
                                       error='Select At Least 1 Option')
            start = request.form.get('start_time')
            print(start)
            end = request.form.get('finish_time')
            try:
                start_datetime = utils.to_date_time(start)
                end_datetime = utils.to_date_time(end)
            except ValueError:
                return render_template('reports_main.html',
                                       user=check_logged_in(),
                                       key=request.args.get('key'),
                                       data=database.manage_users(),
                                       error='Invalid Date Entry')
            if key != 'Colour':
                if instuction[0] == 'All Users':
                    from_db = database.report_id()
                else:
                    from_db = []
                    for user in instuction:
                        id = (user.split(','))[0].split(' ')[1]
                        data = database.report_id_key(id)
                        for entry in data:
                            from_db.append(entry)
                data = []
                for i in from_db:
                    i_datetime_start = utils.to_date_time(i[3])
                    i_datetime_end = utils.to_date_time(i[4])
                    if i_datetime_end > start_datetime and i_datetime_start \
                            < end_datetime:
                        data.append('{0},{1},{2},{3},{4}'.format(i[0],
                                                                 i[1],
                                                                 i[2],
                                                                 i[3],
                                                                 i[4]))
                f = open('C:\\Users\\joshu\\OneDrive\\python\\cib'
                         '\\static\\output.csv', 'w')
                f.write('Employee ID, Car Reg, Parking Bay,'
                        'Start Time, End Time \n')
                for line in data:
                    f.write(line)
                    f.write('\n')
                f.close()

            else:
                if instuction[0] == 'All Colours':
                    from_db = database.report_colour()
                else:
                    from_db = []
                    for colour in instuction:
                        data = database.report_colour_key(colour)
                        for entry in data:
                            from_db.append(entry)
                data = []
                for i in from_db:
                    i_datetime_start = utils.to_date_time(i[4])
                    i_datetime_end = utils.to_date_time(i[5])
                    if i_datetime_end > start_datetime and i_datetime_start \
                            < end_datetime:
                        data.append('{0},{1},{2},{3},{4},{5}'.format(i[0],
                                                                     i[1],
                                                                     i[2],
                                                                     i[3],
                                                                     i[4],
                                                                     i[5]))
                f = open('C:\\Users\\joshu\\OneDrive\\python\\cib'
                         '\\static\\output.csv', 'w')
                f.write('Permit Colour, Employee ID, Car Reg, Parking Bay,'
                        'Start Time, End Time \n')
                for line in data:
                    f.write(line)
                    f.write('\n')
                f.close()
            return send_from_directory(directory='static',
                                       filename='output.csv',
                                       as_attachment=True)
        else:
            return render_template('reports_main.html',
                                   user=check_logged_in(),
                                   key=request.args.get('key'),
                                   data=database.manage_users())
    return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run()
