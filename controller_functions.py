from config import db
from models import User, Trip, Plate, Find
from sqlalchemy.sql import or_
from flask import render_template, request, redirect, session, flash

def index():
    if 'uid' in session:
        return redirect('/home')
    return render_template("login.html")

def login():
    user = User.log_validate(request.form)
    if user:
        session['uid'] = user.id
        session['pw'] = user.password
        return redirect('/home')
    return redirect('/')

def new_user():
    return render_template("new_user.html")

def create_user():
    validate = User.reg_validate(request.form)
    if validate:
        new_user = User.add_new_user(request.form)
        session['uid'] = new_user.id
        session['pw'] = new_user.password
        return redirect('/home')
    return redirect('/')

def home():
    if 'uid' in session:
        current_user = User.current_user(session['uid'])
        if current_user.password == session['pw']:
            # check for ongoing trip and redirect
            return render_template('home.html', current_user = current_user)
    return redirect('/')