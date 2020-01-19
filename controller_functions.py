from config import db
from models import User, Trip, Plate, Find
from flask import render_template, request, redirect, session, flash

def index():
    if 'uid' in session:
        return redirect('/ongoing')
    return render_template("login.html")

def login():
    user = User.log_validate(request.form)
    if user:
        session['uid'] = user.id
        session['pw'] = user.password
        return redirect('/ongoing')
    return redirect('/')

def new_user():
    return render_template("new_user.html")

def create_user():
    validate = User.reg_validate(request.form)
    if validate:
        new_user = User.add_new_user(request.form)
        session['uid'] = new_user.id
        session['pw'] = new_user.password
        new_user.initialize_plates()
        return redirect('/home')
    return redirect('/new_user')

def current_user():
    if 'uid' in session:
        current_user = User.current_user(session['uid'])
        if current_user.password == session['pw']:
            return current_user
    return False

def ongoing():
    user = current_user()
    if not user:
        return redirect('/logout')
    trip = user.ongoing_trip()
    if not trip:
        return redirect('/home')
    session['tid'] = trip.id
    return render_template('ongoing.html', user = user, trip = trip)

def render_lists():
    user = User.current_user(session['uid'])
    trip = Trip.current_trip(session['tid'])
    finds_list = [find.plate for find in trip.ordered_finds()]
    return render_template('partials/lists.html', user=user, trip=trip, finds_list=finds_list)

def find(id):
    Find.find_plate(id, session['tid'])
    return redirect('/render_lists')

def unfind(id):
    find = Find.get_find(id, session['tid'])
    find.unfind()
    return redirect('/render_lists')

def new_plate():
    validate = Plate.validate_plate(request.form)
    if validate:
        new_plate = Plate.create_plate(request.form)
        print(new_plate)
        return redirect(f'/find/{new_plate}')
    return redirect('/render_lists')

def home():
    user = current_user()
    if not user:
        return redirect('/logout')
    return render_template('home.html', user = user)

def trip_detail(id):
    trip = Trip.current_trip(id)
    finds = trip.ordered_finds()
    return render_template('trip_detail.html', trip=trip, finds = finds)

def start_trip():
    validate = Trip.validate_trip(request.form)
    if validate:
        new_trip = Trip.start_trip(request.form)
        return redirect('/ongoing')
    return redirect('/home')

def end_trip(id):
    trip = Trip.current_trip(id)
    trip.end_trip()
    return redirect('/home')

def logout():
    session.clear()
    return redirect('/')