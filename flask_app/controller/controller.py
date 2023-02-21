from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.model.users import Users
from flask_app.model.appointment import Appointments
from flask import flash
from flask_bcrypt import Bcrypt
from datetime import datetime


bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect ('/')

    
@app.route('/dashboard')
def user():
    appointments = Appointments.all_appointments()
    today = datetime.today()
    previous_events = [appointment for appointment in appointments if appointment.date < today.date() or (appointment.date == today.date() and appointment.time < today.time())] #copied from stackoverflow
    return render_template('user.html', appointments = appointments, previous_events = previous_events, today=today)

@app.route('/register_user', methods=['POST'])
def register():
    if not Users.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password']) #password string came from request.form['password']
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    Users.add_user(data) #simply means User.add_user what is the value of data 
    flash("Successfully Registered")
    return redirect ('/')

@app.route('/login_user', methods = ['POST'])
def login():
    data = {
        "email" : request.form['email'],
        
    }
    user_in_db = Users.login_user(data) 
    if not user_in_db:
        return redirect ('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash(u"Invalid Email/Password", "login")
        return redirect("/")

    session ['user_first_name'] = user_in_db.first_name #this will be use for the user.html
    session ['user_last_name'] = user_in_db.last_name
    session ['user_id'] = user_in_db.id
    return redirect ('/dashboard')


@app.route('/create_appointment')
def create_appointment():
    return render_template('create_appointment.html')

@app.route('/new_appointment', methods=['POST'])
def new_appointment():
    
    if request.method == 'POST': 
        task = request.form['task']
        date = request.form['date']
        status = request.form['status']
        appointment_date = datetime.strptime(date, '%Y-%m-%d')
        if appointment_date >= datetime.today():
            data = {
                "task" : task,
                "status" : status,
                "date" : appointment_date,
                "user_id" : session['user_id']
            }
            Appointments.add_appointment(data)
            return redirect('/dashboard')
        else:
            flash("You can't create appointments in the past!")
        return render_template('create_appointment.html')



@app.route('/delete_appointment/<id>')
def delete_appointment(id):
    
    data = {
        "id" : id
    }
    Appointments.delete_appointment(data) 
    return redirect('/dashboard')

@app.route('/update_appointment/<id>')
def retrieve_recipe(id):
    data = {
        "id" : id
    }
    appointment = Appointments.retrieve_appointment(data)
    session ['id'] = appointment.id
    return render_template("updateappointment.html", appointment = appointment)



@app.route('/updateappointment', methods=['POST'])
def update_appointment():

    data = {
        "task" : request.form['task'],
        "status" : request.form['status'],
        "date" : request.form['date'],
        "user_id" : session['user_id'],
        "id" : session['id']
    }
    Appointments.update_appointment(data)
    return redirect ('/dashboard')

